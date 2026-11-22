---
name: cloture-session
description: Clôt une session de travail et écrit la passation, ou reprend une session à partir de la dernière passation. En clôture, relève l'état réel, écrit une passation hors du dépôt, écrit un compte rendu dans 09 Journal/ du vault depuis le modèle Compte rendu, et met à jour la phase du projet. En reprise, relit la passation et l'état, puis donne la prochaine action. À utiliser quand l'utilisateur dit "/fini", "on s'arrête", "clôture", "passation", "reprends" ou "où j'en suis". Ne pas utiliser pour tirer une leçon d'une erreur (retro).
---

# Clôture de session : rien ne se perd entre deux sessions

## But

Qu'une session neuve, avec n'importe quel agent, reparte en une minute.
La passation dit l'état réel, prouvé. Le compte rendu, lui, vit dans le vault, dans
`09 Journal/`, copié du modèle `_Modèles/Notes/Compte rendu.md`.

## Quand l'utiliser

- Fin de session : "/fini", "on s'arrête". Reprise : "reprends", "où j'en suis".

## Quand ne pas l'utiliser

- Tirer une leçon d'une erreur : retro.

## Le projet et le code

Règles R1 à R3 du skill projet. L'état Git se relève dans `BASE` et dans les worktrees
(`git -C "$BASE" worktree list`). Le compte rendu s'écrit dans `09 Journal/` du vault :
le service mémoire du serveur le commite.

## La passation

Elle vit hors du dépôt, pour ne jamais le salir :
`~/.local/share/harness/passations/<nom-du-dépôt>/<AAAA-MM-JJ-HHMM>.md`.
Si un ticket est en cours, un résumé court va aussi en commentaire de l'issue.

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

1. **Relever l'état réel.** Aucune mémoire, que des commandes, dans `BASE` et chaque
   worktree : `git status --short`, `git branch --show-current`, `git log --oneline -3`,
   `gh pr list --state open`, `gh run list --branch preprod --limit 1`.
   Preuve : les sorties, résumées.

2. **Signaler ce qui risque d'être perdu.** Fichiers non commités, commits non poussés,
   branche sans demande de fusion, CI rouge. En tête du rapport. Ne rien pousser, ne
   rien commiter : c'est le rôle de feature et de livrer.

3. **Relire la session.** Ce qui a été fait, décidé, laissé en suspens.
   Les décisions pas encore au journal des décisions du vault, y compris celles des
   rubriques "Décisions" des tickets fusionnés : les écrire dans la table du journal,
   datées, avec le ticket dans la colonne Détail.

4. **Écrire le compte rendu dans le vault.**
   Copier `_Modèles/Notes/Compte rendu.md` dans
   `09 Journal/<Nom> - CR <AAAA-MM-JJ> <sujet>.md`.
   Propriétés : `projet`, `type: journal`, `statut: valide`, `resume`, `haut: "[[<Nom> - 09 Journal]]"`,
   `source: "[[<Nom>]]"`.
   Remplir : Ce qui a été fait. Ce qui a été décidé, chaque décision aussi reportée au
   journal des décisions. Ce qui reste.
   Une décision lourde prend sa propre note depuis `_Modèles/Notes/Décision.md`, dans
   `07 Décisions/`, liée dans la colonne Détail.
   Puis mettre à jour la note projet si la `phase` a changé pendant la session.
   Ne jamais écrire `avancement` : il est calculé par le récap. Une idée hors sujet de
   la session : une entrée au parking (règle R6).
   Preuve : le chemin du compte rendu, la note projet relue.

5. **Écrire la passation.** `mkdir -p` du dossier, puis le fichier au format ci-dessus.
   Ticket en cours : `gh issue comment <numéro> --body-file <fichier>` avec En cours,
   En attente, Prochaine action. Preuve : le chemin, et le lien du commentaire.

6. **Rapporter.** La passation entière, le chemin du compte rendu, puis :
   "Session close. Pour reprendre, dites reprends."

## Étapes, reprise

1. Lire la passation la plus récente :
   `ls -1 ~/.local/share/harness/passations/<nom-du-dépôt>/ | tail -n 1`.
   Aucune : le dire, et faire seulement l'étape 2.
2. Relever l'état réel, comme à l'étape 1.
3. Lire `<Nom> - GitHub` (récap généré) et le dernier compte rendu de `09 Journal/`,
   et comparer avec l'état réel. Ce qui a changé depuis : le dire.
4. Donner la prochaine action, une seule, avec la phrase exacte à dire.
   Preuve : la passation et le compte rendu lus, les écarts.

## Point d'arrêt

Aucun. Clôture et reprise ne modifient ni le code ni GitHub, sauf le commentaire de
passation sur l'issue en cours.

## Preuve attendue

Clôture : le chemin de la passation, le chemin du compte rendu, l'état relevé par
commande, les risques. Reprise : la passation et le compte rendu lus, les écarts.

## Interdits

- Écrire la passation dans le dépôt de code.
- Pousser, commiter, fusionner, supprimer une branche.
- Écrire un état de mémoire sans l'avoir relevé par commande.
- Écrire `avancement` dans la note projet : il est calculé.
- Réinventer le compte rendu au lieu de copier le modèle.
- Mettre un secret, un extrait de `.env` ou de vraies données de personnes.
- Donner plus d'une prochaine action.
