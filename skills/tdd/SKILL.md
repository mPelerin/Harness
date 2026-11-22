---
name: tdd
description: Code un comportement à la fois en partant du test. Écrit un test qui échoue, le voit échouer, écrit le plus petit code qui le fait passer, le voit passer, puis nettoie. Le journal des comportements s'écrit dans la note du ticket, rubrique Journal de l'agent. Pour un bug, reproduit d'abord le défaut par un test. À utiliser quand feature code une fonction avec de la logique ou corrige un bug, ou quand l'utilisateur dit "tdd", "teste d'abord" ou "reproduis le bug". Ne pas utiliser pour un changement sans logique, ni pour les contrôles (verifier) ni l'écran (fiche QA).
---

# TDD : le test d'abord, un comportement à la fois

## But

Chaque comportement du ticket a un test qui aurait échoué sans le code.
Un test qu'on n'a jamais vu échouer ne prouve rien.
Le journal des comportements vit dans la note du ticket, rubrique "Journal de
l'agent", daté. Il n'y a plus de fichier `log.md` dans le dépôt.

## Quand l'utiliser

- Feature code une fonction avec de la logique, ou corrige un bug.
- L'utilisateur dit "tdd", "teste d'abord", "reproduis le bug".

## Quand ne pas l'utiliser

- Texte, documentation, configuration : pas de logique à tester.
- Lancer tous les contrôles : verifier. Tester à l'écran : qa-prep.

## Le projet et le code

Règles R1 à R3 du skill projet. Tout se passe dans le worktree du ticket : le code dans
`$ARBRE/code`, la note dans `$ARBRE/05 Tickets/`. Elle part dans le commit du ticket.

## Étapes

1. **Lister les comportements.**
   Lire "C'est fini quand" dans la note du ticket. En tirer une liste, un par ligne,
   du plus simple au plus dur. Chaque ligne dit une entrée et un résultat attendu :
   "un panier vide donne un total de 0". Bug : la première ligne est le défaut, avec
   les étapes pour le reproduire.
   Écrire la liste dans la note, rubrique "Journal de l'agent", avec la date.
   Preuve : la liste, visible dans la note.

2. **Écrire un seul test, pour le premier comportement.**
   Le placer à côté du code testé, selon l'usage du projet. Le nom du test dit le
   comportement en français. Tester le vrai code, ne pas imiter ce qu'on teste.
   Preuve : le chemin du test.

3. **Le voir échouer.**
   Lancer seulement ce test. Il doit échouer pour la bonne raison : résultat faux, ou
   fonction manquante. Une erreur d'import n'est pas un bon échec.
   Il passe déjà : le comportement existe, ou le test ne teste rien. Le dire, le revoir.
   Preuve : la ligne d'échec, citée.

4. **Écrire le plus petit code qui le fait passer.**
   Rien de plus que ce que demande ce test. Preuve : le `chemin:ligne` ajouté.

5. **Le voir passer.** Relancer le même test, puis tous les tests du fichier.
   Preuve : la ligne de réussite, citée.

6. **Nettoyer.** Renommer, enlever les doublons, simplifier. Le comportement ne change
   pas. Relancer : toujours vert.

7. **Comportement suivant.** Retour à l'étape 2, jusqu'au bout de la liste. Les cas
   limites ont leur ligne : vide, zéro, négatif, trop long, double envoi.

8. **Finir.** Ajouter dans la note, rubrique "Journal de l'agent", une ligne datée par
   comportement : test, échec vu, réussite vue. Les fichiers de code entrent dans le
   commit du ticket avec la note (`git add` un par un, puis `git commit --amend --no-edit`).
   Preuve : la note relue, et le commit toujours unique.

## Point d'arrêt

Aucun. Le skill rend la main à feature à la fin de la liste.
Un comportement impossible à tester par commande (affichage sur téléphone) : le noter
pour la fiche QA, et continuer.

## Preuve attendue

Pour chaque comportement : le nom du test, la ligne d'échec vue, la ligne de réussite
vue, et la trace dans la note du ticket.

## Interdits

- Écrire le code avant le test.
- Garder un test jamais vu échouer.
- Modifier un test pour le faire passer, sauf s'il était faux. Le dire alors dans la note.
- Ignorer ou désactiver un test (`skip`, `only` laissé en place).
- Imiter la fonction qu'on teste. Imiter seulement ce qui est hors du projet.
- Mettre de vraies données de personnes dans un test.
- Écrire dans le dossier du vault au lieu du worktree.
