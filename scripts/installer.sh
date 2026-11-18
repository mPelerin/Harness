#!/usr/bin/env bash
# installer.sh : branche les agents sur le harness, en deux couches.
#
# Couche 1, le moteur (ce dépôt) : règles communes, skills, gabarit, commande nouveau-projet.
# Couche 2, l'instance de l'utilisateur : un dossier config/ dans son dépôt privé, avec
#   harness.conf (PRENOM, ... sans secret), profil.md (sa façon de travailler), et à côté
#   un dossier skills/ pour ses skills perso. Ce dossier est relié en ~/.config/harness.
#
# Ce qu'il fait :
#   - config  : ~/.config/harness -> le dossier config/ de l'instance (option --config) ;
#   - règles  : génère AGENTS.md = règles du moteur + profil de l'instance, puis
#               ~/.claude/CLAUDE.md et ~/.config/opencode/AGENTS.md -> ce fichier généré ;
#   - skills  : un lien par skill du moteur, puis un par skill de l'instance, dans ~/.claude/skills/ ;
#   - commandes : ~/.local/bin/nouveau-projet -> scripts/nouveau-projet.sh du moteur,
#                 ~/.local/bin/orchestrateur -> scripts/orchestrateur.sh du moteur,
#                 ~/.local/bin/pre-vol -> scripts/pre-vol.sh du moteur.
#
# Ce qu'il garantit :
#   - il ne supprime jamais rien : ce qui occupe la place d'un lien part dans une sauvegarde datée ;
#   - on peut le relancer sans dégât ; sans instance, il installe le moteur seul ;
#   - il lit harness.conf sans l'exécuter.
#
# Usage :
#   bash scripts/installer.sh [--essai] [--config <dossier config de l'instance>]
#   bash scripts/installer.sh --agents     affiche le AGENTS.md qui serait généré, sans rien changer

set -euo pipefail

aide() {
  echo "Usage : bash scripts/installer.sh [--essai] [--config <dossier>]"
  echo "        bash scripts/installer.sh --agents"
  echo "  --essai    montre ce qui serait fait, sans rien changer"
  echo "  --config   dossier config/ de votre instance, relié en ~/.config/harness"
  echo "  --agents   affiche le AGENTS.md généré, sans rien changer"
}

ESSAI=0
AFFICHER_AGENTS=0
CONFIG_SOURCE=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --essai) ESSAI=1 ;;
    --agents) AFFICHER_AGENTS=1 ;;
    --config)
      [ "$#" -ge 2 ] || { echo "Option --config sans dossier." >&2; exit 2; }
      CONFIG_SOURCE="$2"; shift ;;
    -h|--aide) aide; exit 0 ;;
    *) echo "Option inconnue : $1" >&2; aide >&2; exit 2 ;;
  esac
  shift
done

if [ "$(id -u)" -eq 0 ]; then
  echo "Arrêt : ne lancez pas ce script avec sudo ni en root." >&2
  exit 1
fi

DOSSIER_SCRIPT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DEPOT="$(cd -- "$DOSSIER_SCRIPT/.." && pwd -P)"
CONFIG="$HOME/.config/harness"
CLAUDE="$HOME/.claude"
OPENCODE="$HOME/.config/opencode"
GENERE="${XDG_STATE_HOME:-$HOME/.local/state}/harness/AGENTS.md"

if [ ! -f "$DEPOT/AGENTS.md" ]; then
  echo "Arrêt : AGENTS.md introuvable dans $DEPOT. Ce script doit rester dans le dossier scripts/ du dépôt." >&2
  exit 1
fi

