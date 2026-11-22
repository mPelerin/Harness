---
name: cadrage
description: Remplit la mémoire du projet dans le vault, phase par phase (Discovery, Cadrage, Design, Conception), une phase par session, à partir des notes du classeur. À la fin, crée le dépôt GitHub à la racine du dossier projet (notes et code/), avec README, .gitignore et AGENTS.md, sans aucune bibliothèque, après le go de la porte 1. À utiliser quand l'utilisateur dit "cadrage", "cadre cette idée", "challenge mon idée", "continuer le cadrage", "écris le PRD" ou "on cadre le projet". Ne pas utiliser pour créer le classeur (projet), les tickets (tickets) ni coder (feature).
---

# Cadrage : remplir la mémoire, phase par phase

## But

Un projet cadré sans rien oublier. Les notes du classeur sont la référence. On les
remplit dans l'ordre, une phase par session. À la fin, le dépôt naît à la racine du
dossier projet : il emporte toutes les notes, et `code/` reste vide jusqu'au ticket socle.

## Quand l'utiliser

- Le classeur existe et des notes sont `a-faire`.
- Feature ou nuit renvoient ici parce que `AGENTS.md` a des trous `<...>` : étape 7
  seulement, sans nouvelle question.

## Quand ne pas l'utiliser

- Pas de classeur : skill projet.
- La note projet a `prod` rempli : le projet est en ligne. **Arrêt**, le cadrage d'une
  évolution n'est pas encore défini. Le dire.

## Les phases et qui écrit

Le champ `phase` de la note projet dit où reprendre. Chaque note porte un `agent` :
remplir la note avec le regard de ce rôle (ex. `cfo` pour Coûts : chiffres et seuil de
rentabilité). Sur Hermès, une carte par note, assignée à ce profil.

| Phase | Notes, dans l'ordre du modèle |
| --- | --- |
| 01 Discovery | Idée brute, Problème et opportunité, Utilisateurs et personas, Entretiens, Recherche et existant, Hypothèses et risques, Synthèse discovery |
| 02 Cadrage | Pilotage, PRD, Priorités, Stories, Contraintes techniques, Juridique et données, Coûts, Critères d'acceptation |
| 03 Design | Inspirations, Expérience (UX), Écrans et états, Identité visuelle (UI), Thèmes, Maquettes |
| 04 Conception | Architecture, Données, Sécurité, Specs, Plan de travail |

`a-faire` devient `brouillon` quand la note est remplie, `valide` quand l'utilisateur l'a
relue. Une note sans objet prend `obsolete`, avec la raison écrite dedans.

## Étapes

1. **Situer** (règle R1 du skill projet). Lire la note projet et le `resume` des notes de
   la phase. Lister celles qui sont `a-faire`, comme la vue `Documents à faire.base`.
   Preuve : le chemin, la phase, la liste des notes avec leur statut.

2. **Décider où on en est.** Phase complète quand toutes ses notes sont `valide` ou
   `obsolete` : passer à la suivante. Jamais deux phases dans la même session.
   Preuve : "phase X : n notes validées, m à faire".

3. **Au premier passage, reformuler l'idée** en deux phrases : qui, fait quoi, pour quel
   résultat. Attendre le "oui". Preuve : la reformulation et le "oui".

4. **Remplir les notes, une par une, dans l'ordre.** Lire la note, puis poser les
   questions qui manquent. Une question par message, choix courts, "Recommandé" en
   premier, la raison en une phrase. Après dix questions, proposer d'arrêter : le reste
   devient "Hypothèses". La note Idée brute s'écrit avec les mots de l'utilisateur.
   Livrables répétitifs, copiés de `_Modèles/Notes` :
   - Atelier : `<Nom> - Atelier AAAA-MM-JJ <sujet>` dans `01 Discovery/`.
   - Entretien : `<Nom> - Entretien AAAA-MM-JJ <rôle>` dans `01 Discovery/`, lié depuis
     Entretiens.
   - Décision lourde : `<Nom> - Décision AAAA-MM-JJ <sujet>` dans `07 Décisions/`,
     liée dans la colonne Détail du journal des décisions.
   Chaque réponse qui tranche : une ligne datée au journal des décisions.
   Preuve : chaque note remplie, passée à `brouillon`.

