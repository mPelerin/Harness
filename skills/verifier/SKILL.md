---
name: verifier
description: Lance les contrôles du projet dans code/ du dépôt et rapporte la preuve, avec la commande, le code de sortie et la dernière ligne, liée à un commit précis. Relie chaque preuve aux critères de la note du ticket dans le vault. À utiliser quand l'utilisateur dit "vérifie", "lance les contrôles", "est-ce que ça passe", "prouve-le", ou avant de dire qu'un travail est fini. Appelé aussi par feature et livrer. Ne pas utiliser pour tester à l'écran (fiche QA) ni pour relire le code (revue).
---

# Vérifier : prouver, pas affirmer

## But

Un "ça passe" ne vaut que s'il vient avec la commande lancée et sa sortie.
Ce skill lance les contrôles et rend une preuve courte, que l'utilisateur relit d'un
coup d'oeil. Les critères du ticket se lisent dans sa note du vault.

## Quand l'utiliser

- Avant de dire qu'un travail est fini. Appelé par feature, livrer et qa-prep.
- L'utilisateur dit "vérifie", "est-ce que ça passe", "prouve-le".

## Quand ne pas l'utiliser

- Tester à l'écran : qa-prep. Relire le code : revue.

## Le projet et le code

Règles R1 à R3 du skill projet. La commande se lance dans `code/` du worktree du ticket
(`$ARBRE/code`), ou du dépôt `BASE` hors ticket. Pas de dépôt : **arrêt**.

## Étapes

1. **Trouver la commande.**
   La lire dans `AGENTS.md` à la racine du dépôt, rubrique "Commandes de vérification".
   Si elle dit "à définir", lire la note `02 Cadrage/<Nom> - Contraintes techniques`
   pour la pile, puis le fichier de projet de cette pile dans `code/` (`package.json`,
   `build.gradle`...) : un script `verifier` sert de commande. Le dire, et proposer de
   l'écrire dans `AGENTS.md`. Ne pas le modifier sans "go".
   Rien trouvé nulle part : s'arrêter et demander. Ne jamais inventer.
   Preuve : la commande exacte et le `fichier:ligne` qui la donne.

2. **Fixer ce qu'on vérifie.**
   `git rev-parse --short HEAD` et `git status --short`, à la racine du worktree.
   Des fichiers non commités : le dire. La preuve vaut pour l'état du dossier, pas
   pour le commit. Preuve : le code du commit et l'état du dossier.

3. **Lancer la commande en entier, sans filtrer.**
   ```bash
   LOG=$(mktemp); <commande> > "$LOG" 2>&1; echo "code de sortie : $?"; tail -n 15 "$LOG"
   ```
   Un tuyau vers `tail` ou `grep` cacherait l'échec : on lit le journal après coup.
   Preuve : le code de sortie et les quinze dernières lignes.

4. **Si c'est rouge, corriger la cause.**
   Lire la première erreur. Corriger dans le code. Relancer l'étape 3 en entier.
   Trois tentatives au plus. Ne jamais affaiblir le contrôle : pas de test ignoré, pas
   de `eslint-disable`, pas de règle assouplie sans "go".
   Preuve : la sortie de chaque tentative.

5. **Relier aux critères de la note du ticket**, quand il y en a une.
   Pour chaque condition de "C'est fini quand" : une preuve (nom du test, sortie,
   `chemin:ligne`) ou "non vérifié" avec la raison (écran, téléphone, en ligne).
   Aucun critère passé sous silence. Écrire le résumé dans la note du ticket du
   worktree, rubrique "Journal de l'agent", à la date du jour.
   Hors ticket (mise en ligne, contrôle d'ensemble) : une ligne par critère dans le
   tableau "Preuves" de `06 Qualité/<Nom> - Vérification` du vault (critère, commande,
   sortie), datée. C'est la porte de sortie.
   Preuve : un tableau critère, preuve.

6. **Regarder la CI**, si une demande de fusion existe.
   `gh pr checks` donne l'état. Rouge : `gh run view <identifiant> --log-failed`.
   Sans demande de fusion : "CI non lancée". Preuve : l'état de chaque étape.

7. **Rendre le bloc de preuve.**

   ```
   Vérification : <commande> (trouvée dans AGENTS.md:12)
   Commit : a1b2c3d (dossier propre)
   Code de sortie : 0
   Dernière ligne : <recopiée telle quelle>
   Critères du ticket : 3 prouvés sur 4, 1 non vérifié (écran téléphone)
   CI : non lancée
   ```

   Preuve : ce bloc, complet.

## Point d'arrêt

- Aucune commande trouvée : s'arrêter, demander.
- Toujours rouge après trois tentatives : s'arrêter, rapporter.
- Aucune autre pause. Une preuve verte se rend tout de suite.

## Preuve attendue

Le bloc de l'étape 7, complet. Il vaut pour le commit cité et pour lui seul.
Dès qu'un fichier change, la preuve est périmée : relancer le skill.

## Interdits

- Écrire "tous les tests passent" sans la sortie.
- Citer un résultat de mémoire ou d'avant la dernière modification.
- Cacher le code de sortie derrière un tuyau.
- Affaiblir un contrôle pour le faire passer.
- Lire un fichier `.env`. Regarder `.env.example` et demander à l'utilisateur.
- Dire "pas lié à mon changement" sans l'avoir prouvé.
