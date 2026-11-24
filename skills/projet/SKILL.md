---
name: projet
description: Ouvre le classeur d'un nouveau projet dans le vault Projets, à partir du modèle _Modèles/Projet, et s'arrête. Toutes les notes existent dès le départ en statut a-faire. Porte aussi les règles communes à tous les skills du vault (situer le projet, où se fait Git, comment écrire une note). À utiliser quand l'utilisateur dit "nouveau projet", emploie "projet" suivi d'un nom, dit "j'ai une idée de projet", "ouvre le classeur" ou "crée le projet". Ne pas utiliser pour remplir les notes (cadrage), créer le dépôt GitHub (cadrage) ni créer des tickets (tickets).
---

# Projet : ouvrir le classeur

## But

Créer le dossier complet du projet dans le vault, avec toutes ses notes vides.
Chaque note a sa place dès le premier jour, et un skill qui l'écrit (voir la carte
`CARTE-SKILLS-VAULT.md` du lot).

## Quand l'utiliser

- Une idée de projet neuve, même vague.
- Un autre skill renvoie ici pour les règles communes.

## Quand ne pas l'utiliser

- Le classeur existe : skill cadrage.
- Une petite fonction dans un projet existant : skill tickets, mode B.

## Règles communes à tous les skills du vault

**R1. Situer, sans chemin en dur.** Remonter jusqu'à la marque du vault :

```bash
D=$(pwd)
until [ -f "$D/_Méthode/Conventions.md" ] || [ "$D" = "/" ]; do D=$(dirname "$D"); done
test -f "$D/_Méthode/Conventions.md" || { echo "Lancez la commande depuis le vault Projets."; exit 1; }
VAULT="$D"
RESTE=$(realpath --relative-to="$VAULT" "$(pwd)")
[ "$RESTE" = "." ] || { NOM="${RESTE%%/*}"; PROJET="$VAULT/$NOM"; }
```

`PROJET` vide alors qu'un projet est attendu : **arrêt**, "placez-vous dans le dossier
du projet". Lire ensuite la note projet `<Nom>.md`, puis le `resume` des notes utiles.
Jamais tout le vault, jamais tout un projet.

**R2. Le dépôt Git est le dossier du projet.** Il contient les notes et `code/`.
Les commandes de l'appli (installation, tests) se lancent dans `code/`. Les commandes
`git` et `gh` se lancent à la racine du dépôt.
`<Nom> - GitHub.md` est généré et jamais versionné.

**R3. Un seul dépôt Git par machine, jamais deux écrivains.** La synchro du vault
n'emporte pas `.git`. Le dossier du vault n'a de `.git` que sur le serveur, où il reste
sur `preprod`. Donc :

```bash
DEPOT=$(sed -n 's/^depot: *"*\([^"]*\)"*$/\1/p' "$PROJET/$NOM.md")
if [ -d "$PROJET/.git" ]; then BASE="$PROJET"
else BASE="$HOME/.local/share/harness/depots/$NOM"
  [ -d "$BASE/.git" ] || gh repo clone "$DEPOT" "$BASE"
fi
git -C "$BASE" fetch origin
```

- Un ticket se travaille dans un **worktree**, un second dossier de travail du même
  dépôt, hors du vault : `ARBRE="$HOME/.local/share/harness/worktrees/$NOM/<branche>"`.
  La note du ticket s'y écrit, et part dans le commit du ticket.
- Une note hors ticket (cadrage, compte rendu, décision, parking) s'écrit dans le vault.
  Le service mémoire du serveur la commite sur `preprod`, notes seulement.
- Juste après une fusion (livrer, preprod), la note se met à jour dans `BASE` par un
  **commit mémoire** sur `preprod`, notes seulement :
  ```bash
  git -C "$BASE" switch preprod && git -C "$BASE" pull --ff-only
  # écrire la note dans $BASE, puis :
  git -C "$BASE" add -- "<chemin de la note>"
  git -C "$BASE" diff --cached --name-only | grep -E '^(code/|\.github/)' && exit 1
  git -C "$BASE" commit -m "Mémoire : <ce qui change>" && git -C "$BASE" push origin preprod
  ```
  Jamais de code sur `preprod` hors fusion. Push refusé : `pull --rebase`, puis réessayer
  une fois ; sinon arrêt.

