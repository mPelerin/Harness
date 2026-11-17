---
name: verifier
description: Lance les contrôles du projet et rapporte la preuve, avec la commande, le code de sortie et la dernière ligne, liée à un commit précis. À utiliser quand l'utilisateur dit "vérifie", "lance les contrôles", "est-ce que ça passe", "prouve-le", ou avant de dire qu'un travail est fini. Appelé aussi par feature et livrer. Ne pas utiliser pour tester à la main à l'écran (fiche QA) ni pour relire le code (revue).
---

# Vérifier : prouver, pas affirmer

## But

Un "ça passe" ne vaut que s'il vient avec la commande lancée et sa sortie.
Ce skill lance les contrôles du projet et rend une preuve courte, que l'utilisateur relit d'un coup d'oeil.

## Quand l'utiliser

- L'utilisateur demande de vérifier, de lancer les contrôles, ou de prouver un résultat.
- Avant toute phrase du genre "c'est fini" ou "ça marche".
- Appelé par feature (étape 6) et par livrer.

## Quand ne pas l'utiliser

- Tester un écran, un parcours, un téléphone : c'est la fiche QA, faite par l'utilisateur.
- Chercher des défauts de conception dans le code : skill revue.
- Vérifier que l'appli répond en ligne : skill livrer.

## Étapes

1. **Trouver la commande.**
   La lire dans le AGENTS.md du projet, rubrique "Commandes de vérification".
   Si la rubrique est absente ou garde un modèle non rempli (`<commande de vérification>`), regarder `package.json` : le profil Next.js y définit le script `verifier` (format, lint, types, tests, build).
   Commande trouvée dans `package.json` : l'utiliser, le dire, et proposer de l'écrire dans AGENTS.md. Ne pas modifier AGENTS.md sans "go".
   Rien trouvé nulle part : s'arrêter et demander. Ne jamais en inventer une.
   Preuve : la commande exacte et le `fichier:ligne` qui la donne.

2. **Fixer ce qu'on vérifie.**
   Lancer `git rev-parse --short HEAD` et `git status --short`.
   Des fichiers non commités : le dire. La preuve vaudra pour l'état actuel du dossier, pas pour le commit.
   Preuve : le code du commit et l'état du dossier ("propre" ou "n fichiers modifiés").

3. **Lancer la commande en entier, sans filtrer.**

   ```bash
   LOG=$(mktemp); npm run verifier > "$LOG" 2>&1; echo "code de sortie : $?"; tail -n 15 "$LOG"
   ```

   Remplacer `npm run verifier` par la commande de l'étape 1 si elle diffère.
   Un tuyau vers `tail` ou `grep` cacherait l'échec : on lit le journal après coup.
   Preuve : le code de sortie et les quinze dernières lignes.

4. **Si c'est rouge, corriger la cause.**
   Lire la première erreur, pas la dernière. Corriger dans le code. Relancer l'étape 3 en entier.
   Trois tentatives au plus. Ensuite s'arrêter et rapporter ce qui échoue et ce qui a été tenté.
   Ne jamais réparer en affaiblissant le contrôle : pas de test ignoré, pas de `eslint-disable`, de `@ts-ignore` ni de `any` ajouté, pas de règle assouplie sans "go" de l'utilisateur.
   Preuve : la sortie de chaque tentative.

5. **Relier aux critères du ticket**, quand un ticket est connu.
   Pour chaque condition de "C'est fini quand" : une preuve (nom du test, sortie, `fichier:ligne`) ou "non vérifié" avec la raison (écran, téléphone, en ligne).
   Aucun critère passé sous silence.
   Preuve : un tableau critère, preuve.

6. **Regarder la CI**, si une demande de fusion existe.
   `gh pr checks` donne l'état des étapes de la branche courante. En cas de rouge, `gh run view <identifiant> --log-failed`.
   Sans demande de fusion, écrire "CI non lancée" : elle ne tourne que sur les demandes de fusion, et après une fusion sur main ou sur `preprod`.
   Preuve : l'état de chaque étape, ou "CI non lancée".

7. **Rendre le bloc de preuve.**

   ```
   Vérification : npm run verifier (trouvée dans package.json:14)
   Commit : a1b2c3d (dossier propre)
   Code de sortie : 0
   Dernière ligne : <recopiée telle quelle>
   Critères du ticket : 3 prouvés sur 4, 1 non vérifié (écran téléphone)
   CI : non lancée
   ```

   Preuve : ce bloc, complet.

## Point d'arrêt

- Aucune commande trouvée, ni dans AGENTS.md ni dans package.json : s'arrêter, demander.
- Toujours rouge après trois tentatives : s'arrêter, rapporter.
- Aucune autre pause. Une preuve verte se rend tout de suite.

## Preuve attendue

Le bloc de l'étape 7, complet. Il vaut pour le commit cité et pour lui seul.
Dès qu'un fichier change, la preuve est périmée : relancer le skill.

## Interdits

- Écrire "tous les tests passent" sans la sortie.
- Citer un résultat de mémoire ou d'avant la dernière modification.
- Cacher le code de sortie derrière un tuyau (`| tail`, `| grep`).
- Affaiblir un contrôle pour le faire passer.
- Lire un fichier `.env`. Si un test demande des variables, regarder `.env.example` et demander à l'utilisateur.
- Dire "pas lié à mon changement" sans l'avoir prouvé (même commande sur main).
