#!/usr/bin/env bash
# orchestrateur.sh : dépose une demande chez l'orchestrateur, puis suit la carte.
# Ne code rien, ne fusionne rien, n'affiche aucun secret.
# Aucune valeur personnelle ici : tout vient de ~/.config/harness/harness.conf.
#
# Usage :
#   orchestrateur.sh deposer-demande --ticket N --depot compte/depot --titre "..." --corps FICHIER
#   orchestrateur.sh etat CARTE
#   orchestrateur.sh suivre CARTE --depot compte/depot --ticket N [--interval 120] [--max 14400]
#
# Codes de sortie :
#   0  la carte est finie
#   1  erreur de commande ou réponse illisible
#   3  ORCHESTRATEUR vide : pas de délégation
#   4  carte bloquée ou archivée
#   5  délai dépassé, la carte travaille encore
#   6  la demande est finie sans carte de code (aucune carte enfant)

set -uo pipefail

CONF="${HARNESS_CONF:-$HOME/.config/harness/harness.conf}"

lire_conf() {
  [ -f "$CONF" ] && sed -n "s/^$1=//p" "$CONF" | tail -n 1
}

ORCH="$(lire_conf ORCHESTRATEUR)"
HOTE="$(lire_conf HOTE_SSH_SERVEUR)"

# Cite un texte pour un shell, apostrophes comprises.
citer() {
  printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"
}

exiger_orchestrateur() {
  if [ -z "$ORCH" ]; then
    echo "Arrêt : ORCHESTRATEUR est vide dans $CONF. Le codage se fait ici, sans délégation." >&2
    exit 3
  fi
  if [ -n "$HOTE" ]; then
    command -v ssh >/dev/null 2>&1 || { echo "Arrêt : ssh est absent." >&2; exit 1; }
    command -v gh >/dev/null 2>&1 || { echo "Arrêt : gh est absent." >&2; exit 1; }
  else
    command -v "$ORCH" >/dev/null 2>&1 || { echo "Arrêt : commande $ORCH absente, et HOTE_SSH_SERVEUR est vide." >&2; exit 1; }
  fi
}

# Lance une commande chez l'orchestrateur. L'entrée standard est transmise telle quelle.
# $1 : arguments déjà cités, sans le nom de l'outil.
chez_orchestrateur() {
  local commande="$1"
  if [ -n "$HOTE" ]; then
    ssh -o BatchMode=yes "$HOTE" "sudo -n -i $(citer "$ORCH") $commande"
  else
    bash -c "$(citer "$ORCH") $commande"
  fi
}

# Première valeur d'un champ simple du JSON d'une carte.
champ() {
  printf '%s\n' "$1" | sed -n "s/^[[:space:]]*\"$2\": \"\([^\"]*\)\".*/\1/p" | head -n 1
}

json_carte() {
  chez_orchestrateur "kanban show --json $(citer "$1")"
}

# Identifiants des cartes enfants, dans l'ordre du JSON.
enfants() {
  printf '%s\n' "$1" \
    | awk '/"children":/{f=1;next} f&&/\]/{exit} f{print}' \
    | grep -oE 't_[0-9a-f]{6,}' || true
}

cmd_deposer() {
  local ticket="" depot="" titre="" corps=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --ticket) ticket="${2:-}"; shift 2 ;;
      --depot)  depot="${2:-}";  shift 2 ;;
      --titre)  titre="${2:-}";  shift 2 ;;
      --corps)  corps="${2:-}";  shift 2 ;;
      *) echo "Option inconnue : $1" >&2; exit 2 ;;
    esac
  done
  [ -n "$ticket" ] && [ -n "$depot" ] && [ -n "$titre" ] && [ -n "$corps" ] || {
    echo "Usage : orchestrateur.sh deposer-demande --ticket N --depot compte/depot --titre \"...\" --corps FICHIER" >&2
    exit 2
  }
  [ -f "$corps" ] || { echo "Arrêt : corps introuvable : $corps" >&2; exit 1; }

  local cle sortie id
  cle="feature-$(printf '%s' "$depot" | tr '/' '-')-$ticket-$(date +%F)"
  sortie="$(chez_orchestrateur "kanban create --json --assignee orchestrator --idempotency-key $(citer "$cle") --body-file - $(citer "$titre")" < "$corps")" || {
    echo "Arrêt : le dépôt de la demande a échoué." >&2
    printf '%s\n' "$sortie" >&2
    exit 1
  }
  id="$(printf '%s\n' "$sortie" | grep -oE 't_[0-9a-f]{6,}' | head -n 1)"
  [ -n "$id" ] || {
    echo "Arrêt : aucun identifiant de carte dans la réponse." >&2
    printf '%s\n' "$sortie" >&2
    exit 1
  }
  printf '%s\n' "$id"
}

