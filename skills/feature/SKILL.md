---
name: feature
description: Réalise un ou plusieurs tickets d'affilée. Lit la note du ticket et l'issue, travaille dans un worktree du dépôt (notes et code ensemble), écrit plan, décisions et journal dans la note du ticket, code dans code/, vérifie, relit, prépare la fiche QA, puis livre jusqu'à la porte 2 avec un tableau unique. Sert aussi aux agents codeurs de Hermès, sur leur carte. À utiliser quand l'utilisateur dit "feature", "feature 12", "feature 2 3 4", "feature tout", "prends le ticket 12" ou "enchaîne les tickets", ou quand une carte kanban le demande. Ne pas utiliser pour une idée sans ticket (cadrage), écrire ou corriger un ticket (tickets), ni mettre en ligne (livrer).
---

# Feature : réaliser des tickets d'affilée

## But

Des demandes de fusion prêtes à tester : un commit par ticket, CI verte, fiche QA prête.
L'utilisateur n'intervient qu'à la porte 2, une fois pour le lot.
**Un ticket = un changement = un commit**, qui contient le code et la note du ticket.

La porte 1 est le "go" donné à la création du ticket. On ne s'arrête avant le code que
si une question produit reste ouverte, si le ticket est sensible sans "go" écrit, ou si
le code montre qu'il est déjà fait ou qu'il contredit une décision écrite.

## Quand l'utiliser

- Des numéros : c'est le lot. "feature tout" : les tickets ouverts dont la note a
  `agent: local`, dans l'ordre des dépendances. Pas de numéro : proposer le plus petit.
- Une carte kanban de Hermès qui cite un ticket.

## Quand ne pas l'utiliser

- Ticket sans "C'est fini quand" vérifiable : skill tickets.
- Ticket `agent: hermes` lancé en local : Hermès l'a déjà. Le dire, ne pas le prendre.

## Le projet

Règles R1 à R4 du skill projet. `BASE` est le dépôt de cette machine. Chaque ticket a
son worktree `ARBRE`. La note du ticket se lit et s'écrit **dans `ARBRE`** :
`$ARBRE/05 Tickets/<Nom> - T<n> <titre>.md`. L'appli se lance dans `$ARBRE/code`.

## Étapes

1. **Lire les tickets.** `gh issue view <n> --json number,title,body,labels,state`, la
   note du ticket, `AGENTS.md`, le journal des décisions, et le `resume` des notes de
   `04 Conception/`. Ouvrir Architecture, Données ou Sécurité seulement si le ticket les
   touche. Contrôles, dans `BASE` :
   `test -n "$(git ls-remote --heads origin preprod)"`, et rien ne s'affiche avec
   `git show origin/preprod:AGENTS.md | awk '/<!--/{c=1} {print (c ? "" : $0)} /-->/{c=0}' | grep -nE '<[^>]+>'`.
   Sinon arrêt, "dites cadrage". Ranger le lot selon "Dépend de" : dépendance encore
   ouverte, le ticket attend. `gh pr list --state open --json number,headRefName` : un
   ticket qui a déjà sa demande de fusion attend à la porte 2. Écarter, sans bloquer le
   reste, un ticket fermé, flou ou multiple : "à passer par tickets".
   Preuve : le lot, dans l'ordre, chaque ticket en une phrase.

2. **Lire le code, sans rien modifier.** Un sous-agent en lecture seule si possible.
   Preuve : par ticket, `chemin:ligne` classés "existe déjà" et "manque".

3. **Questions, en un seul message, seulement s'il en reste.** Numérotées, choix courts,
   "Recommandé" en premier, "reco" pour tout prendre. Y joindre les tickets sensibles
   (plan en trois lignes) et les tickets déjà faits ou contraires à une décision, avec
   leur preuve. Rien à demander : continuer. Sur une carte Hermès : une question bloque
   la carte, elle ne se devine pas. Preuve : les réponses, ou "aucune question".

