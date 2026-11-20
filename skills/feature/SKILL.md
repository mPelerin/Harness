---
name: feature
description: Réalise un ou plusieurs tickets GitHub d'affilée, sans arrêt inutile. Lit les tickets et le code, pose en un seul message les questions qui restent, code chaque ticket dans un seul commit, vérifie, relit, prépare la fiche QA, puis enchaîne avec livrer jusqu'à la demande de fusion et la CI verte. S'arrête une fois, à la porte 2, avec un tableau unique. Si ORCHESTRATEUR est rempli dans harness.conf, il délègue : une sous-conversation par ticket dépose la carte et la suit, et la conversation principale ne montre qu'un tableau. À utiliser quand l'utilisateur dit "feature", "feature 12", "feature 2 3 4", "feature tout", "feature local 12", "prends le ticket 12", "enchaîne les tickets" ou "fais les tickets ouverts". Ne pas utiliser pour une idée sans ticket (cadrage), pour écrire ou corriger un ticket (tickets), ni pour une mise en ligne (livrer).
---

# Feature : réaliser des tickets d'affilée

## But

Transformer un ou plusieurs tickets en demandes de fusion prêtes à tester : un commit par ticket, CI verte, fiche QA prête.
L'agent enchaîne seul. L'utilisateur n'intervient qu'à la porte 2, une fois pour tout le lot.

**Règle du commit unique.** Un ticket = un changement = un commit.
Le code, le test et la note du ticket vont dans ce commit. Le dépôt est le dossier du projet : les notes à la racine, l'appli dans `code/`, où se lancent ses commandes.
Une branche de ticket ne touche pas au journal des décisions : deux tickets d'un lot qui y ajoutent chacun une ligne se bloquent à la fusion.
Le ticket se travaille dans un worktree (`git worktree add`) : le dossier principal, synchronisé avec Obsidian, reste sur `preprod`.

**La note du ticket.** C'est la note du ticket (`05 Tickets/<projet> - T<numéro> <titre>.md` dans le vault), créée avec le modèle « Ticket » si elle n'existe pas. Elle contient :
- « Le ticket », « Plan » et « Décisions » : l'instruction. Le ticket recopié, les réponses aux questions, le plan, une ligne datée par décision.
- « Journal de l'agent » : chaque étape, la commande lancée, son résultat, daté.
- « Fiche QA » : remplie par le skill qa-prep.

**La porte 1 est le "oui" donné à la création du ticket** (skill tickets).
L'agent ne s'arrête de nouveau avant le code que dans trois cas :
- une question produit reste sans réponse écrite ;
- le ticket touche à l'argent, aux droits d'accès, aux données personnelles, au schéma de la base, ou demande une nouvelle bibliothèque ;
- le code montre que le ticket est déjà fait, ou qu'il contredit une décision écrite (journal des décisions du projet, ou la rubrique "Décisions" d'une note de ticket).

## Quand l'utiliser

- L'utilisateur donne un ou plusieurs numéros : c'est le lot.
- "feature tout" : le lot est `gh issue list --state open --limit 30`, dans l'ordre des dépendances. Le montrer en une ligne, puis continuer.
- Pas de numéro : proposer le plus petit ticket ouvert, et attendre.

## Quand ne pas l'utiliser

- Idée sans ticket : skill cadrage, puis tickets.
- Ticket flou, sans "C'est fini quand" vérifiable : skill tickets d'abord.
- Mettre en ligne (`preprod` vers main) : skill livrer, mode mise en ligne.

## Mode délégation

**Quand il s'applique.**
```bash
sed -n 's/^ORCHESTRATEUR=//p' ~/.config/harness/harness.conf | tail -n 1
```
Une valeur : délégation. Vide ou absente : mode local, les étapes normales.
"feature local 12" ou "feature local tout" force le mode local, sans lire la clé.

**Principe.** La conversation principale ne code pas. Elle reste un registre.
Chaque ticket part dans une **sous-conversation neuve** : l'outil de sous-agent de l'agent, un brief court, rien d'autre.
Les tickets indépendants partent en arrière-plan. Un ticket qui "Dépend de" un autre attend le retour de celui-ci.
Pas d'outil de sous-agent : le dire, et proposer « feature local ». Ne pas coder ici à la place.

**Pré-vol, avant tout dépôt.** `pre-vol <numéros> --strict` (code 1 : il reste un blocage, ou un ticket ne déclare rien).
Un ticket bloqué n'est pas déposé, il est mis "à préparer" dans le tableau.
Tout ticket qui réclame une variable, un compte, une migration ou un service le déclare dans "Prérequis" (skill tickets).

**Ticket sensible.** Argent, droits d'accès, données personnelles, base, nouvelle bibliothèque : il part seulement si le go écrit est dans la conversation. Sans ce go, il n'est pas déposé, et le tableau le dit. Jamais de go supposé.

