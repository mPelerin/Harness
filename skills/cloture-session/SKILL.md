---
name: cloture-session
description: Clôt une session de travail sur un projet et écrit la passation, ou reprend une session à partir de la dernière passation. En clôture, relève l'état réel (git, demandes de fusion, tickets), signale ce qui risque d'être perdu, écrit une passation courte hors du dépôt et en commentaire du ticket en cours. En reprise, relit la passation et l'état, puis donne la prochaine action. À utiliser quand l'utilisateur dit "/fini", "fini", "on s'arrête", "clôture", "fin de session", "passation", ou "reprends", "on en était où", "où j'en suis". Ne pas utiliser pour tirer une leçon d'une erreur (retro).
---

# Clôture de session : rien ne se perd entre deux sessions

## But

Qu'une session neuve, avec n'importe quel agent, reparte en une minute.
La passation dit l'état réel, prouvé, et une seule prochaine action.

## Quand l'utiliser

- **Clôture** : l'utilisateur arrête le travail.
- **Reprise** : l'utilisateur revient et demande où il en était.

## Quand ne pas l'utiliser

- Transformer une erreur en garde-fou : skill retro.
- Livrer ce qui reste : skill livrer.

## La passation

Elle vit hors du dépôt, pour ne jamais salir l'arbre de travail :
`~/.local/share/harness/passations/<nom-du-dépôt>/<AAAA-MM-JJ-HHMM>.md`.
Si un ticket est en cours, un résumé court va aussi en commentaire du ticket : il suit le ticket, quel que soit le PC.

```
# Passation <nom-du-dépôt>, <date et heure>
Objectif de la session : <une phrase>
Fait : <ticket, demande de fusion, lien>, une ligne chacun
En cours : <branche>, <étape du skill>, commit <code>
En attente de l'utilisateur : <porte 2 de #4, question X>, ou "rien"
Risques : <fichier non commité, branche non poussée, CI rouge>, ou "aucun"
Prochaine action : <une seule, avec la commande ou la phrase exacte à dire>
```

## Étapes, clôture

1. **Relever l'état réel.** Aucune mémoire, que des commandes :
   `git status --short`, `git branch --show-current`, `git log --oneline -3`,
   `git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads`,
   `gh pr list --state open --json number,title,headRefName,baseRefName`,
   `gh run list --branch preprod --limit 1`.
   Preuve : les sorties, résumées.

2. **Signaler ce qui risque d'être perdu.**
   Fichiers non commités, commits non poussés, branche sans demande de fusion, CI rouge.
   Les dire en tête du rapport. Ne rien pousser, ne rien commiter, ne rien supprimer : c'est le rôle de feature et de livrer.

3. **Relire la session.**
   Ce qui a été décidé, fait, laissé en suspens. Les décisions qui ne sont pas encore dans `docs/decisions.md` : les lister comme "à écrire dans le prochain ticket".

4. **Écrire la passation.**
   `mkdir -p` du dossier, puis le fichier au format ci-dessus. Phrases courtes, liens et commandes exacts.
   Ticket en cours : `gh issue comment <numéro> --body-file <fichier>` avec les lignes En cours, En attente et Prochaine action.
   Preuve : le chemin du fichier, et le lien du commentaire s'il y en a un.

5. **Rapporter dans la conversation.** La passation entière, puis :
   "Session close. Pour reprendre, dites reprends."

## Étapes, reprise

1. Lire la passation la plus récente du dépôt : `ls -1 ~/.local/share/harness/passations/<nom-du-dépôt>/ | tail -n 1`.
   Aucune passation : le dire, et faire seulement l'étape 2.
2. Relever l'état réel, comme à l'étape 1 de la clôture.
3. Comparer. Ce qui a changé depuis la passation (fusion faite, CI passée, ticket fermé) : le dire.
4. Donner la prochaine action, une seule, avec la phrase exacte à dire à l'agent.
   Preuve : la passation lue, l'état relevé, les écarts.

## Point d'arrêt

Aucun. La clôture et la reprise ne modifient ni le code ni GitHub, sauf le commentaire de passation sur le ticket en cours.

## Preuve attendue

Clôture : le chemin de la passation, l'état relevé par commande, les risques. Reprise : la passation lue et les écarts avec l'état réel.

## Interdits

- Écrire la passation dans le dépôt du projet.
- Pousser, commiter, fusionner, supprimer une branche.
- Écrire un état de mémoire sans l'avoir relevé par commande.
- Mettre un secret, un extrait de `.env` ou de vraies données de personnes dans la passation ou le commentaire.
- Donner plus d'une prochaine action.