cmd_etat() {
  [ $# -ge 1 ] || { echo "Usage : orchestrateur.sh etat CARTE" >&2; exit 2; }
  local statut
  statut="$(champ "$(json_carte "$1")" status)"
  printf '%s\n' "${statut:-inconnu}"
}

# Cherche la demande de fusion dont la branche commence par "<ticket>-".
demande_fusion() {
  local depot="$1" ticket="$2" sortie
  [ -n "$depot" ] || return 0
  sortie="$(gh pr list --repo "$depot" --state all --limit 50 \
    --json number,headRefName \
    --jq ".[] | select(.headRefName | startswith(\"$ticket-\")) | .number" 2>/dev/null | tail -n 1)"
  printf '%s' "$sortie"
}

etat_ci() {
  local depot="$1" pr="$2" sortie code
  [ -n "$pr" ] || { printf 'absente'; return 0; }
  sortie="$(gh pr checks "$pr" --repo "$depot" 2>&1)"
  code=$?
  if [ "$code" -eq 0 ]; then
    printf 'verte'
  elif [ "$code" -eq 8 ]; then
    printf 'en cours'
  elif printf '%s' "$sortie" | grep -qi 'no checks'; then
    printf 'absente'
  else
    printf 'rouge'
  fi
}

cmd_suivre() {
  local carte="" depot="" ticket="" interval=120 max=14400
  while [ $# -gt 0 ]; do
    case "$1" in
      --depot)    depot="${2:-}";    shift 2 ;;
      --ticket)   ticket="${2:-}";   shift 2 ;;
      --interval) interval="${2:-120}"; shift 2 ;;
      --max)      max="${2:-14400}"; shift 2 ;;
      -*) echo "Option inconnue : $1" >&2; exit 2 ;;
      *)  carte="$1"; shift ;;
    esac
  done
  [ -n "$carte" ] || { echo "Usage : orchestrateur.sh suivre CARTE --depot compte/depot --ticket N" >&2; exit 2; }

  local debut=$SECONDS cible="$carte" json statut agent enfant pr pr_ci
  while :; do
    json="$(json_carte "$cible")"
    statut="$(champ "$json" status)"

    case "$statut" in
      done)
        if [ "$cible" = "$carte" ]; then
          enfant="$(enfants "$json" | tail -n 1)"
          if [ -n "$enfant" ] && [ "$enfant" != "$carte" ]; then
            cible="$enfant"
            continue
          fi
          printf 'ticket=%s carte=%s agent=orchestrator etat=sans_carte demande_fusion=absente ci=absente\n' \
            "${ticket:-?}" "$carte"
          exit 6
        fi
        agent="$(champ "$json" assignee)"
        pr="$(demande_fusion "$depot" "$ticket")"
        pr_ci="$(etat_ci "$depot" "$pr")"
        printf 'ticket=%s carte=%s agent=%s etat=done demande_fusion=%s ci=%s\n' \
          "${ticket:-?}" "$cible" "${agent:-?}" "${pr:-absente}" "$pr_ci"
        exit 0
        ;;
      blocked|archived)
        agent="$(champ "$json" assignee)"
        printf 'ticket=%s carte=%s agent=%s etat=%s demande_fusion=absente ci=absente\n' \
          "${ticket:-?}" "$cible" "${agent:-?}" "$statut"
        exit 4
        ;;
      todo|ready|running|review|scheduled) ;;
    esac

    if [ $((SECONDS - debut)) -gt "$max" ]; then
      printf 'ticket=%s carte=%s agent=? etat=en_cours demande_fusion=absente ci=absente\n' \
        "${ticket:-?}" "$cible"
      exit 5
    fi
    sleep "$interval"
  done
}

case "${1:-}" in
  deposer-demande) shift; exiger_orchestrateur; cmd_deposer "$@" ;;
  etat)            shift; exiger_orchestrateur; cmd_etat "$@" ;;
  suivre)          shift; exiger_orchestrateur; cmd_suivre "$@" ;;
  -h|--aide|"")
    awk 'NR>1 && /^#/ {sub(/^# ?/, ""); print; next} NR>1 {exit}' "${BASH_SOURCE[0]}"
    ;;
  *) echo "Ordre inconnu : $1" >&2; echo "Ordres : deposer-demande, etat, suivre" >&2; exit 2 ;;
esac
