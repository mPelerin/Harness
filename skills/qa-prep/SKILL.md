---
name: qa-prep
description: Prépare la fiche QA d'un ticket pour que l'utilisateur teste vite. L'agent prouve lui-même tout ce qu'une commande peut prouver, et ne laisse à l'utilisateur que les étapes à l'écran, précises, avec au moins un chemin qui doit échouer, et les commandes exactes pour lancer l'appli sur la branche. À utiliser quand feature arrive à la fiche QA, ou quand l'utilisateur dit "fiche QA", "prépare le test", "qu'est-ce que je dois tester" ou "cahier de test du ticket". Ne pas utiliser pour lancer les contrôles automatiques (verifier) ni pour relire le code (revue).
---

# QA-prep : la fiche de test, prête à dérouler

## But

Une fiche que l'utilisateur déroule en quelques minutes, sans deviner.
Ce que la machine peut prouver est déjà prouvé. Ce qui reste demande des yeux.

## Quand l'utiliser

- Appelé par feature, étape 8.
- L'utilisateur demande ce qu'il doit tester sur un ticket.

## Quand ne pas l'utiliser

- Lancer les tests automatiques : skill verifier.
- Chercher des défauts dans le code : skill revue.

## Étapes

1. **Lire.** Le ticket ("C'est fini quand"), `git diff origin/preprod...HEAD`, et `docs/qa/modele-fiche-qa.md`.
   Preuve : la liste des conditions du ticket.

2. **Classer chaque condition.**
   - **Machine** : une commande ou un test la prouve. L'agent la lance maintenant.
   - **Écran** : il faut regarder ou cliquer. L'utilisateur la fait.
   - **En ligne** : seulement sur la version déployée. Elle attend la mise en ligne.
   Preuve : chaque condition avec sa classe.

3. **Prouver les étapes Machine.**
   Lancer chaque commande. Résultat ✅ et une preuve courte dans la colonne Résultat.
   Rouge : ce n'est pas une fiche à écrire, c'est un défaut. Retour à feature.
   Preuve : chaque commande et sa sortie.

4. **Écrire les étapes Écran.** Huit au plus.
   Précises : où cliquer, quoi saisir, ce qui doit s'afficher.
   Au moins une qui doit échouer : mauvaise saisie, mauvais compte, double clic.
   Une étape téléphone (390 pixels de large) dès qu'un écran change.
   Données inventées, jamais de vraies personnes.

5. **Écrire la rubrique "Pour tester".** Les commandes exactes, à copier d'un bloc :
   `git fetch origin && git switch <branche> && <commande d'installation> && <commande de lancement>`, puis l'adresse locale à ouvrir, avec la page.
   Les commandes viennent de la rubrique "Commandes de vérification" du AGENTS.md.
   Et pour revenir : `git switch preprod`.

6. **Aucune étape Écran ?** Écrire en tête de fiche : "Rien à tester à l'écran. Les preuves Machine suffisent."
   La porte 2 se résume alors à lire les preuves et dire "go".

7. **Enregistrer.** `docs/qa/<numéro>-<mots-courts>.md`, copié du modèle.
   La colonne Commentaire reste vide.
   L'ajouter au commit : `git add docs/qa/<fichier>` puis `git commit --amend --no-edit`, si la branche n'est pas encore poussée. Sinon un commit de correction (skill livrer).
   Preuve : le chemin, le nombre d'étapes Machine et Écran.

## Point d'arrêt

Aucun. Le skill rend la main à feature.

## Preuve attendue

Le chemin de la fiche, le nombre d'étapes Machine prouvées et d'étapes Écran laissées à l'utilisateur, et "à tester à l'écran : oui ou non".

## Interdits

- Donner à l'utilisateur une étape qu'une commande peut prouver.
- Écrire une étape vague : "tester l'export", "vérifier que ça marche".
- Une fiche sans étape qui doit échouer, quand un écran change.
- Remplir la colonne Commentaire.
- Mettre de vraies données de personnes, un secret ou un extrait de `.env`.
- Marquer ✅ une étape Machine sans la sortie de la commande.