**R4. Écrire une note.** Toujours copiée d'un modèle (`_Modèles/Notes` ou le classeur),
jamais réinventée. Copier le corps seulement quand le modèle est une méthode (Fiche QA).
Propriétés des conventions, avec `source` (la note parente) à la place de `precedent`.
Les notes du classeur reçoivent leur `source` du modèle (`scripts/vault/structure.py`), jamais
d'un renommage automatique : `precedent` dit la note d'avant, pas la note parente.
Statuts d'une note : `a-faire`, `brouillon`, `valide`, `obsolete`. Statuts d'un ticket :
`a-faire`, `en-cours`, `en-revue`, `valide`, `obsolete`.
Une information vit à un seul endroit : lier la note d'origine, ne pas recopier.
À chaque écriture, retirer les commentaires de rédaction hérités du modèle dans les
rubriques qui viennent d'être remplies. Laisser les consignes des rubriques encore
vides, les annotations ajoutées par l'utilisateur et les marqueurs automatiques.
Exemple : sous « Entretiens menés », retirer « Une note par entretien… » dès que
le premier lien d'entretien est ajouté. Le modèle conserve ses consignes.

**R5. Les portes.** `_Méthode/Portes.md` donne les cases de chaque porte. À une porte,
citer les cases qu'on ne peut pas cocher. Une case vide = on n'ouvre pas.

**R6. Une idée hors sujet** va en fin de `_Méthode/Parking à idées.md`, datée. Seul
l'utilisateur tranche.

## Étapes

1. **Situer** (R1), depuis la racine du vault. Preuve : le chemin de `VAULT`.

2. **Demander le nom**, une seule question. Lettres, chiffres, tirets et espaces.
   Jamais `#`, `^`, `[`, `]`, `|`, `/`, `&`, `\`. `<vault>/<Nom>` ne doit pas exister.
   Preuve : `test ! -e "$VAULT/$NOM" && echo libre`.

3. **Créer le classeur avec le générateur du moteur**, qui suit `scripts/vault/structure.py` :
   ```bash
   HARNESS=$(dirname "$(dirname "$(readlink -f ~/.claude/skills/projet)")")
   VAULT_PROJETS="$VAULT" python3 "$HARNESS/scripts/vault/vault_projets.py" nouveau "$NOM"
   ```
   Générateur absent : copier le modèle et renommer, à la main.
   ```bash
   cp -r "$VAULT/_Modèles/Projet" "$VAULT/$NOM" && cd "$VAULT/$NOM"
   find . -name "PROJET*" -type f | while read -r f; do mv "$f" "${f//PROJET/$NOM}"; done
   grep -rl "PROJET" --include="*.md" . | while read -r f; do sed -i "s/PROJET/$NOM/g" "$f"; done
   ```
   Arrêt si `_Modèles/Projet` manque : le modèle a bougé, ne rien improviser.

4. **Contrôler.** `grep -rn "PROJET" "$VAULT/$NOM"` n'affiche rien, et
   `VAULT_PROJETS="$VAULT" python3 "$HARNESS/scripts/vault/vault_projets.py" verifier "$VAULT/$NOM"`
   ne signale ni lien cassé ni propriété manquante. Preuve : les deux sorties.

5. **Remplir la note projet.** `phase: discovery`, `depot: ""`, `prod: ""`,
   `preprod: ""`. Jamais `avancement` : il est calculé dans `<Nom> - GitHub`.
   `resume` : une phrase dictée par l'utilisateur, le problème, pour qui, ce que ça
   change. Elle alimente le tableau de bord. Preuve : la note relue.

6. **Montrer le classeur. POINT D'ARRÊT.** Les 9 sections, le nombre de notes, la
   phrase. Preuve : `find "$VAULT/$NOM" -name "*.md" | sort`.

7. **Passer la main.** Donner le prompt à copier dans une nouvelle conversation :
   `Projet <nom>. Dossier <chemin absolu>. Lancez le skill cadrage pour Discovery.
   Lisez <chemin de la note projet>, puis <chemin de 01 Discovery/agent.md>
   avant de reformuler l'idée.
   Utilisez le skill Visualize, s'il est disponible, pour le questionnaire dans
   le chat avec un seul bouton de validation.`

## Point d'arrêt

- Étape 6 : rien n'est validé sans la relecture de l'utilisateur.
- Le nom ne change plus après coup sans refaire l'étape 4.

## Preuve attendue

Le chemin du classeur, le contrôle de l'étape 4 vide, la phrase du projet.

## Interdits

- Remplir les notes : c'est le skill cadrage.
- Créer le dépôt GitHub, créer des tickets.
- Toucher à `_Modèles/`, `_Méthode/`, `_À trier/` ou aux blocs entre
  `<!-- debut:auto -->` et `<!-- fin:auto -->`.
- Écrire la phrase du projet à la place de l'utilisateur.
- Inventer une note absente du modèle.
- Lancer `git` dans le dossier du vault sur une machine où il n'a pas de `.git` (R3).
