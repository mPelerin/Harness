#!/usr/bin/env bash
# nouveau-projet.sh : crée un projet Next.js à partir du gabarit du harness.
#
# Ce qu'il fait, depuis la racine du vault des projets (le dossier qui contient _Méthode/) :
#   0. crée la mémoire du projet, <nom>/ (notes du vault), avec scripts/vault/vault_projets.py ;
#   1. crée l'appli dans <nom>/code avec le générateur officiel de Next.js (version fixée) ;
#   2. pose par-dessus le socle (template-projet/), le profil (profils/nextjs/) et les MCP (mcp/) ;
#   3. installe Prettier, Vitest et Lefthook (versions fixées) ;
#   4. fixe toutes les versions, active les hooks Git, fait le premier commit ;
#   5. lance la vérification complète et affiche le résultat.
#
# Ce qu'il garantit :
#   - il ne touche à rien en dehors du dossier <nom>/ ;
#   - il s'arrête si <nom>/code existe déjà ; des notes déjà présentes dans <nom>/ sont gardées.
#
# Usage : nouveau-projet <nom>      exemple : nouveau-projet mon-appli

set -euo pipefail

# Versions fixées. Pour les faire évoluer : changer ici, tester sur un projet d'essai.
V_NEXT="16.4.6"
V_PRETTIER="3.10.1"
V_VITEST="5.1.0"
V_LEFTHOOK="2.2.2"
V_NODE="24"   # même version majeure que .nvmrc et que Node sur le PC

NOM="${1:-}"
if [ -z "$NOM" ] || [ "$NOM" = "-h" ] || [ "$NOM" = "--aide" ]; then
  echo "Usage : nouveau-projet <nom>"
  echo "  Le nom s'écrit en minuscules, chiffres et tirets. Exemple : mon-appli"
  exit 2
fi
if ! printf '%s' "$NOM" | grep -Eq '^[a-z0-9][a-z0-9-]*$'; then
  echo "Arrêt : nom refusé. Minuscules, chiffres et tirets seulement. Exemple : mon-appli" >&2
  exit 2
fi
if [ "$(id -u)" -eq 0 ]; then
  echo "Arrêt : ne lancez pas ce script avec sudo ni en root." >&2
  exit 1
fi
for outil in node npm npx git; do
  command -v "$outil" >/dev/null || { echo "Arrêt : $outil est introuvable." >&2; exit 1; }
done

# Emplacement du dépôt harness : le dossier parent de scripts/ (le lien symbolique est suivi).
DOSSIER_SCRIPT="$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)"
DEPOT="$(cd -- "$DOSSIER_SCRIPT/.." && pwd -P)"
SOCLE="$DEPOT/template-projet"
PROFIL="$DEPOT/profils/nextjs"
[ -d "$SOCLE" ] && [ -d "$PROFIL" ] || { echo "Arrêt : gabarit introuvable dans $DEPOT." >&2; exit 1; }

if [ ! -d "$PWD/_Méthode" ]; then
  echo "Arrêt : lancez ce script depuis la racine du vault des projets (le dossier qui contient _Méthode/)." >&2
  exit 1
fi
command -v python3 >/dev/null || { echo "Arrêt : python3 est introuvable." >&2; exit 1; }
PROJET="$PWD/$NOM"
CIBLE="$PROJET/code"
if [ -e "$CIBLE" ]; then
  echo "Arrêt : $CIBLE existe déjà. Rien n'a été modifié." >&2
  exit 1
fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Arrêt : vous êtes dans un dépôt Git. Placez-vous dans un dossier qui n'en est pas un." >&2
  exit 1
fi

echo "0/5 Mémoire du projet dans le vault"
if [ -f "$PROJET/$NOM.md" ]; then
  VAULT_PROJETS="$PWD" python3 "$DEPOT/scripts/vault/vault_projets.py" completer "$NOM"
else
  VAULT_PROJETS="$PWD" python3 "$DEPOT/scripts/vault/vault_projets.py" nouveau "$NOM"