4. **Pour chaque ticket, un worktree.**
   ```bash
   git -C "$BASE" fetch origin
   ARBRE="$HOME/.local/share/harness/worktrees/$NOM/<n>-<mots-courts>"
   git -C "$BASE" worktree add -b "<n>-<mots-courts>" "$ARBRE" origin/preprod
   ```
   Sur une carte Hermès, vérifier dans cet arbre que la révision de cadrage transmise
   est incluse (`git merge-base --is-ancestor "$REVISION" HEAD`, depuis `ARBRE`).
   Relire la note versionnée, ses critères et ses sources. Si la note a changé depuis
   cette révision, vérifier son affectation et son accord avant de coder.
   Révision absente, note manquante ou accord retiré : bloquer la carte.
   Dans la note du ticket (dans `ARBRE`) : `branche`, et `statut: en-cours`.
   Preuve : `git -C "$ARBRE" branch --show-current`.

5. **Coder, dans un seul commit.** Avant de coder, remplir dans la note "## Plan" et
   "## Décisions" (une ligne datée, avec la raison). Skill tdd pour la logique.
   Chaque étape marquante : une ligne datée dans "## Journal de l'agent".
   `git add <fichier>` un par un, jamais `-A`. Premier commit
   `git commit -m "<phrase en français> (ticket #<n>)"`, puis `git commit --amend --no-edit`.
   Une branche de ticket n'écrit pas dans le journal des décisions : la décision reste
   dans la note du ticket, cloture-session la reporte.
   Preuve : `git -C "$ARBRE" rev-list --count origin/preprod..HEAD` affiche 1.

6. **Vérifier.** Skill verifier. Preuve : le bloc de preuve.

7. **Relire.** Skill revue. Corriger dans le même commit, refaire l'étape 6.

8. **Fiche QA.** Skill qa-prep, dans la note du ticket. Puis `statut: en-revue`, et
   `git add` de la note, `--amend`. Preuve : le compte toujours à 1.

9. **Livrer jusqu'à la porte 2.** Skill livrer, mode ticket, étapes 1 à 5. Puis ticket
   suivant à l'étape 4. Sur une carte Hermès : rendre le lien et l'état sur la carte.

10. **Rapport unique. POINT D'ARRÊT : porte 2.** Un tableau : ticket, demande de fusion,
    commit, CI, à tester à l'écran, point d'attention. Puis les cases "Porte 2" de
    `_Méthode/Portes.md` que l'agent n'a pas pu cocher, et ce qui n'est pas fait ou pas
    vérifié. "Testez les fiches marquées oui. Dites go tout, go 2 4, ou ce qui ne va pas."
    Le "go" reprend livrer à l'étape 7.

## Points d'arrêt

- Avant le code : les cas de la porte 1, une fois pour le lot. Porte 2 : étape 10.
- Arrêt d'un ticket, le lot continue : verifier ou CI rouge après trois tentatives,
  conflit. `git rebase --abort` ou `git merge --abort` si besoin, rien de plus poussé,
  worktree propre. Le noter dans la note et le rapport.
- Arrêt de tout : pas de dépôt, `preprod` absente, `AGENTS.md` à trous, fetch en échec.

## Preuve attendue

Par ticket : la branche, le commit, la demande de fusion, la CI verte, le bloc de
verifier, et la note avec Plan, Décisions, Journal et Fiche QA dans le même commit.

## Interdits

- Coder un ticket sensible sans "go" écrit.
- Travailler dans le dossier du vault, sur `main` ou sur `preprod`. Deux tickets dans le
  même worktree. Pousser en force, `--no-verify`, `git add -A`.
- Écrire `Closes`, `Fixes` ou `Resolves` devant un numéro.
- Plus d'un commit avant le push. `--amend` après le push.
- Changer la rubrique "Le ticket" de la note ou l'issue : c'est le skill tickets.
- Ajouter une bibliothèque sans "go", origine et version montrées.
- Lire un `.env` ou un secret. Mettre de vraies données de personnes.
- Dire "ça passe" sans la sortie citée. Deviner une décision produit.
