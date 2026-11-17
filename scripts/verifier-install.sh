#!/usr/bin/env bash
# verifier-install.sh : contrôle que le harness est bien branché. Ne modifie rien.
#
# Ce qu'il contrôle :
#   - le dépôt  : AGENTS.md, CLAUDE.md, règle test, fichiers secrets, état Git ;
#   - l'instance : ~/.config/harness, harness.conf, profil.md, interdits.txt ;
#   - les règles : le AGENTS.md généré est à jour, et Claude Code comme OpenCode le lisent ;
#   - les skills : ceux du moteur et ceux de l'instance respectent le format et sont reliés ;
#   - les liens cassés et les skills en double ;
#   - les scripts : droit d'exécution, sur le PC et dans Git, et la commande nouveau-projet.
#
# Ce qu'il garantit :
#   - lecture seule : aucune création, aucun déplacement, aucune suppression ;
#   - pas d'accès réseau : l'état GitHub est le dernier connu par ce PC.
#
# Résultat :
#   [OK]         tout va bien
#   [ATTENTION]  ça marche, mais quelque chose mérite un coup d'oeil
#   [PROBLÈME]   quelque chose ne marchera pas
#   Dernière ligne : OK, ou STOP s'il y a au moins un problème.
#   Code de sortie : 0 sans problème, 1 s'il y a au moins un problème.
#
# Usage :
#   bash scripts/verifier-install.sh

set -uo pipefail

case "${1:-}" in
  "") ;;
  -h|--aide) echo "Usage : bash scripts/verifier-install.sh"; exit 0 ;;
  *) echo "Option inconnue : $1" >&2; echo "Usage : bash scripts/verifier-install.sh" >&2; exit 2 ;;
esac

if [ "$(id -u)" -eq 0 ]; then
  echo "Arrêt : ne lancez pas ce script avec sudo ni en root. Il contrôlerait le mauvais dossier personnel." >&2
  exit 1
fi

DOSSIER_SCRIPT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DEPOT="$(cd -- "$DOSSIER_SCRIPT/.." && pwd -P)"
CLAUDE="$HOME/.claude"
OPENCODE="$HOME/.config/opencode"
AGENTS_PARTAGES="$HOME/.agents"
CONFIG="$HOME/.config/harness"
GENERE="${XDG_STATE_HOME:-$HOME/.local/state}/harness/AGENTS.md"

ok=0
attention=0
problemes=0

bon()  { echo "  [OK] $*";        ok=$((ok + 1)); }
avert(){ echo "  [ATTENTION] $*"; attention=$((attention + 1)); }
grave(){ echo "  [PROBLÈME] $*";  problemes=$((problemes + 1)); }

# Contrôle qu'un lien existe et pointe vers la bonne cible.
controler_lien() {
  local cible="$1"
  local lien="$2"
  if [ -L "$lien" ]; then
    local vers
    vers="$(readlink -- "$lien")"
    if [ "$vers" = "$cible" ]; then
      bon "$lien"
    else
      grave "$lien pointe ailleurs : $vers. Lancez installer.sh."
    fi
  elif [ -e "$lien" ]; then
    grave "$lien est un vrai fichier ou dossier, pas un lien. Lancez installer.sh, il le mettra de côté."
  else
    grave "$lien n'existe pas. Lancez installer.sh."
  fi
}

# Lit la valeur d'un champ dans l'en-tête d'un SKILL.md (entre les deux lignes ---).
lire_champ() {
  local fichier="$1"
  local champ="$2"
  awk -v champ="$champ" '
    NR == 1 { if ($0 != "---") exit; next }
    $0 == "---" { exit }
    index($0, champ ":") == 1 {
      valeur = substr($0, length(champ) + 2)
      sub(/^[ \t]+/, "", valeur)
      sub(/[ \t\r]+$/, "", valeur)
      if (valeur ~ /^".*"$/ || valeur ~ /^'\''.*'\''$/) valeur = substr(valeur, 2, length(valeur) - 2)
      print valeur
      exit
    }
  ' "$fichier"
}

# Liste les champs de l'en-tête d'un SKILL.md.
lister_champs() {
  awk '
    NR == 1 { if ($0 != "---") exit; next }
    $0 == "---" { exit }
    /^[A-Za-z_-]+:/ { sub(/:.*/, ""); print }
  ' "$1"
}