**Le brief du sous-agent, neuf lignes.**
> Ticket #N, dépôt compte/dépôt, branche de base `preprod`. Ne touche jamais à `main`.
> Tu ne codes pas : tu déposes et tu suis.
> Écris le corps de la demande : ticket, dépôt, base `preprod`, jamais `main`, go écrit si le ticket est sensible.
> Pour Hermès, dans ce corps : « Tu ne codes pas. Choisis l'agent (écran, données, droits, CI, défaut). Crée une carte enfant avec `--parent <cette carte>`, skills feature et tdd, dont le corps reprend le ticket, la base `preprod` et l'interdiction de `main`. Elle code, pousse et ouvre la demande de fusion vers `preprod`, sans fusionner. »
> Dépose : `orchestrateur deposer-demande --ticket N --depot compte/dépôt --titre "Ticket #N : titre" --corps FICHIER`.
> Suis : `orchestrateur suivre CARTE --depot compte/dépôt --ticket N`.
> Tu absorbes l'attente : kanban, états, relances, CI. Jamais de code, de diff ni de journal.
> Tu ne réponds qu'une fois, à la fin.
> `ticket #N, demande de fusion #P, CI verte` ou `ticket #N, bloqué : motif de cinq mots`.

**Le tableau, seule sortie de la conversation principale.**

| Ticket | Agent | Demande de fusion | État |
| --- | --- | --- | --- |

Il se remplit au fil des retours. Tant qu'une sous-conversation n'a pas rendu sa ligne, la sienne reste "en cours".
Puis s'arrêter. Ne pas attendre les cartes ici, ne pas relancer soi-même.

## Skills appelés

En mode local : tdd (étape 5), verifier (étape 6), revue (étape 7), qa-prep (étape 8), livrer (étape 9).
En mode délégation : aucun. Le travail se fait sur le serveur.

## Étapes

En mode délégation, l'étape 1 et le pré-vol se font ici. Les étapes 2 et 4 à 9 ne se font pas ici. Le tableau de suivi remplace l'étape 10.

