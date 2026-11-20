---
name: cadrage
description: Transforme une idée de projet en documents de cadrage validés (PRD, écrans, user stories) dans les notes du projet (vault Obsidian), en posant les questions une à la fois, et remplit le AGENTS.md du projet. Écrit les notes dans le vault et AGENTS.md sur la branche preprod, puis s'arrête pour le go de l'utilisateur (porte 1). À utiliser quand l'utilisateur dit "cadrage", "cadre cette idée", "j'ai une idée de projet", "challenge mon idée", "écris le PRD" ou "fais les user stories". Ne pas utiliser pour créer les tickets (tickets), pour réaliser un ticket (feature), ni pour une petite correction qui tient dans un ticket.
---

# Cadrage : de l'idée aux documents de cadrage

## But

Sortir d'une idée floue avec des documents de cadrage validés par l'utilisateur.
Ils vivent dans le dossier du projet, dans le vault Obsidian (`RACINE_PROJETS/<projet>/`, voir `harness.conf`), pas dans un ticket ni dans le dépôt. Le dépôt est le sous-dossier `code/`.

- `02 Cadrage/<projet> - PRD.md` : le document de besoin. Quel problème, pour qui, ce qui est fait et ce qui ne l'est pas.
- `03 Design/<projet> - Écrans et états.md` : les écrans et les parcours. Facultatif si l'appli n'a pas d'écran.
- `02 Cadrage/<projet> - Stories.md` : les user stories, numérotées S1, S2... Le skill tickets en fait des tickets.

Les réponses qui resserviront vont dans `07 Décisions/<projet> - Journal des décisions.md`.
Une note remplie passe en `statut: brouillon`, puis `valide` après la porte 1. Les autres notes du dossier (discovery, design, conception) se remplissent quand l'agent qui les porte (propriété `agent`) est appelé.
Le cadrage remplit aussi le `AGENTS.md` du projet. C'est lui qui sait tout : sans lui, ce fichier reste un modèle à trous, lu à chaque conversation.

## Les branches

Le projet a deux branches qui durent, jamais trois : `main` et `preprod`.
- `main` = ce qui est en ligne, publié sur `DOMAINE_PROD`. Rien ne s'y écrit directement.
- `preprod` = le travail validé, pas encore en ligne, publié sur `DOMAINE_PREPROD` derrière un login. Elle naît de `main` et ne disparaît jamais.
- `main` est **toujours** la branche par défaut du dépôt GitHub. Un dépôt neuf pousse `main` en premier : GitHub prend la première branche poussée comme défaut, et une seule.
Chaque fusion de `preprod` vers main est une porte 3, donc une mise en ligne.
Les documents de cadrage s'écrivent directement sur `preprod`. Le code, jamais : il passe par une branche de ticket.

## Quand l'utiliser

