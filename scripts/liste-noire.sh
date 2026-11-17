#!/usr/bin/env bash
# liste-noire.sh : refuse qu'un mot de la liste noire de l'utilisateur entre dans ce dépôt.
#
# La liste vit dans l'instance, jamais ici : ~/.config/harness/interdits.txt
# (un mot par ligne, sans tenir compte des majuscules, lignes # ignorées).
#
# Usage :
#   bash scripts/liste-noire.sh --index            fichiers prêts à être commités et auteur (hook pre-commit)
#   bash scripts/liste-noire.sh --message <fichier> message de commit (hook commit-msg)
#   bash scripts/liste-noire.sh --push             lit sur l'entrée les références poussées (hook pre-push) :
#                                                  noms de branche et d'étiquette, messages et contenu des commits
#   bash scripts/liste-noire.sh --tout [dossier]   tout le dossier, hors .git (avant un premier commit)
#
# Résultat : dernière ligne OK ou STOP. Code 0 si rien trouvé, 1 sinon.
# Sans liste noire, il refuse : un garde-fou absent ne doit pas passer pour un feu vert.

set -uo pipefail
shopt -s lastpipe  # "texte | chercher" garde la trouvaille dans le shell courant

LISTE="${HARNESS_INTERDITS:-$HOME/.config/harness/interdits.txt}"

stop() { echo "STOP : $*" >&2; echo "STOP"; exit 1; }

[ -r "$LISTE" ] || stop "liste noire introuvable ($LISTE). Lancez installer.sh --config <instance>/config."
MOTIFS="$(mktemp)"
trap 'rm -f -- "$MOTIFS"' EXIT
grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' -- "$LISTE" > "$MOTIFS"
[ -s "$MOTIFS" ] || stop "liste noire vide ($LISTE)."

trouve=0
signaler() { echo "  [interdit] $*" >&2; trouve=1; }

# Lit un texte sur l'entrée et signale chaque ligne qui contient un mot interdit.
chercher() {
  local ou="$1"
  local lignes
  lignes="$(grep -n -i -F -f "$MOTIFS" || true)"
  [ -z "$lignes" ] || while IFS= read -r l; do signaler "$ou, ligne ${l%%:*}"; done <<< "$lignes"
}

case "${1:-}" in
  --index)
    # L'auteur du commit part avec lui : nom et e-mail sont publics aussi.
    git var GIT_AUTHOR_IDENT | chercher "auteur du commit"
    git var GIT_COMMITTER_IDENT | chercher "auteur (committer) du commit"
    while IFS= read -r -d '' f; do
      printf '%s\n' "$f" | chercher "nom de fichier $f"
      git show ":$f" 2>/dev/null | chercher "$f"
    done < <(git diff --cached --name-only -z --diff-filter=ACMR)
    ;;
  --message)
    [ -r "${2:-}" ] || stop "fichier du message introuvable."
    grep -v '^#' -- "$2" | chercher "message de commit"
    ;;
  --push)
    zero="0000000000000000000000000000000000000000"
    while read -r ref_locale sha_local ref_distante _; do
      [ "$sha_local" = "$zero" ] && continue   # suppression d'une branche : rien n'est envoyé
      printf '%s\n%s\n' "$ref_locale" "$ref_distante" | chercher "nom de branche ou d'étiquette $ref_distante"
      # Commits envoyés : ceux qu'aucune branche distante connue ne contient déjà.
      for c in $(git rev-list "$sha_local" --not --remotes); do
        git log -1 --format=%B "$c" | chercher "message du commit ${c:0:7}"
        git log -1 --format='%an <%ae>%n%cn <%ce>' "$c" | chercher "auteur du commit ${c:0:7}"
        git diff-tree --no-commit-id --name-only -r "$c" | chercher "nom de fichier du commit ${c:0:7}"
        git grep -I -n -i -F -f "$MOTIFS" "$c" -- . > /dev/null 2>&1 && signaler "contenu du commit ${c:0:7}"
      done
      # Une étiquette annotée a aussi son propre message.
      if [ "$(git cat-file -t "$sha_local")" = "tag" ]; then
        git cat-file -p "$sha_local" | chercher "message de l'étiquette $ref_distante"
      fi
    done
    ;;
  --tout)
    dossier="${2:-.}"
    while IFS= read -r -d '' f; do
      printf '%s\n' "${f#"$dossier"/}" | chercher "nom de fichier ${f#"$dossier"/}"
      chercher "${f#"$dossier"/}" < "$f"
    done < <(find "$dossier" -name .git -prune -o -type f -print0)
    ;;
  *)
    echo "Usage : bash scripts/liste-noire.sh --index | --message <fichier> | --push | --tout [dossier]" >&2
    exit 2
    ;;
esac

if [ "$trouve" -ne 0 ]; then
  echo "Un mot de la liste noire a été trouvé. Retirez-le, ou mettez ce contenu dans votre instance." >&2
  echo "STOP"
  exit 1
fi
echo "OK"
