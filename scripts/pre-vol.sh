#!/usr/bin/env bash
# pre-vol.sh : liste les blocages humains d'un lot de tickets, avant le codage ou la nuit.
# Ne lit jamais une valeur de secret : seulement des noms.
#
# Usage :
#   pre-vol.sh [--depot compte/depot] [--tous | numéro ...] [--local] [--strict]
#   pre-vol.sh --numero N --corps FICHIER        (contrôle d'un corps, sans GitHub)
#
# --strict : un ticket sans rubrique « Prérequis » compte comme un blocage.
#            À utiliser avant de lancer la nuit ou de déléguer. Sans --strict, c'est un simple avis.
#
# Un prérequis s'écrit dans le ticket : « Prérequis : NOM (GitHub dev), compte X ».
#   NOM sans parenthèses       -> coffre Doppler du serveur
#   NOM (coffre)               -> coffre Doppler du serveur
#   NOM (GitHub dev)           -> secrets et variables de l'environnement « dev »
#   NOM (GitHub depot)         -> secrets et variables du dépôt
#   autre texte ou autre lieu  -> à confirmer par vous
#
# --local : le coffre est joint depuis cette machine, sans SSH. À utiliser sur le serveur.
#
# Codes de sortie :
#   0  aucun blocage déclaré
#   1  au moins un blocage à régler
#   2  usage
#   3  dépôt introuvable

set -uo pipefail

CONF="${HARNESS_CONF:-$HOME/.config/harness/harness.conf}"

lire_conf() {
  [ -f "$CONF" ] && sed -n "s/^$1=//p" "$CONF" | tail -n 1
}

HOTE="$(lire_conf HOTE_SSH_SERVEUR)"
DOPPLER_FILE="$(lire_conf FICHIER_DOPPLER)"

citer() {
  printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"
}

LOCAL=0
STRICT=0
DEPOT=""
TOUS=0
CORPS=""
NUMERO=""
tickets=()

while [ $# -gt 0 ]; do
  case "$1" in
    --depot)  DEPOT="${2:-}"; shift 2 ;;
    --tous)   TOUS=1; shift ;;
    --local)  LOCAL=1; shift ;;
    --strict) STRICT=1; shift ;;
    --corps)  CORPS="${2:-}"; shift 2 ;;
    --numero) NUMERO="${2:-}"; shift 2 ;;
    -h|--aide)
      awk 'NR>1 && /^#/ {sub(/^# ?/, ""); print; next} NR>1 {exit}' "${BASH_SOURCE[0]}"
      exit 0
      ;;
    -*) echo "Option inconnue : $1" >&2; exit 2 ;;
    *)  tickets+=("$1"); shift ;;
  esac
done

# Le dépôt : l'option, sinon le dossier Git courant. Un corps fourni ne vient pas d'un dépôt.
if [ -z "$DEPOT" ] && [ -z "$CORPS" ]; then
  url="$(git remote get-url origin 2>/dev/null || true)"
  case "$url" in
    *github.com[:/]*)
      DEPOT="${url#*github.com}"
      DEPOT="${DEPOT#[:/]}"
      DEPOT="${DEPOT%.git}"
      ;;
  esac
fi

if [ -z "$CORPS" ] && [ -z "$DEPOT" ]; then
  echo "Arrêt : aucun dépôt. Utilisez --depot compte/depot, ou lancez la commande dans le projet." >&2
  exit 3
fi

if [ -z "$CORPS" ] && [ "$TOUS" -eq 0 ] && [ "${#tickets[@]}" -eq 0 ]; then
  echo "Usage : pre-vol.sh [--depot compte/depot] [--tous | numéro ...]" >&2
  exit 2
fi

# Noms de variables déclarés dans .env.example sur preprod (aucune valeur).
noms_exemple() {
  [ -n "$DEPOT" ] || return 0
  gh api "repos/$DEPOT/contents/.env.example?ref=preprod" --jq '.content' 2>/dev/null \
    | tr -d '\n' \
    | base64 -d 2>/dev/null \
    | grep -oE '^[A-Za-z_][A-Za-z0-9_]*' \
    | sort -u
}

