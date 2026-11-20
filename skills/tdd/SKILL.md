---
name: tdd
description: Code un comportement à la fois en partant du test. Écrit un test qui échoue, le voit échouer, écrit le plus petit code qui le fait passer, le voit passer, puis nettoie. Pour un bug, reproduit d'abord le défaut par un test. À utiliser quand feature code une fonction avec de la logique ou corrige un bug, ou quand l'utilisateur dit "tdd", "teste d'abord", "écris le test" ou "reproduis le bug". Ne pas utiliser pour un changement sans logique (texte, documentation, configuration), ni pour lancer tous les contrôles (verifier), ni pour tester à l'écran (fiche QA).
---

# TDD : le test d'abord, un comportement à la fois

## But

Chaque comportement du ticket a un test qui aurait échoué sans le code.
Un test qu'on n'a jamais vu échouer ne prouve rien.

## Quand l'utiliser

- Appelé par feature, étape 5, quand le ticket a de la logique : calcul, règle, condition, transformation de données.
- Un bug à corriger : toujours, en commençant par le reproduire.
- L'utilisateur demande d'écrire le test d'abord.

## Quand ne pas l'utiliser

- Changement sans logique : texte d'interface, documentation, fichier de configuration, copie d'un gabarit. Écrire alors dans le « Journal de l'agent » de la note du ticket : "tdd sans objet : <raison>".
- Lancer toute la batterie : skill verifier.
- Tester l'écran à la main : fiche QA.

## Étapes

1. **Lister les comportements.**
   Lire "C'est fini quand" du ticket. En tirer une liste de comportements, un par ligne, du plus simple au plus dur.
   Chaque ligne dit une entrée et un résultat attendu : "un panier vide donne un total de 0".
   Bug : la première ligne est le défaut, avec les étapes pour le reproduire.
   Preuve : la liste, écrite dans le « Journal de l'agent » de la note du ticket.

2. **Écrire un seul test, pour le premier comportement.**
   Le placer à côté du code testé, selon l'usage du projet (profil Next.js : `<nom>.test.ts`, lancé par Vitest).
   Le nom du test dit le comportement en français.
   Tester le vrai code. Ne pas imiter ce qu'on teste.
   Preuve : le chemin du test.

3. **Le voir échouer.**
   Lancer seulement ce test (profil Next.js : `npx vitest run <fichier>`).
   Il doit échouer pour la bonne raison : le résultat est faux, ou la fonction manque.
   Une erreur de frappe ou d'import n'est pas un bon échec : corriger le test, relancer.
   Il passe déjà : le comportement existe, ou le test ne teste rien. Le dire, et le revoir.
   Preuve : la ligne d'échec, citée.

4. **Écrire le plus petit code qui le fait passer.**
   Rien de plus que ce que demande ce test.
   Preuve : le `chemin:ligne` du code ajouté.

5. **Le voir passer.**
   Relancer le même test, puis tous les tests du fichier.
   Preuve : la ligne de réussite, citée.

6. **Nettoyer.**
   Renommer, enlever les doublons, simplifier. Le comportement ne change pas.
   Relancer les tests du fichier : toujours verts.

7. **Comportement suivant.** Retour à l'étape 2, jusqu'au bout de la liste.
   Les cas limites ont leur ligne : vide, zéro, valeur négative, texte trop long, double envoi.

8. **Finir.** Ajouter une ligne dans le « Journal de l'agent » de la note du ticket par comportement : test, échec vu, réussite vue.
   Les fichiers entrent dans le commit du ticket (`git add <fichier>` puis `git commit --amend --no-edit`).

## Point d'arrêt

Aucun. Le skill rend la main à feature à la fin de la liste.
Un comportement impossible à tester par une commande (affichage sur téléphone) : le noter pour la fiche QA, continuer.

## Preuve attendue

Pour chaque comportement : le nom du test, la ligne d'échec vue, la ligne de réussite vue.

## Interdits

- Écrire le code avant le test.
- Garder un test jamais vu échouer.
- Modifier un test pour le faire passer, sauf s'il était faux. Le dire alors dans le « Journal de l'agent » de la note du ticket.
- Ignorer ou désactiver un test (`skip`, `only` laissé en place).
- Imiter la fonction qu'on teste. Imiter seulement ce qui est hors du projet : réseau, horloge.
- Mettre de vraies données de personnes dans un test.
