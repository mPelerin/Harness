---
name: qa-prep
description: Prépare la fiche QA d'un ticket et l'écrit dans la rubrique Fiche QA de sa note dans le vault, en suivant le modèle _Modèles/Notes/Fiche QA.md. L'agent prouve lui-même tout ce qu'une commande peut prouver, et ne laisse à l'utilisateur que les étapes à l'écran, précises, avec au moins un chemin qui doit échouer. Il bloque la fiche si un prérequis humain manque. À utiliser quand feature arrive à la fiche QA, ou quand l'utilisateur dit "fiche QA", "prépare le test" ou "qu'est-ce que je dois tester". Ne pas utiliser pour les contrôles (verifier) ni la relecture (revue).
---

# QA-prep : la fiche de test, dans la note du ticket

## But

Une fiche que l'utilisateur déroule en quelques minutes, sans deviner.
Ce que la machine peut prouver est déjà prouvé. Ce qui reste demande des yeux.
La fiche vit dans la note du ticket, rubrique "Fiche QA", copiée du modèle
`_Modèles/Notes/Fiche QA.md` : le corps seulement, de `## #<numéro>` à "Remise à zéro",
sans son en-tête ni son titre. Une fiche qui cache une migration ou un compte à créer
n'est pas prête : elle est bloquée, et le dit en tête.

## Quand l'utiliser

- Feature arrive à la fiche QA. L'utilisateur dit "fiche QA", "qu'est-ce que je dois tester".

## Quand ne pas l'utiliser

- Les contrôles automatiques : verifier. La relecture : revue.

## Le projet et le code

Règles R1 à R3 du skill projet. Les commandes de preuve se lancent dans `$ARBRE/code`.
La fiche s'écrit dans la note du ticket du worktree. Sources à lire :
`03 Design/<Nom> - Écrans et états` (les six états) et `02 Cadrage/<Nom> - Critères
d'acceptation`, par leur `resume` d'abord.

## Étapes

1. **Lire.** La note du ticket ("C'est fini quand"), le diff
   `git diff origin/preprod...HEAD` dans le worktree, et le modèle
   `_Modèles/Notes/Fiche QA.md`.
   Preuve : la liste des conditions du ticket.

2. **Classer chaque condition.**
   - **Machine** : une commande ou un test la prouve. L'agent la lance maintenant.
   - **Écran** : il faut regarder ou cliquer. L'utilisateur la fait.
   - **En ligne** : seulement sur la version déployée. Elle attend la mise en ligne.
   Preuve : chaque condition avec sa classe.

3. **Chercher les prérequis humains, avant tout le reste.**
   Lire le diff : migration, variable d'environnement, compte, service externe, jeu de
   données. Chacun se règle par un humain. L'écrire en tête de fiche, avec la commande
   exacte ou l'endroit où poser la valeur. Jamais la valeur d'un secret.
   **Un prérequis manquant bloque la fiche.** Ne pas l'écrire "prête", ne pas la
   marquer "à tester". Le dire à feature.
   Preuve : la liste des prérequis, ou "aucun".

4. **Prouver les étapes Machine.**
   Lancer chaque commande dans `$ARBRE/code`. Résultat ✅ et preuve courte dans la colonne
   Résultat. Rouge : ce n'est pas une fiche à écrire, c'est un défaut. Retour à feature.
   Preuve : chaque commande et sa sortie.

5. **Écrire les étapes Écran.** Huit au plus, précises : où cliquer, quoi saisir, ce
   qui doit s'afficher. Au moins une qui doit échouer : mauvaise saisie, mauvais
   compte, double clic. Une étape téléphone (390 pixels) dès qu'un écran change.
   Données inventées, jamais de vraies personnes.

6. **Écrire la rubrique "Pour tester".** Commandes exactes à copier d'un bloc, depuis
   la rubrique "Commandes de vérification" de `AGENTS.md` :
   `git fetch origin && git switch <branche> && <installation> && <lancement>`,
   puis l'adresse locale et la page. Et pour revenir : `git switch preprod`.

7. **Aucune étape Écran ?** Écrire en tête de fiche : "Rien à tester à l'écran. Les
   preuves Machine suffisent." La porte 2 se résume alors à lire les preuves.
   Un prérequis manquant garde la priorité : la fiche reste bloquée.

8. **Écrire la fiche dans la note du ticket**, rubrique "## Fiche QA", en respectant
   la structure du modèle : à tester à l'écran, à faire avant, version testée,
   pour tester, comptes de test, tableau des étapes, remise à zéro.
   La colonne Commentaire reste vide : c'est la place de l'humain.
   Preuve : le chemin de la note, le nombre d'étapes Machine et Écran, les prérequis.

9. **Tenir le plan de test**, `06 Qualité/<Nom> - Plan de test` du worktree, pour la
   non-régression : le test qui couvre le ticket sous "Tests automatisés", et l'étape
   Écran principale sous "Tests à la main" (geste, résultat attendu, `#<n>`).
   Elle part dans le commit du ticket.

## Point d'arrêt

Aucun. Le skill rend la main à feature.
Une fiche bloquée par un prérequis humain se dit dans le rapport.

## Preuve attendue

Le chemin de la note, le nombre d'étapes prouvées et laissées à l'utilisateur, les
prérequis humains ou "aucun", et "à tester à l'écran : oui ou non".

## Interdits

- Donner à l'utilisateur une étape qu'une commande peut prouver.
- Écrire une étape vague : "tester l'export", "vérifier que ça marche".
- Une fiche sans étape qui doit échouer, quand un écran change.
- Écrire une fiche prête quand un prérequis humain manque.
- Remplir la colonne Commentaire.
- Modifier le modèle `_Modèles/Notes/Fiche QA.md`.
- Mettre de vraies données de personnes, un secret ou un extrait de `.env`.
- Marquer ✅ une étape Machine sans la sortie de la commande.