# Noms présents dans le coffre, jamais les valeurs.
noms_coffre() {
  local commande
  commande="set -a; . $DOPPLER_FILE; set +a; doppler secrets --only-names --json"
  if [ "$LOCAL" -eq 1 ] || [ -z "$HOTE" ]; then
    bash -c "$commande" 2>/dev/null
  else
    ssh -o BatchMode=yes "$HOTE" "sudo -n -i sh -c $(citer "$commande")" 2>/dev/null
  fi | grep -oE '"[A-Za-z_][A-Za-z0-9_]*"' | tr -d '"' | sort -u
}

# Noms des secrets et variables GitHub, jamais les valeurs. Mis en cache par environnement.
GH_ENV_LU=""
GH_NOMS=""
noms_github() {
  local env="$1"
  if [ "$env" = "$GH_ENV_LU" ]; then
    printf '%s\n' "$GH_NOMS"
    return 0
  fi
  GH_ENV_LU="$env"
  if [ -z "$DEPOT" ]; then
    GH_NOMS=""
  elif [ -n "$env" ]; then
    GH_NOMS="$(
      { gh secret list --repo "$DEPOT" --env "$env" --json name --jq '.[].name' 2>/dev/null || true
        gh variable list --repo "$DEPOT" --env "$env" --json name --jq '.[].name' 2>/dev/null || true
      } | sort -u
    )"
  else
    GH_NOMS="$(
      { gh secret list --repo "$DEPOT" --json name --jq '.[].name' 2>/dev/null || true
        gh variable list --repo "$DEPOT" --json name --jq '.[].name' 2>/dev/null || true
      } | sort -u
    )"
  fi
  printf '%s\n' "$GH_NOMS"
}

liste_exemple=""
liste_coffre=""
coffre_lu=0
if [ -n "$DOPPLER_FILE" ]; then
  liste_coffre="$(noms_coffre)"
  [ -n "$liste_coffre" ] && coffre_lu=1
fi
[ -n "$DEPOT" ] && liste_exemple="$(noms_exemple)"

blocages=0
declare -a lignes=()

ajouter() {
  lignes+=("$(printf '| %-6s | %-38s | %-14s | %s |' "$1" "$2" "$3" "$4")")
  [ "$5" -eq 1 ] && blocages=$((blocages + 1))
}

# Corps d'un ticket : GitHub, ou fichier fourni.
corps_de() {
  if [ -n "$CORPS" ]; then
    cat "$CORPS"
  else
    gh issue view "$1" --repo "$DEPOT" --json body --jq '.body' 2>/dev/null
  fi
}

# Vérifie une variable selon son lieu.
variable() {
  local numero="$1" nom="$2" lieu="$3" bas env dest
  bas="$(printf '%s' "$lieu" | tr 'A-Z' 'a-z')"
  lieu_bas="$bas"
  dest="coffre"
  env=""
  case "$bas" in
    "") ;;
    *github*)
      dest="github"
      env="$(printf '%s' "$lieu" | sed -E 's/.*[Gg][Ii][Tt][Hh][Uu][Bb][[:space:]]*//' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
      case "$(printf '%s' "$env" | tr 'A-Z' 'a-z')" in
        ""|dépôt|depot|du\ dépôt|du\ depot|repo) env="" ;;
      esac
      ;;
    *coffre*|*doppler*) ;;
    *) dest="autre" ;;
  esac

  if [ -n "$DEPOT" ] && ! printf '%s\n' "$liste_exemple" | grep -qxF "$nom"; then
    ajouter "$numero" "$nom" ".env.example" "à déclarer, non bloquant" 0
  fi

  case "$dest" in
    github)
      if [ -n "$env" ]; then
        if noms_github "$env" | grep -qxF "$nom"; then
          ajouter "$numero" "$nom" "GitHub $env" "posée" 0
        else
          ajouter "$numero" "$nom" "GitHub $env" "absente ou illisible" 1
        fi
      else
        if noms_github "" | grep -qxF "$nom"; then
          ajouter "$numero" "$nom" "GitHub dépôt" "posée" 0
        else
          ajouter "$numero" "$nom" "GitHub dépôt" "absente ou illisible" 1
        fi
      fi
      ;;
    coffre)
      if [ "$coffre_lu" -eq 0 ]; then
        ajouter "$numero" "$nom" "coffre" "illisible, à confirmer" 1
      elif printf '%s\n' "$liste_coffre" | grep -qxF "$nom"; then
        ajouter "$numero" "$nom" "coffre" "posée" 0
      else
        ajouter "$numero" "$nom" "coffre" "absente" 1
      fi
      ;;
    autre)
      ajouter "$numero" "$nom" "$lieu" "à confirmer" 1
      ;;
  esac
}