echo "Dépôt harness : $DEPOT"
echo "Contrôle en lecture seule : rien ne sera modifié."
echo

# ---------------------------------------------------------------- Dépôt
echo "Dépôt"
if [ -f "$DEPOT/AGENTS.md" ]; then
  bon "AGENTS.md présent ($(wc -l < "$DEPOT/AGENTS.md") lignes)"
  if grep -q "copeau-42" "$DEPOT/AGENTS.md"; then
    bon "règle test présente (copeau-42)"
  else
    avert "règle test copeau-42 absente de AGENTS.md"
  fi
else
  grave "AGENTS.md introuvable. Ce script doit rester dans le dossier scripts/ du dépôt."
  echo
  echo "Bilan : $ok OK, $attention attention, $problemes problème(s)."
  exit 1
fi

if [ -f "$DEPOT/CLAUDE.md" ] && grep -q "^@AGENTS.md" "$DEPOT/CLAUDE.md"; then
  bon "CLAUDE.md du dépôt importe AGENTS.md"
else
  avert "CLAUDE.md du dépôt absent ou sans la ligne @AGENTS.md"
fi

if command -v git >/dev/null 2>&1 && git -C "$DEPOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if ! suivis="$(git -C "$DEPOT" ls-files 2>&1)"; then
    avert "Git ne répond pas, contrôles Git sautés : $(echo "$suivis" | head -n 1)"
    suivis=""
  fi
  secrets="$(printf '%s\n' "$suivis" | grep -E '(^|/)(\.env(\..*)?|id_rsa|id_ed25519|.*\.pem|.*\.key)$' || true)"
  if [ -n "$secrets" ]; then
    grave "fichier(s) secret(s) suivi(s) par Git : $(echo "$secrets" | tr '\n' ' ')"
  else
    bon "aucun fichier secret suivi par Git"
  fi

  modifies="$(git --no-optional-locks -C "$DEPOT" status --porcelain | wc -l)"
  if [ "$modifies" -eq 0 ]; then
    bon "aucune modification en attente"
  else
    avert "$modifies fichier(s) modifié(s) ou nouveau(x) pas encore enregistré(s) dans Git"
  fi

  if git -C "$DEPOT" rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
    en_avance="$(git -C "$DEPOT" rev-list --count '@{upstream}..HEAD')"
    en_retard="$(git -C "$DEPOT" rev-list --count 'HEAD..@{upstream}')"
    if [ "$en_avance" -eq 0 ] && [ "$en_retard" -eq 0 ]; then
      bon "identique à GitHub (dernier état connu par ce PC)"
    else
      [ "$en_avance" -gt 0 ] && avert "$en_avance enregistrement(s) pas encore envoyé(s) sur GitHub (git push)"
      [ "$en_retard" -gt 0 ] && avert "$en_retard enregistrement(s) de GitHub pas encore récupéré(s) (git pull)"
    fi
  else
    avert "pas de lien avec un dépôt GitHub pour cette branche"
  fi
else
  avert "ce dossier n'est pas un dépôt Git"
fi
echo

