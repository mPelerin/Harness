---
name: cadrage
description: Remplit la mémoire du projet dans le vault, phase par phase (Discovery, Cadrage, Design, Conception), une phase par session, à partir des notes du classeur. Dès le premier entretien si demandé, prépare GitHub. À la fin, complète le dépôt à la racine du dossier projet (notes et code/), avec README, .gitignore et AGENTS.md, sans aucune bibliothèque, après le go de la porte 1. À utiliser quand l'utilisateur dit "cadrage", "cadre cette idée", "challenge mon idée", "continuer le cadrage", "écris le PRD" ou "on cadre le projet". Ne pas utiliser pour créer le classeur (projet), les tickets (tickets) ni coder (feature).
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

Traiter les phases dans l'ordre Discovery, Cadrage, Design, Conception. Pour les
livrables, suivre l'ordre du sommaire de la phase. Le champ `agent` d'une note
précise le regard à adopter. Sur Hermès, affecter une carte par note à ce profil.

`a-faire` devient `brouillon` quand la note est remplie, `valide` quand l'utilisateur l'a
relue. Une note sans objet prend `obsolete`, avec la raison écrite dedans.

## Étapes

1. **Situer** (R1 du skill projet). Lire la phase dans la note projet, puis le fichier
   `agent.md` à la racine du dossier de cette phase pour adopter son rôle principal.
   Puis lire les `resume` et lister les notes `a-faire`. Si `agent.md` manque, suivre les profils des notes.
   Avant le premier questionnaire, renommer la conversation active avec la phase lue
   (Discovery, Cadrage, Design ou Conception). Respecter un titre choisi par l'utilisateur.
   Dans Codex, appeler `set_thread_title` avec le titre, sans identifiant de conversation
   pour cibler la conversation active. Sur Claude Code, le [hook](scripts/titre.py)
   applique le titre au lancement. Garder `/rename <phase>` comme solution de secours.
   Avant le questionnaire, indiquer le chemin de l'`agent.md` effectivement lu et le
   rôle adopté. S'il manque, signaler le recours aux profils des notes.
   Preuve : le chemin du projet, la phase, la liste des notes avec leur statut.

2. **Décider où on en est.** Une phase est complète quand toutes ses notes sont
   `valide` ou `obsolete`. Si c'est déjà le cas, aller à l'étape 6 pour terminer
   la phase, ou à l'étape 7 pour finaliser Conception. Traiter une seule phase
   par conversation.
   Preuve : "phase X : n notes validées, m à faire".