fi

echo "1/5 Création de l'appli Next.js $V_NEXT"
cd -- "$PROJET"
npx --yes "create-next-app@$V_NEXT" code \
  --ts --eslint --app --src-dir --tailwind --use-npm \
  --import-alias "@/*" --disable-git --yes
cd -- "$CIBLE"
npm pkg set name="$NOM"

echo "2/5 Pose du socle et du profil"
cp -- .gitignore .gitignore.next
cp -r -- "$SOCLE/." .
cp -r -- "$PROFIL/." .
cp -- "$DEPOT/mcp/claude/projet.mcp.json" .mcp.json
cp -- "$DEPOT/mcp/opencode/opencode.json" opencode.json
mv -- .gitignore.next .gitignore
printf '\n# Captures et journaux de Playwright MCP\n.playwright-mcp/\n' >> .gitignore
printf '\n# Le modèle des variables, lui, entre dans le dépôt\n!.env.example\n' >> .gitignore
cat > README.md <<FIN
# $NOM

Projet créé avec le gabarit du harness. Les règles pour les agents sont dans \`AGENTS.md\`.

\`\`\`bash
npm run dev        # lancer en local
npm run verifier   # tout contrôler d'un coup
\`\`\`

## Après un clone sur un autre PC

\`\`\`bash
npm ci && npx lefthook install
\`\`\`

La seconde commande active les hooks Git, c'est-à-dire les contrôles lancés avant chaque commit et chaque push.
Sans elle, ils ne tournent pas sur un dépôt cloné.
FIN

# Remplit la rubrique "Commandes de vérification" de AGENTS.md, pour que les agents la trouvent sans demander.
sed -i \
  -e "s|^<commande d'installation>  |npm ci                    |" \
  -e "s|^<commande de lancement>    |npm run dev               |" \
  -e "s|^<commande de vérification> |npm run verifier          |" \
  AGENTS.md
if grep -q '^<commande' AGENTS.md || ! grep -q '^npm run verifier ' AGENTS.md; then
  echo "Arrêt : la rubrique des commandes de AGENTS.md n'a pas pu être remplie." >&2
  exit 1
fi

echo "3/5 Installation de Prettier, Vitest, Lefthook et des types de Node $V_NODE"
npm install --save-dev --save-exact \
  "prettier@$V_PRETTIER" "vitest@$V_VITEST" "lefthook@$V_LEFTHOOK" \
  "@types/node@$V_NODE"

echo "4/5 Versions fixées, hooks, premier commit"
npm pkg set \
  scripts.format="prettier --write ." \
  scripts.format:check="prettier --check ." \
  scripts.typecheck="tsc --noEmit" \
  scripts.test="vitest run" \
  scripts.verifier="npm run lint && npm run format:check && npm run test && npm run build && npm run typecheck"
# Remplace chaque plage de versions (ex. ^5) par la version réellement installée.
node -e '
const fs = require("fs");
const p = JSON.parse(fs.readFileSync("package.json", "utf8"));
for (const groupe of ["dependencies", "devDependencies"]) {
  for (const nom of Object.keys(p[groupe] || {})) {
    p[groupe][nom] = JSON.parse(fs.readFileSync("node_modules/" + nom + "/package.json", "utf8")).version;
  }
}
fs.writeFileSync("package.json", JSON.stringify(p, null, 2) + "\n");
'
npm install
npx prettier --write . >/dev/null
git init -q -b main
npx lefthook install
git add .
git commit -q -m "Premier commit : gabarit du harness"

echo "5/5 Vérification complète"
npm run verifier

echo
echo "OK : projet créé dans $CIBLE"
echo "Notes du projet : $PROJET (vault). Code : $CIBLE."
echo "Le reste de AGENTS.md sera rempli par le skill cadrage. D'abord, relier le dépôt GitHub :"
echo "  git remote add origin git@github.com:<compte>/$NOM.git && git push -u origin main"