5. **Règles de contenu.** Les personnes sont des rôles ou des prénoms inventés, jamais de
   vraies personnes.
   - Discovery : sources datées, au moins trois opportunités dans l'arbre des
     opportunités (un problème en haut, une branche par piste), la synthèse dit "on y
     va, on change, ou on arrête".
   - Cadrage : le PRD reprend la synthèse et tient une rubrique "Retiré du périmètre",
     une ligne datée par retrait. Stories numérotées S1, S2, chacune avec des conditions
     vérifiables. **Pilotage** : les profils Hermès appelés, dans l'ordre, une raison par
     profil sauté ; l'orchestrateur le lit avant de répartir.
     **Contraintes techniques** : le type d'appli (landing, web, Android, Android et web,
     service sans écran) d'après les appareils des personas, puis la pile, chaque
     bibliothèque avec rôle, origine et version. Pas de pile par défaut. Le ticket
     socle l'installe, rien de plus. **Critères d'acceptation** : vérifiables par
     commande ou par geste ; ils deviennent les règles métier de `AGENTS.md`.
   - Design : sauter la phase si l'appli n'a pas d'écran, raison dans chaque note.
     Contrastes mesurés. Écrans et états liste les six états de chaque écran.
   - Conception : Architecture (frontières, modes de panne), Données (schéma, durée de
     conservation), Sécurité (points d'entrée, données sensibles : ce qui rendra un
     ticket `Sensible`), Specs (découpées en tâches), Plan de travail (lots,
     dépendances, chemin critique : le skill tickets en tire l'ordre).
   Preuve : les notes remplies, et les "sans objet" avec leur raison.

6. **Fin de session. POINT D'ARRÊT.** Montrer les notes, demander la relecture. Relue :
   `valide`. Phase complète : mettre `phase` à jour dans la note projet.
   Preuve : les statuts relus, la valeur de `phase`, et `vault_projets.py verifier <Nom>`
   (commande de l'étape 4 du skill projet) sans lien cassé.

7. **Conception complète : porte 1.** Montrer le récapitulatif (phrase, utilisateurs,
   nombre de stories, contraintes, points sensibles, retraits du périmètre) et les cases
   "Porte 1" de `_Méthode/Portes.md` encore vides. Puis : "Je crée le dépôt à la racine
   de `<Nom>`, avec les notes, README, .gitignore et AGENTS.md. Rien d'autre. Dites go."
   Sans ce go, rien ne se crée. Preuve : le récapitulatif, le "go" écrit.

8. **Créer le dépôt**, hors du vault (règle R3), puis le pousser :
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

9. **Passer la main.** "Cadrage terminé, dépôt créé. Dites tickets." Si le skill nuit
   est installé, une seule question : "Voulez-vous lancer le mode nuit ? Oui, ou non."

## Point d'arrêt

- Étape 3 : pas de suite sans reformulation confirmée.
- Étape 6 : aucune note ne passe `valide` sans relecture.
- Étape 7 : le dépôt ne se crée pas sans le "go" de la porte 1.

## Preuve attendue

Les notes et leurs statuts, la valeur de `phase`, les retraits du périmètre. Pour le
dépôt : l'adresse, le contrôle `AGENTS.md` vide, `main` par défaut, `preprod` poussée.

## Interdits

- Remplir deux phases dans la même session. Plusieurs questions dans un message.
- Deviner une décision produit. Réduire le périmètre sans l'écrire.
- Ajouter une bibliothèque, un socle ou du code au dépôt.
- Écrire dans `_Modèles/`, `_Méthode/`, `_À trier/` ou dans les blocs générés.
- Recopier une information d'une autre note au lieu de la lier.
- Mettre de vraies données de personnes.
- Lancer `git` dans le dossier du vault de ce PC. Pousser en force. Créer des tickets.
