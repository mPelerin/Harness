# Dépôt GitHub du cadrage

## Initialisation au premier entretien

Après confirmation du nom et du compte, intervenir sur accord explicite.

- Créer le dépôt privé hors du vault, avec README et les modèles d’issue et de PR de
  `template-projet/.github/`. Pousser le premier commit sur `main`, puis créer et
  pousser `preprod` depuis ce commit. Vérifier que la branche par défaut est `main`.
- Créer un GitHub Project privé avec `gh project create --owner <compte> --title <nom>`,
  puis `gh project link <numéro> --owner <compte> --repo <compte>/<dépôt>`.
  Noter immédiatement son URL et son numéro dans Pilotage et renseigner `depot`
  dans la note projet. Si interrompu, retrouver le dépôt et le Project existants
  avant de poursuivre. Une permission Projects manquante est signalée.
- Inclure le workflow `methode/controles-depot.yml` sous `.github/workflows/`
  avant le premier push. Vérifier le résultat dans Actions. Le ticket socle ajoutera
  ensuite les tests de l’application selon la pile choisie.
- Prévoir une vue Tableau par statut et une vue Liste par priorité dans le Project.
  Vérifier les vues disponibles dans GitHub avant d’annoncer leur création.

Preuve : URL du dépôt, branches distantes, Project lié et résultat du contrôle.

## Finaliser le dépôt de cadrage

Intervenir après le feu vert écrit de la porte 1.

Si le dépôt existe depuis le premier entretien,
reprendre sa branche `preprod` dans `BASE`, compléter les fichiers ci-dessous et
pousser seulement le cadrage. Réutiliser son Project et ses branches. Les commandes
de création qui suivent concernent uniquement un dépôt encore absent :
```bash
BASE="$HOME/.local/share/harness/depots/$NOM"
COMPTE=$(sed -n 's/^COMPTE_GITHUB=//p' ~/.config/harness/harness.conf | tail -n 1)
mkdir -p "$BASE" && cp -r "$PROJET/." "$BASE/" && rm -f "$BASE/$NOM - GitHub.md"
cd "$BASE" && git init -b main && mkdir -p code && touch code/.gitkeep
```
Écrire à la racine :
- `README.md` : la phrase du projet, et "les documents sont les notes de ce dossier".
- `.gitignore` : `<Nom> - GitHub.md`, `.env*` (sauf `.env.example`), et selon le type
  d'appli `code/node_modules/` et `code/.next/` (web), `code/build/` et
  `code/.gradle/` (Android).
- `AGENTS.md`, ce squelette exact, chaque `<...>` rempli depuis les notes :
  `# <Nom>` ; `## Projet` (la phrase) ; `## Utilisateurs` ; `## Où sont les documents`
  (un lien par section `01` à `09`) ; `## Commandes de vérification` ("à définir :
  ticket socle") ; `## Règles métier critiques` (depuis Critères d'acceptation) ;
  `## Pièges connus` ("aucun pour l'instant").
- `CLAUDE.md` : une ligne, `@AGENTS.md`.
Contrôle, qui ne doit rien afficher :
`awk '/<!--/{c=1} {print (c ? "" : $0)} /-->/{c=0}' AGENTS.md | grep -nE '<[^>]+>'`
Puis `git add -- .` (le `.gitignore` fait le tri, vérifié par `git status --short`),
commit "Premier commit : notes du cadrage, AGENTS.md, README",
`gh repo create "$COMPTE/<dépôt>" --private --source=. --push`,
`gh repo view "$COMPTE/<dépôt>" --json defaultBranchRef` affiche `main`,
`git switch -c preprod && git push -u origin preprod`.
Écrire `depot: <compte>/<dépôt>` dans la note projet du vault. Le service mémoire du
serveur rattache alors le dossier du vault à ce dépôt.
Preuve : l'adresse, `git ls-remote origin preprod` égal à `git rev-parse HEAD`.