- Une idée de projet ou de grosse fonction, même vague.
- L'utilisateur veut qu'on challenge une idée avant de la construire.
- Les notes de cadrage du projet sont à compléter.
- `AGENTS.md` garde des `<...>` (feature s'arrête et renvoie ici). Seulement l'étape 7, sans nouvelle question.

## Quand ne pas l'utiliser

- L'idée tient en un seul ticket clair : skill tickets, mode B.
- Le projet est déjà en ligne : voir l'arrêt de l'étape 1.

## Étapes

1. **Situer le projet.**
   Le dossier du projet existe dans le vault, sinon `python3 <harness>/scripts/vault/vault_projets.py nouveau <projet>`. Le dossier du projet est aussi son dépôt Git (notes à la racine, appli dans `code/`) : le reste de l'étape se fait dans `<projet>/`.
   `git status --short` doit être vide. Puis `git fetch origin`.
   - `origin/main` existe et la note PRD est en `statut: valide` : le projet est en ligne. **Arrêt.** Le cadrage d'une évolution n'est pas encore défini. Le dire à l'utilisateur.
     Exception : seul `AGENTS.md` est à remplir. Aller sur `preprod`, puis directement à l'étape 7.
   - Sinon, `preprod` existe (`git ls-remote --heads origin preprod`) : `git switch preprod && git pull --ff-only`. On complète le cadrage.
   - Sinon : projet neuf.
     - Dossier pas encore dépôt : `git init -b main`, un premier commit (README, `.gitignore`, le gabarit du projet), puis `gh repo create <compte>/<dépôt> --private --source=. --push`. `main` est poussée en premier, donc GitHub la prend comme branche par défaut. Enfin `git switch -c preprod`.
     - Dépôt existant avec `main` mais sans `preprod` : `git switch main && git pull --ff-only && git switch -c preprod`.
   Preuve : `git branch --show-current` affiche `preprod`, et `gh repo view <compte>/<dépôt> --json defaultBranchRef` affiche `main`.

2. **Reformuler l'idée.**
   La redire en deux phrases : qui, fait quoi, pour quel résultat.
   Confirmer la reformulation avant de continuer.
   Preuve : la reformulation, et le "oui" de l'utilisateur.

3. **Lire avant de demander.**
   Lire le AGENTS.md du projet, la note projet, le journal des décisions et les notes de cadrage déjà remplies, le code, et `gh issue list --state open --limit 20`.
   Une question dont la réponse est dans le dépôt ne se pose pas.
   Preuve : la liste de ce qui existe déjà, en `chemin:ligne` ou numéro de ticket.

4. **Dresser l'arbre des décisions.**
   Lister les décisions à prendre, dans l'ordre où elles dépendent les unes des autres.
   Penser à : le plus petit résultat utile, les cas d'échec, les comptes et les droits, les données personnelles, l'argent, les écrans, ce qu'on ne fait pas.
   Preuve : la liste numérotée, montrée en une fois, courte.

5. **Questionner, une décision à la fois.**
   Une seule question par message, des choix courts, "Recommandé" en premier, la raison en une phrase.
   Une réponse peut ouvrir de nouvelles branches : les ajouter à l'arbre.
   Après dix questions, proposer de s'arrêter. Le reste devient "Hypothèse".
   Preuve : chaque décision a une réponse ou est marquée "Hypothèse".

6. **Écrire les documents.**
   Utiliser les modèles plus bas, dans les notes du vault (le frontmatter de la note reste en place). Écrans seulement s'il y a des écrans.
   Ajouter les réponses utiles au journal des décisions, une ligne par décision, datée.
   **Périmètre réduit.** Chaque fois qu'une réponse retire quelque chose (un écran, un réglage, un mode, un parcours), ajouter une ligne datée dans « Retiré du périmètre » du PRD : quoi, pourquoi, et si c'est remis à plus tard. Rien ne disparaît en silence.
   Preuve : la liste des notes écrites, `vault_projets.py verifier` sans erreur, et ce qui a été retiré.

7. **Remplir `AGENTS.md`, puis commiter sur preprod.**
   Chaque `<...>` est remplacé à partir des notes, du code et du journal des décisions. Aucune nouvelle question.
   - Projet : les deux phrases du PRD. Utilisateurs : la rubrique du PRD.
   - Technologies, rangement : ce qui existe vraiment (`package.json`, les dossiers). Pas encore choisi : "aucune pour l'instant".
   - Règles métier critiques : tirées des Points sensibles et des "C'est fini quand" du PRD, avec leur raison. Aucune : "Aucune pour l'instant. En ajouter une dès qu'une erreur coûterait de l'argent ou de la confiance."
   - `<prénom>` : la valeur `PRENOM` de `~/.config/harness/harness.conf`. `<Piège suivant>` : ligne retirée. Dans le commentaire du haut, garder la ligne de licence et retirer le mode d'emploi.
   Ce qui manque s'écrit "à définir", et devient une Hypothèse dans le PRD.
   Contrôle, qui ne doit rien afficher :
   ```bash
   awk '/<!--/{c=1} {print (c ? "" : $0)} /-->/{c=0}' AGENTS.md | sed -E 's/<(numéro|mots-courts|n)>//g' | grep -nE '<[^>]+>'
   ```
   `git add` de `AGENTS.md` puis de chaque note écrite, une par une, puis un commit en français, par exemple "Cadrage : PRD, écrans, stories et AGENTS.md".
   Ne rien pousser à cette étape.
   Preuve : le contrôle vide, `git log --oneline -1` et la liste des fichiers du commit.

8. **Faire relire. POINT D'ARRÊT (porte 1).**
   Montrer à l'utilisateur le nom de chaque note écrite, `AGENTS.md` compris, et un résumé : nombre de stories, décisions, hypothèses, règles métier, et ce qui a été retiré du périmètre.
   Demander "go" après sa relecture. Chaque correction est un nouveau commit, puis on remontre.
   Preuve : le "go" de l'utilisateur, visible dans la conversation.

9. **Pousser et passer la main.**
   `git push -u origin preprod`, puis `git ls-remote --heads origin preprod`. Jamais de push forcé.
   Si la branche par défaut n'est pas `main` : `gh repo edit <compte>/<dépôt> --default-branch main`.
   Preuve : le code du commit affiché par `git ls-remote`, égal à celui de `git rev-parse HEAD`, et `gh repo view <compte>/<dépôt> --json defaultBranchRef` qui affiche `main`.
   Annoncer "Cadrage poussé sur preprod.".
   Si un skill `nuit` est installé, proposer le mode nuit en une seule question : "Voulez-vous lancer le mode nuit ? Oui, ou non."
   "Oui", "ok", "c'est bon" : skill nuit, tout de suite. Ce oui est son "go".
   "Non", ou pas de skill `nuit` : "Dites tickets pour créer les tickets à partir des stories."

## Modèle de la note PRD

```markdown
# PRD : <nom du projet>

## Problème
<Ce qui ne va pas aujourd'hui, pour qui, en deux ou trois phrases.>

## Utilisateurs
<Qui s'en sert. Un rôle par ligne.>

## Ce que ça fait
- <Parcours : l'utilisateur fait ceci, il obtient cela.>

## C'est fini quand
- [ ] <Condition que l'utilisateur peut vérifier lui-même.>

## Hors périmètre
- <Ce qu'on ne fait pas, et pourquoi.>

## Retiré du périmètre
- <Date : ce qui a été retiré en cours de cadrage, et pourquoi. « Rien » si rien n'a été retiré.>

## Points sensibles
- Argent, droits d'accès, données personnelles, base de données, services externes et variables attendues : <lesquels, ou "aucun">.

## Hypothèses
- <Ce qui n'a pas été tranché, à vérifier plus tard.>
```

## Modèle de la note Écrans et états

```markdown
# Écrans et parcours

## <Nom de l'écran>
- Sert à : <une phrase>.
- On y arrive par : <écran ou action>.
- États : vide, chargement, erreur, plein. <Ce qu'on voit dans chacun.>
```

## Modèle de la note Stories

```markdown
# User stories

## S1 : <titre court>
En tant que <rôle>, je veux <action>, pour <résultat>.
C'est fini quand :
- [ ] <Condition vérifiable>
```

## Point d'arrêt

- Étape 1 : arrêt si le projet est déjà en ligne, ou si le dossier n'est pas propre.
- Étape 2 : pas de suite sans reformulation confirmée.
- Étape 7 : arrêt si le contrôle de `AGENTS.md` affiche encore une ligne.
- Étape 8 : rien n'est poussé sans "go".
- Étape 9 : le mode nuit, s'il est installé, ne part pas sans "oui".

## Preuve attendue

- Les chemins des documents, et le commit sur `preprod`.
- Le contrôle de `AGENTS.md`, vide.
- Le "go" de l'utilisateur, puis le commit relu sur GitHub.
- Le nombre de stories, de décisions et d'hypothèses.
- Ce qui a été retiré du périmètre, s'il y en a.

## Interdits

- Poser plusieurs questions dans le même message.
- Deviner une décision produit. Une réponse absente devient une hypothèse écrite.
- Réduire un périmètre sans l'écrire dans « Retiré du périmètre ».
- Écrire sur main. Écrire du code, même sur `preprod`.
- Pousser en force (`--force`, `--force-with-lease`).
- Créer des tickets : c'est le rôle du skill tickets.
- Mettre de vraies données de personnes dans un document. Des exemples inventés.
- Ajouter une bibliothèque sans dire son origine et sa version.
- `git add -A`. `--no-verify`.