if [ -n "$CONFIG_SOURCE" ]; then
  [ -d "$CONFIG_SOURCE" ] || { echo "Arrêt : le dossier $CONFIG_SOURCE n'existe pas." >&2; exit 1; }
  CONFIG_SOURCE="$(cd -- "$CONFIG_SOURCE" && pwd -P)"
  case "$CONFIG_SOURCE/" in
    "$DEPOT"/*) echo "Arrêt : la config de l'instance ne doit pas être dans le moteur ($DEPOT)." >&2; exit 1 ;;
  esac
fi
# Dossier config lu : celui donné par --config, sinon ~/.config/harness.
CONF_LUE="${CONFIG_SOURCE:-$CONFIG}"

# Lit une valeur de harness.conf, sans exécuter le fichier. Vide si absente.
lire_conf() {
  local fichier="$CONF_LUE/harness.conf"
  [ -f "$fichier" ] || return 0
  sed -n "s/^$1=//p" "$fichier" | tail -n 1 | sed 's/[[:space:]]*$//; s/^"\(.*\)"$/\1/'
}

# Écrit sur la sortie le AGENTS.md généré : règles du moteur, puis profil de l'instance.
generer_agents() {
  local prenom
  prenom="$(lire_conf PRENOM)"
  echo "<!-- Fichier généré par installer.sh du harness. Ne pas le modifier : il est réécrit à chaque installation. -->"
  echo "<!-- Pour changer les règles : AGENTS.md du harness. Pour changer le profil : profil.md de l'instance. -->"
  echo
  cat -- "$DEPOT/AGENTS.md"
  if [ -f "$CONF_LUE/profil.md" ]; then
    echo
    if [ -n "$prenom" ]; then
      echo "# Profil de l'utilisateur : $prenom"
      echo
      echo "L'utilisateur s'appelle $prenom. Partout où les règles et les skills disent \"l'utilisateur\", c'est $prenom."
    else
      echo "# Profil de l'utilisateur"
    fi
    echo
    cat -- "$CONF_LUE/profil.md"
  fi
}

if [ "$AFFICHER_AGENTS" -eq 1 ]; then
  generer_agents
  exit 0
fi

crees=0
deja_bons=0
sauvegardes=0
# Dossier de sauvegarde : DOSSIER_SAUVEGARDES de harness.conf, sinon le dossier par défaut.
dossier="$(lire_conf DOSSIER_SAUVEGARDES)"
dossier="${dossier/#\~/$HOME}"
SAUVEGARDE="${dossier:-$HOME/.local/state/harness/sauvegardes}/$(date +%Y-%m-%d_%H%M%S)"

# Déplace ce qui occupe la place d'un lien vers la sauvegarde datée.
sauvegarder() {
  local chose="$1"
  local relatif="${chose#"$HOME"/}"
  local destination="$SAUVEGARDE/$relatif"
  if [ "$ESSAI" -eq 1 ]; then
    echo "  [essai] déplacerait $chose vers $destination"
  else
    mkdir -p -- "$(dirname -- "$destination")"
    mv -n -- "$chose" "$destination"
    if [ -e "$chose" ] || [ -L "$chose" ]; then
      echo "Arrêt : impossible de mettre $chose de côté. Rien d'autre n'a été modifié à cet endroit." >&2
      exit 1
    fi
    echo "  [sauvegardé] $chose -> $destination"
  fi
  sauvegardes=$((sauvegardes + 1))
}

# Crée le lien "lien" vers "cible". Ne fait rien s'il est déjà bon.
# La cible doit exister : un lien qui pointe dans le vide n'est jamais "déjà bon".
relier() {
  local cible="$1"
  local lien="$2"
  if [ -L "$lien" ] && [ -e "$lien" ] && [ "$(readlink -- "$lien")" = "$cible" ]; then
    echo "  [déjà bon] $lien"
    deja_bons=$((deja_bons + 1))
    return 0
  fi
  if [ -e "$lien" ] || [ -L "$lien" ]; then
    sauvegarder "$lien"
  fi
  if [ "$ESSAI" -eq 1 ]; then
    echo "  [essai] créerait $lien -> $cible"
  else
    mkdir -p -- "$(dirname -- "$lien")"
    ln -sT -- "$cible" "$lien"
    echo "  [créé] $lien -> $cible"
  fi
  crees=$((crees + 1))
}

echo "Moteur harness : $DEPOT"
[ "$ESSAI" -eq 1 ] && echo "MODE ESSAI : rien ne sera modifié."
echo

# ---------------------------------------------------------------- Instance
echo "Instance (~/.config/harness)"
[ -z "$CONFIG_SOURCE" ] || relier "$CONFIG_SOURCE" "$CONFIG"
INSTANCE=""
if [ -d "$CONF_LUE" ]; then
  INSTANCE="$(cd -- "$CONF_LUE/.." && pwd -P)"
  [ -f "$CONF_LUE/harness.conf" ] && echo "  [lu] harness.conf, prénom : $(lire_conf PRENOM)" || echo "  [rien] pas de harness.conf"
  [ -f "$CONF_LUE/profil.md" ] && echo "  [lu] profil.md" || echo "  [rien] pas de profil.md"
else
  echo "  [aucune] pas d'instance : moteur seul. Voir harness.conf.exemple."
fi
echo

# ---------------------------------------------------------------- Règles générées
echo "Règles générées : $GENERE"
if [ "$ESSAI" -eq 1 ]; then
  echo "  [essai] écrirait les règles du moteur$([ -f "$CONF_LUE/profil.md" ] && echo " et le profil de l'instance")"
else
  mkdir -p -- "$(dirname -- "$GENERE")"
  # Le profil peut être personnel : fichier lisible par l'utilisateur seul.
  ( umask 077; generer_agents > "$GENERE.tmp" ) && mv -f -- "$GENERE.tmp" "$GENERE"
  echo "  [écrit] $(wc -l < "$GENERE") lignes"
fi
echo

echo "Règles pour Claude Code"
if [ -d "$CLAUDE" ]; then
  relier "$GENERE" "$CLAUDE/CLAUDE.md"
else
  echo "  [ignoré] $CLAUDE n'existe pas : Claude Code n'est pas installé ici."
fi
echo

echo "Règles pour OpenCode"
if [ -d "$OPENCODE" ]; then
  relier "$GENERE" "$OPENCODE/AGENTS.md"
else
  echo "  [ignoré] $OPENCODE n'existe pas : OpenCode n'est pas installé ici."
fi
echo

# ---------------------------------------------------------------- Skills
# Les deux agents lisent ~/.claude/skills. Sans Claude Code, on passe par le dossier d'OpenCode.
if [ -d "$CLAUDE" ]; then
  DOSSIER_SKILLS="$CLAUDE/skills"
elif [ -d "$OPENCODE" ]; then
  DOSSIER_SKILLS="$OPENCODE/skills"
else
  DOSSIER_SKILLS=""
fi

relier_skills() {
  local source="$1"
  local trouve=0
  for dossier in "$source"/*/; do
    [ -f "${dossier}SKILL.md" ] || continue
    trouve=1
    relier "${dossier%/}" "$DOSSIER_SKILLS/$(basename -- "$dossier")"
  done
  [ "$trouve" -eq 1 ] || echo "  [rien] aucun skill dans $source"
}