traiter() {
  local numero="$1" corps="$2" ligne item nom lieu declare=0
  while IFS= read -r ligne; do
    declare=1
    ligne="$(printf '%s' "$ligne" | sed -E 's/^[^:]*:[[:space:]]*//' | tr ';' '\n' | tr ',' '\n')"
    while IFS= read -r item; do
      item="$(printf '%s' "$item" \
        | tr -d '`*' \
        | sed -E 's/^[[:space:]>_-]+//; s/[[:space:]]+$//; s/\.$//')"
      [ -n "$item" ] || continue
      case "$(printf '%s' "$item" | tr 'A-Z' 'a-z')" in
        aucun|aucune|rien|neant|néant) continue ;;
      esac

      nom="$item"
      lieu=""
      case "$item" in
        *\(*\))
          nom="$(printf '%s' "$item" | sed -E 's/[[:space:]]*\([^)]*\)[[:space:]]*$//' | sed -E 's/[[:space:]]+$//')"
          lieu="$(printf '%s' "$item" | sed -E 's/^[^(]*\(([^)]*)\)[[:space:]]*$/\1/')"
          ;;
      esac
      [ -n "$nom" ] || continue

      if printf '%s' "$nom" | grep -qE '^[A-Z][A-Z0-9_]{2,}$'; then
        variable "$numero" "$nom" "$lieu"
      else
        if [ -n "$lieu" ]; then
          ajouter "$numero" "$nom" "$lieu" "à confirmer" 1
        else
          ajouter "$numero" "$nom" "vous" "à confirmer" 1
        fi
      fi
    done <<< "$ligne"
  done < <(printf '%s\n' "$corps" | grep -iE '^[[:space:]>*_-]*[[:space:]]*pr[ée]requis[[:space:]]*:')
  if [ "$declare" -eq 0 ]; then
    ajouter "$numero" "(rubrique Prérequis)" "ticket" "non déclaré, à confirmer" "$STRICT"
  fi
}

if [ -n "$CORPS" ]; then
  traiter "${NUMERO:-?}" "$(cat "$CORPS")"
else
  if [ "$TOUS" -eq 1 ]; then
    while IFS= read -r n; do
      [ -n "$n" ] && tickets+=("$n")
    done < <(gh issue list --repo "$DEPOT" --state open --limit 50 --json number --jq '.[].number' 2>/dev/null)
  fi
  for n in "${tickets[@]}"; do
    traiter "$n" "$(corps_de "$n")"
  done
fi

echo "Pré-vol des blocages (noms seulement, aucune valeur lue)"
if [ "${#lignes[@]}" -eq 0 ]; then
  echo "Aucun prérequis à vérifier."
  echo "Rappel : « Prérequis : aucun » vaut déclaration. Un ticket sans rubrique ne déclare rien, et le pré-vol ne devine pas."
  exit 0
fi

echo
printf '| %-6s | %-38s | %-14s | %s |\n' "Ticket" "Prérequis" "Où" "État"
printf '| %-6s | %-38s | %-14s | %s |\n' "------" "--------------------------------------" "--------------" "--------------------------"
for l in "${lignes[@]}"; do
  printf '%s\n' "$l"
done
echo

if [ "$blocages" -gt 0 ]; then
  echo "Blocages à régler avant de lancer : $blocages."
  exit 1
fi
echo "Aucun blocage certain. Relisez les lignes « à confirmer »."
exit 0