3. **Au premier passage, reformuler l'idée** en deux phrases : qui, fait quoi, pour quel
   résultat. Confirmer la reformulation, puis recueillir les réponses par séries (étape 4).
   Une fois le nom et le compte confirmés, proposer l'initialisation GitHub. Sur
   accord explicite, suivre [l'initialisation](references/depot.md#initialisation-au-premier-entretien).

4. **Mener l’entretien par séries, puis écrire en lot.** Lire les notes utiles une
   fois au début de la série. Poser 5 questions indépendantes à la fois, ou 10 à la
   demande. Montrer le solde quand il en reste moins. Poser les questions dépendantes
   une fois la réponse nécessaire obtenue.
   - Numéroter les questions et lettrer les choix. Mettre "Recommandé" en premier
     quand c'est pertinent, avec la raison en une phrase. Indiquer sous chaque question
     "Plusieurs réponses possibles". Prévoir "Autre" et "À revoir". Sous la série, laisser
     un espace "Texte libre" pour compléter une réponse ou proposer son propre choix.
   - Si Visualize est disponible, lire et appliquer son skill dès la première série.
     « J’utilise le skill Visualize pour afficher le questionnaire directement dans
     le chat, avec un seul bouton de validation. » Afficher des cases à cocher
     indépendantes (`type="checkbox"`) pour chaque question. Cocher un deuxième choix
     doit laisser le premier coché. Un seul choix suffit si l'utilisateur le souhaite.
     Avant d'afficher, vérifier que la validation transmet tous les choix cochés et le texte libre.
   - Sans Visualize, utiliser le formulaire natif s'il autorise plusieurs réponses
     par question. Afficher chaque question au-dessus de ses choix cliquables.
     Placer un champ libre commun sous les questions et un seul bouton de validation.
     Si l'interface ne permet pas ce format, afficher toute la série dans un seul
     message. Si l'utilisateur demande des choix cliquables en priorité, utiliser le
     formulaire natif en séries plus courtes et recueillir le complément libre
     dans le formulaire ou dans le chat, selon l'interface.
     Exemple de réponse groupée : `1A, 2B+C, 3 à revoir`, puis
     `Texte libre : 2. Mon complément…`. Une réponse dictée convient aussi.
   - Entre deux écritures, garder les réponses dans la conversation et enchaîner
     les séries sans demander l'accord pour continuer. Écrire au bout de
     15 questions répondues, ou 20 à la demande. Compter une fois chaque numéro,
     même avec plusieurs choix ou une correction. Une question sautée ou "À revoir"
     reste ouverte.
     Réduire la série à l'approche du seuil pour le respecter.
   - Au seuil, à la fin de l'entretien ou avant de quitter la conversation,
     écrire les réponses en attente et les décisions dans le vault en un lot.
     Dans ce même lot, retirer les consignes des rubriques remplies (R4 du skill projet).
     Écrire aussi à la demande. Noter les points encore ouverts pour la reprise.
     Vérifier le classeur une fois et repartir à zéro après vérification du lot.
     Si l'écriture échoue, relire ce qui a été écrit avant de réessayer et conserver
     les réponses restantes. Une réponse ne vaut pas validation de la note.
     Garder les mots de l'utilisateur dans la note Idée brute.
   Livrables répétitifs, copiés de `_Modèles/Notes` :
   - Atelier : `<Nom> - Atelier AAAA-MM-JJ <sujet>` dans `01 Discovery/`.
   - Entretien : `<Nom> - Entretien AAAA-MM-JJ <rôle>` dans `01 Discovery/`, lié depuis
     Entretiens.
   - Décision lourde : `<Nom> - Décision AAAA-MM-JJ <sujet>` dans `07 Décisions/`,
     liée dans la colonne Détail du journal des décisions.
   À l’écriture du lot, ajouter une ligne datée par décision tranchée au journal.
   Preuve : notes passées à `brouillon`, décisions consignées et vérification du lot.

5. **Contrôler les livrables.** Suivre la méthode de l'`agent.md` de la phase s'il existe.
   Avant de rédiger ou de relire, appliquer [les contrôles de la phase](references/livrables.md),
   y compris sur les projets anciens. Preuve : notes remplies et raisons des « sans objet ».

6. **Fin de phase. POINT D'ARRÊT.** Écrire les dernières réponses avant la relecture.
   Montrer les notes et demander la relecture. Relue : `valide`. Discovery, Cadrage
   ou Design complet : mettre `phase` à jour dans la note projet, vérifier puis
   finir avec un prompt de reprise pour le skill cadrage et la phase suivante.
   En cas d'arrêt avant validation, préparer un prompt pour reprendre la même phase.
   Si la phase Conception est complète, finir le cadrage aux étapes 7 à 9.
   Preuve : les statuts relus et la valeur de `phase`. Vérifier les changements avec
   `vault_projets.py verifier <Nom>` (étape 4 du skill projet). Réutiliser le résultat
   si aucune note n’a changé depuis le contrôle.

7. **Conception complète : porte 1.** Montrer le récapitulatif (phrase, utilisateurs,
   nombre de stories, contraintes, points sensibles, retraits du périmètre) et les cases
   "Porte 1" de `_Méthode/Portes.md` encore vides. Si GitHub est déjà initialisé, proposer de finaliser le cadrage dans le dépôt existant. Sinon : "Je crée le dépôt à la racine
   de `<Nom>`, avec les notes, README, .gitignore et AGENTS.md. Rien d'autre. Dites go."
   Sans ce go, rien ne se crée. Preuve : le récapitulatif, le "go" écrit.

8. **Finaliser le dépôt de cadrage.** Après le feu vert de la porte 1, lire et
   appliquer [la finalisation GitHub](references/depot.md#finaliser-le-dépôt-de-cadrage)
   pour reprendre le dépôt existant ou le créer et vérifier le résultat.

9. **Passer la main.** Résumer le résultat vérifié et donner le prompt pour lancer
   tickets dans une nouvelle conversation. Si le mode nuit est la suite souhaitée,
   préparer un prompt pour en examiner le lancement. Il demandera le feu vert
   prévu dans cette nouvelle conversation.

Pour reprendre une phase dans une nouvelle conversation, fournir un bloc prêt à copier :

```text
Projet <nom>. Dossier <chemin absolu>.
Lancez le skill cadrage à la phase <phase>.
Lisez <chemin de l'agent.md de la phase> avant de reprendre l'entretien.
Renommez cette conversation avec le nom de la phase, sauf si je lui ai déjà donné un titre.
Utilisez Visualize si disponible. Chaque question doit permettre de cocher plusieurs réponses à la fois. Prévoyez un seul bouton de validation pour toute la série.
Lisez <note projet et notes utiles>. Reprenez par <action précise ou relecture attendue>.
```

## Point d'arrêt

- Étape 3 : pas de suite sans reformulation confirmée.
- Étape 6 : aucune note ne passe `valide` sans relecture.
- Au premier entretien, la création du dépôt exige l’accord explicite de l’utilisateur. La porte 1 valide ensuite le contenu du cadrage.

## Preuve attendue

Les notes et leurs statuts, la valeur de `phase`, les retraits du périmètre. Pour le
dépôt : l'adresse, le contrôle `AGENTS.md` vide, `main` par défaut, `preprod` poussée.

## Interdits

- Remplir deux phases dans la même session.
- Deviner une décision produit. Réduire le périmètre sans l'écrire.
- Ajouter une bibliothèque, un socle ou du code au dépôt.
- Écrire dans `_Modèles/`, `_Méthode/`, `_À trier/` ou dans les blocs générés.
- Recopier une information d'une autre note au lieu de la lier.
- Mettre de vraies données de personnes.
- Lancer `git` dans le dossier du vault de ce PC. Pousser en force. Créer des tickets.