echo "Skills du moteur"
if [ -z "$DOSSIER_SKILLS" ]; then
  echo "  [ignoré] aucun agent trouvé."
else
  relier_skills "$DEPOT/skills"
fi
echo

echo "Skills de l'instance"
if [ -z "$DOSSIER_SKILLS" ] || [ -z "$INSTANCE" ] || [ ! -d "$INSTANCE/skills" ]; then
  echo "  [aucun]"
else
  # Un skill perso ne remplace jamais un skill du moteur : sinon chaque passage échangerait les deux liens.
  for dossier in "$INSTANCE"/skills/*/; do
    nom="$(basename -- "$dossier")"
    if [ -d "$DEPOT/skills/$nom" ]; then
      echo "Arrêt : le skill $nom existe dans le moteur et dans l'instance. Renommez celui de l'instance." >&2
      exit 1
    fi
  done
  relier_skills "$INSTANCE/skills"
fi
echo

echo "Commandes du harness"
relier "$DEPOT/scripts/nouveau-projet.sh" "$HOME/.local/bin/nouveau-projet"
relier "$DEPOT/scripts/orchestrateur.sh" "$HOME/.local/bin/orchestrateur"
relier "$DEPOT/scripts/pre-vol.sh" "$HOME/.local/bin/pre-vol"
echo

echo "Bilan : $crees lien(s) à créer ou créés, $deja_bons déjà bon(s), $sauvegardes élément(s) mis de côté."
if [ "$sauvegardes" -gt 0 ] && [ "$ESSAI" -eq 0 ]; then
  echo "Sauvegarde : $SAUVEGARDE"
fi
if [ "$ESSAI" -eq 1 ]; then
  echo "C'était un essai. Relancez sans --essai pour installer."
else
  echo "Fermez puis rouvrez vos agents : ils lisent règles et skills au démarrage."
  echo "Après un changement de AGENTS.md ou de profil.md, relancez ce script : les règles sont générées."
fi