# ---------------------------------------------------------------- Instance
echo "Instance (~/.config/harness)"
INSTANCE=""
if [ -L "$CONFIG" ] && [ -d "$CONFIG" ]; then
  INSTANCE="$(cd -- "$CONFIG/.." && pwd -P)"
  case "$(cd -- "$CONFIG" && pwd -P)/" in
    "$DEPOT"/*) grave "$CONFIG pointe dans le moteur. La config doit vivre dans le dépôt d'instance." ;;
    *) bon "$CONFIG -> $(readlink -- "$CONFIG")" ;;
  esac
  if [ -f "$CONFIG/harness.conf" ]; then
    prenom="$(sed -n 's/^PRENOM=//p' "$CONFIG/harness.conf" | tail -n 1)"
    [ -n "$prenom" ] && bon "harness.conf lu, PRENOM rempli" || avert "harness.conf sans PRENOM : les agents diront \"l'utilisateur\""
  else
    avert "pas de harness.conf dans $CONFIG"
  fi
  [ -f "$CONFIG/profil.md" ] && bon "profil.md présent" || avert "pas de profil.md : seules les règles du moteur seront lues"
  [ -f "$CONFIG/interdits.txt" ] && bon "interdits.txt présent (liste noire du hook)" || avert "pas de interdits.txt : le hook de liste noire ne bloquera rien"
elif [ -e "$CONFIG" ]; then
  grave "$CONFIG existe mais n'est pas un lien vers un dossier. Lancez installer.sh --config <dossier>."
else
  echo "  [aucune] pas d'instance : moteur seul."
fi
echo

# ---------------------------------------------------------------- Règles
echo "Règles générées"
if [ -f "$GENERE" ]; then
  if cmp -s "$GENERE" <(bash "$DEPOT/scripts/installer.sh" --agents 2>/dev/null); then
    bon "$GENERE à jour (moteur$([ -f "$CONFIG/profil.md" ] && echo " + profil"))"
  else
    grave "$GENERE n'est plus à jour : AGENTS.md ou profil.md a changé. Relancez installer.sh."
  fi
  grep -q "copeau-42" "$GENERE" && bon "règle test présente (copeau-42)" || grave "règle test copeau-42 absente des règles générées"
else
  grave "$GENERE n'existe pas. Lancez installer.sh."
fi
echo

echo "Règles pour Claude Code"
if [ -d "$CLAUDE" ]; then
  controler_lien "$GENERE" "$CLAUDE/CLAUDE.md"
else
  echo "  [ignoré] $CLAUDE n'existe pas : Claude Code n'est pas installé ici."
fi
echo

echo "Règles pour OpenCode"
if [ -d "$OPENCODE" ]; then
  controler_lien "$GENERE" "$OPENCODE/AGENTS.md"
else
  echo "  [ignoré] $OPENCODE n'existe pas : OpenCode n'est pas installé ici."
fi
echo

# ---------------------------------------------------------------- Format des skills
echo "Format des skills (moteur, puis instance)"
noms_skills=()
chemins_skills=()
for dossier in "$DEPOT"/skills/*/ ${INSTANCE:+"$INSTANCE"/skills/*/}; do
  [ -d "$dossier" ] || continue
  nom="$(basename -- "$dossier")"
  fichier="${dossier}SKILL.md"
  if [ ! -f "$fichier" ]; then
    grave "$nom : pas de SKILL.md (en majuscules) dans le dossier"
    continue
  fi
  for deja in "${noms_skills[@]}"; do
    [ "$deja" = "$nom" ] && grave "$nom existe dans le moteur et dans l'instance"
  done
  noms_skills+=("$nom")
  chemins_skills+=("${dossier%/}")
  defauts=""

  if [ "$(head -n 1 "$fichier")" != "---" ]; then
    grave "$nom : l'en-tête doit commencer par une ligne ---"
    continue
  fi

  nom_entete="$(lire_champ "$fichier" name)"
  description="$(lire_champ "$fichier" description)"

  if [ -z "$nom_entete" ]; then
    grave "$nom : champ name absent"
    defauts=1
  elif [ "$nom_entete" != "$nom" ]; then
    grave "$nom : name vaut \"$nom_entete\", il doit être identique au nom du dossier"
    defauts=1
  elif ! printf '%s' "$nom" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' || [ "${#nom}" -gt 64 ]; then
    grave "$nom : nom invalide (minuscules, chiffres, tirets simples, 64 caractères maximum)"
    defauts=1
  fi

  if [ -z "$description" ]; then
    grave "$nom : champ description absent ou vide"
    defauts=1
  elif [ "$description" = ">" ] || [ "$description" = "|" ] || [ "$description" = ">-" ] || [ "$description" = "|-" ]; then
    avert "$nom : description sur plusieurs lignes, longueur non contrôlée. Préférez une seule ligne."
    defauts=1
  elif [ "${#description}" -gt 1024 ]; then
    grave "$nom : description trop longue (${#description} caractères, 1024 maximum)"
    defauts=1
  fi

  autres="$(lister_champs "$fichier" | grep -Ev '^(name|description|license|compatibility)$' | tr '\n' ' ')"
  if [ -n "$autres" ]; then
    avert "$nom : champ(s) en plus dans l'en-tête : $autres(la règle du harness est de s'en passer)"
    defauts=1
  fi

  lignes="$(wc -l < "$fichier")"
  if [ "$lignes" -gt 200 ]; then
    avert "$nom : $lignes lignes, la limite du harness est 200"
    defauts=1
  fi

  [ -z "$defauts" ] && bon "$nom ($lignes lignes)"
done
[ "${#noms_skills[@]}" -eq 0 ] && echo "  [rien] aucun skill trouvé"
echo

# ---------------------------------------------------------------- Installation des skills
# Même choix que installer.sh : ~/.claude/skills, sinon le dossier d'OpenCode.
echo "Skills installés"
if [ -d "$CLAUDE" ]; then
  DOSSIER_SKILLS="$CLAUDE/skills"
elif [ -d "$OPENCODE" ]; then
  DOSSIER_SKILLS="$OPENCODE/skills"
else
  DOSSIER_SKILLS=""
fi

if [ -z "$DOSSIER_SKILLS" ]; then
  echo "  [ignoré] aucun agent trouvé."
else
  for chemin in "${chemins_skills[@]}"; do
    controler_lien "$chemin" "$DOSSIER_SKILLS/$(basename -- "$chemin")"
  done

  # Liens qui visent le moteur ou l'instance mais dont la cible a disparu.
  for dossier_lu in "$CLAUDE/skills" "$OPENCODE/skills" "$AGENTS_PARTAGES/skills"; do
    [ -d "$dossier_lu" ] || continue
    for lien in "$dossier_lu"/*; do
      [ -L "$lien" ] || continue
      vers="$(readlink -- "$lien")"
      case "$vers" in
        "$DEPOT"/*|${INSTANCE:+"$INSTANCE"/*})
          [ -e "$lien" ] || avert "lien cassé : $lien -> $vers (skill retiré du dépôt ?)"
          ;;
      esac
    done
  done

  # Un même nom dans deux dossiers lus par OpenCode crée un doublon.
  for nom in "${noms_skills[@]}"; do
    vus=""
    for dossier_lu in "$CLAUDE/skills" "$OPENCODE/skills" "$AGENTS_PARTAGES/skills"; do
      if [ -e "$dossier_lu/$nom" ] || [ -L "$dossier_lu/$nom" ]; then
        vus="$vus $dossier_lu"
      fi
    done
    if [ "$(echo "$vus" | wc -w)" -gt 1 ]; then
      avert "$nom présent dans plusieurs dossiers :$vus. OpenCode risque de le voir en double."
    fi
  done
fi
echo

# ---------------------------------------------------------------- Scripts et commande nouveau-projet
# L'envoi d'un fichier vers le PC retire le droit d'exécution. Sans ce droit, la commande nouveau-projet est refusée.
echo "Scripts et commande nouveau-projet"
for script in "$DEPOT"/scripts/*.sh; do
  [ -f "$script" ] || continue
  nom_script="$(basename -- "$script")"
  if [ -x "$script" ]; then
    bon "$nom_script est exécutable"
  elif [ "$nom_script" = "nouveau-projet.sh" ]; then
    grave "$nom_script n'est pas exécutable, la commande nouveau-projet sera refusée. Lancez : chmod +x \"$script\""
  else
    avert "$nom_script n'est pas exécutable. Il se lance quand même avec : bash scripts/$nom_script"
  fi
done

# Git doit garder ce droit, sinon il se perd sur un PC neuf.
if command -v git >/dev/null 2>&1 && git -C "$DEPOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  sans_droit="$(git -C "$DEPOT" ls-files -s -- 'scripts/*.sh' | awk '$1 != "100755" { print $4 }' | tr '\n' ' ')"
  if [ -n "$sans_droit" ]; then
    avert "Git n'a pas enregistré le droit d'exécution de : $sans_droit. Lancez : git update-index --chmod=+x <fichier>, puis un commit."
  else
    bon "Git garde le droit d'exécution des scripts"
  fi
fi

controler_lien "$DEPOT/scripts/nouveau-projet.sh" "$HOME/.local/bin/nouveau-projet"
case ":$PATH:" in
  *":$HOME/.local/bin:"*) bon "$HOME/.local/bin est dans le PATH (la liste des dossiers où le terminal cherche les commandes)" ;;
  *) avert "$HOME/.local/bin n'est pas dans le PATH (la liste des dossiers où le terminal cherche les commandes). La commande nouveau-projet ne sera pas trouvée seule." ;;
esac
echo

echo "Bilan : $ok OK, $attention attention, $problemes problème(s)."
if [ "$problemes" -gt 0 ]; then
  echo "Au moins un problème : lancez bash scripts/installer.sh --essai pour voir ce qu'il corrigerait."
  echo "STOP"
  exit 1
fi
echo "Installation conforme."
echo "OK"
exit 0