1. **Lire les tickets.**
   Pour chacun : `gh issue view <numéro> --json number,title,body,labels,state`.
   Lire une fois le AGENTS.md du projet, le journal des décisions, les rubriques "Décisions" des notes de `05 Tickets/`, et les notes de cadrage utiles (d'après leur `resume`).
   `git ls-remote --heads origin preprod` doit répondre. Sinon arrêt : le cadrage n'est pas fait.
   `AGENTS.md` de `preprod` rempli. Ce contrôle ne doit rien afficher :
   `git fetch origin && git show origin/preprod:AGENTS.md | awk '/<!--/{c=1} {print (c ? "" : $0)} /-->/{c=0}' | sed -E 's/<(numéro|mots-courts|n)>//g' | grep -nE '<[^>]+>'`
   Une ligne s'affiche : arrêt. "AGENTS.md n'est pas rempli. Dites cadrage : il le remplit à partir des documents, sans nouvelle question."
   Ranger le lot dans l'ordre des "Dépend de".
   Un ticket dont la dépendance est encore `OPEN` est mis **en attente** : sa branche partirait de `preprod` sans le code dont il a besoin. Il se fait après le "go" de sa dépendance (étape 10).
   `gh pr list --state open --json number,headRefName` : un ticket qui a déjà une demande de fusion ouverte (branche `<numéro>-...`) est écarté. Il attend déjà à la porte 2.
   Écarter, sans bloquer le reste : ticket fermé, sans "C'est fini quand" vérifiable, ou qui réunit plusieurs changements. Le dire dans le rapport final, avec "à passer par tickets".
   Preuve : le lot, dans l'ordre, et pour chaque ticket son changement en une phrase.

2. **Lire le code, sans rien modifier.**
   Un sous-agent en lecture seule si l'agent sait en lancer un. Sinon soi-même.
   Preuve : par ticket, une liste `chemin:ligne`, classée "existe déjà" et "manque".

3. **Questions, en un seul message, seulement s'il en reste.**
   Ne poser que ce qui n'est écrit ni dans les tickets ni dans les documents. Ne jamais deviner un arbitrage.
   Toutes les questions du lot dans un message, numérotées, chacune avec des choix courts et "Recommandé" en premier.
   L'utilisateur peut répondre "reco" : il prend toutes les recommandations.
   Ajouter dans ce message les tickets sensibles (voir la porte 1) avec leur plan en trois lignes. Ils attendent un "go" écrit.
   Y ajouter aussi les tickets déjà faits ou contraires à une décision, avec leur preuve `chemin:ligne`.
   Pas de question et rien de sensible : ne pas s'arrêter. Le plan va dans la note du ticket.
   Preuve : les réponses de l'utilisateur, ou "aucune question".

4. **Pour chaque ticket, l'un après l'autre : créer la branche.**
   Jamais deux tickets en même temps dans le même dossier.
   `git status --short` vide. Sinon arrêt : des changements étrangers rendent le diff illisible.
   `git switch preprod && git pull --ff-only && git switch -c <numéro>-<mots-courts>`.
   Si l'agent sait lancer un sous-agent neuf, chaque ticket peut s'y faire, avec les réponses de l'étape 3. Le contexte reste propre.
   Preuve : `git branch --show-current`.

5. **Coder, dans un seul commit.** Skill tdd pour tout ce qui a de la logique.
   Remplir la note du ticket (ticket, réponses, plan, décisions datées) et tenir son « Journal de l'agent ».
   `git add <fichier>`, un par un, jamais `-A`.
   Premier commit : `git commit -m "<phrase en français> (ticket #<numéro>)"`. Ensuite `git commit --amend --no-edit` à chaque ajout.
   Jamais `Closes`, `Fixes` ni `Resolves` devant un numéro.
   Hook qui refuse : corriger la cause.
   Preuve : `git rev-list --count preprod..HEAD` affiche 1.

6. **Vérifier.** Skill verifier, après le dernier `--amend` de code.
   Preuve : le bloc de preuve, avec le code du commit.

7. **Relire.** Skill revue. Corriger dans le même commit (`--amend`), puis refaire l'étape 6.
   Preuve : le bilan de revue.

8. **Préparer la fiche QA.** Skill qa-prep, dans la note du ticket. L'ajouter au commit avec `--amend`.
   Ne pas relancer verifier ici : livrer le refait sur le commit final, à l'étape 9.
   Preuve : le chemin de la fiche, et le compte toujours à 1.

9. **Livrer jusqu'à la porte 2, sans s'arrêter.** Skill livrer, mode ticket, étapes 1 à 5 : contrôles, push, demande de fusion, CI verte.
   Puis `git switch preprod` et ticket suivant, à l'étape 4.
   Preuve : le lien de la demande de fusion et la CI verte.

10. **Rapport unique. POINT D'ARRÊT : porte 2.**
    Un tableau : ticket, demande de fusion, commit, CI, à tester à l'écran (oui ou non), point d'attention.
    Sous le tableau, seulement s'il y en a : ce qui n'est pas fait, ce qui n'est pas vérifié, les tickets écartés, les tickets en attente. Une ligne chacun.
    Finir par : "Testez les fiches marquées oui. Dites go tout, go 2 4, ou ce qui ne va pas."
    Ce rapport est le message de la porte 2. Le "go" fait reprendre livrer à l'étape 7, ticket par ticket, sans rien redemander.
    Après les fusions, feature reprend seule à l'étape 4 pour les tickets en attente dont la dépendance vient d'arriver dans `preprod`.
    Preuve : le tableau, chaque ligne reliée à un lien ou à une commande.

## Points d'arrêt

- **Avant le code**, seulement dans les trois cas de la porte 1, et une seule fois pour tout le lot.
- **Porte 2**, à l'étape 10. Une fois pour tout le lot.
- **Mode délégation**, après le tableau. On ne suit pas les cartes dans cette conversation.
- **Arrêt d'un ticket, le lot continue** : verifier rouge après trois tentatives, CI rouge après trois tentatives, conflit. Le noter dans le rapport.
  Avant de passer au suivant : `git rebase --abort` ou `git merge --abort` si l'un est en cours, l'état reste commité sur la branche du ticket, rien de plus n'est poussé, `git status --short` est vide, puis `git switch preprod`.
- **Arrêt de tout** : dossier pas propre, `preprod` absente, `AGENTS.md` encore à trous, `git fetch` en échec, push refusé par GitHub.

## Preuve attendue

Le rapport de l'étape 10 contient, par ticket :

- le numéro, la branche, le commit (celui que le "go" couvrira), le lien de la demande de fusion
- la CI verte, et le bloc de verifier sur le même commit
- le chemin de la fiche QA, et s'il y a quelque chose à tester à l'écran

En mode délégation : le tableau de suivi, une ligne par ticket, et la carte déposée pour chacun.

## Interdits

- Coder un ticket sensible sans "go" écrit.
- Travailler sur `main` ou sur `preprod`, y commiter, y pousser.
- Fusionner : c'est livrer, après le "go" de la porte 2.
- Pousser en force (`--force`, `--force-with-lease`). `--no-verify`. `git add -A`.
- Écrire `Closes`, `Fixes` ou `Resolves` devant un numéro de ticket.
- Plus d'un commit par branche avant le push. `--amend` après le push.
- Deux tickets en même temps dans le même dossier.
- Ajouter une bibliothèque sans "go", origine et version exacte montrées.
- Lire un fichier `.env` ou un secret. Écrire de vraies données de personnes.
- Dire "ça passe" sans la sortie citée.
- Modifier un ticket : c'est le skill tickets.
- Deviner une décision produit.
- En mode délégation : coder, créer une branche, écrire un diff ou un journal dans cette conversation.
- Déposer deux fois la même demande le même jour. Laisser une carte toucher `main`.
