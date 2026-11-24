---
name: tickets
description: Crée, relit et corrige les tickets d'un projet. Transforme les stories du vault en issues GitHub, chacune avec sa note dans 05 Tickets/ copiée du modèle Ticket, dans l'ordre du Plan de travail. Un ticket confié à Hermès part seul chez l'orchestrateur quand sa note porte le feu vert. Crée aussi un ticket isolé pour un bug ou une petite fonction, et corrige un ticket flou. À utiliser quand l'utilisateur dit "tickets", "crée les tickets", "découpe en tickets", "crée un ticket", "ouvre une issue", "relis le ticket 12" ou "il y a un bug". Ne pas utiliser pour cadrer (cadrage) ni réaliser un ticket (feature).
---

# Tickets : découper le travail

## But

Des tickets que n'importe quel agent réalise sans deviner. Chaque ticket existe deux
fois : l'issue GitHub, pour la discussion, et la note du vault, qui porte le plan, le
journal et la fiche QA. **Un ticket = un changement = un commit.**
Le "go" à la création est la porte 1 du ticket (`_Méthode/Portes.md`). Un ticket
sensible (argent, droits, données personnelles, base, nouvelle bibliothèque) le dit :
il attendra un second "go" écrit avant le code.

## Quand l'utiliser

- Les stories sont validées et le dépôt existe.
- Un bug, une petite fonction, un ticket à relire. « Lance le ticket N » : retrouver sa note et son issue, vérifier le numéro et les prérequis, puis écrire `execution: À exécuter` dans le coffre. Si le numéro est ambigu, demander lequel.

## Quand ne pas l'utiliser

- Idée floue qui demande plus d'un ticket : skill cadrage.
- Réaliser le ticket : skill feature.

## Le projet

Règles R1 à R4 du skill projet. `gh` se lance à la racine de `BASE`. Pas de dépôt
(`depot` vide dans la note projet) : **arrêt**, le cadrage n'est pas allé au bout.
Les notes de ticket s'écrivent dans le vault : c'est ce qui prévient Hermès.

## Ce qu'est un bon ticket

- Une tranche verticale (écran, logique, données) pour un petit résultat visible.
- Un seul changement, dit en une phrase sans "et aussi". Une demi-journée d'agent au plus.
- Des conditions vérifiables : "le bouton Exporter télécharge un CSV", pas "l'export marche".
- Dans "Le ticket" de la note et dans l'issue : `Dépend de : #<n>`, `Hors périmètre :`,
  `Sensible : <quoi>` ou `Sensible : non`, `Prérequis : NOM (coffre)`, `NOM (GitHub dev)`,
  compte, migration, ou `Prérequis : aucun`. Des noms, jamais une valeur. Le pré-vol les lit.

## Étapes, mode A : des stories aux tickets

1. **Lire**, dans `02 Cadrage/` et `04 Conception/` : Stories (la matière), Priorités et
   **Plan de travail** (l'ordre, les lots, les dépendances), **Specs** (les tâches déjà
   découpées), **Sécurité** (ce qui rend un ticket sensible). Arrêt si Stories est vide.
   Preuve : les stories, numéro et titre, et les lots du plan.

2. **Lire les issues ouvertes.** `gh issue list --state open --limit 30`. Repérer les
   doublons. Preuve : la liste.

3. **Ticket socle.** Si `AGENTS.md` dit "à définir" sous Commandes de vérification, le
   premier ticket est le socle, d'après **Contraintes techniques** : installer la pile
   écrite là, rien de plus ; écrire la commande `verifier` dans `AGENTS.md` ; ajouter la
   CI (`.github/workflows/ci.yml`, qui lance cette commande dans `code/`) ; activer les
   hooks du harness. Tous les autres tickets en dépendent.

4. **Proposer le découpage. POINT D'ARRÊT.** Un tableau : ordre, titre, story, lot,
   résultat visible, dépend de, sensible, conditions. Chaque condition de chaque story est
   couverte. Une ligne à deux changements est coupée avant de montrer.
   « Go » valide la création en attente. « Lance N » autorise uniquement ce ticket. Preuve : le tableau, et la réponse.

5. **Créer issue puis note, ticket par ticket, dans l'ordre des dépendances.**
   Une dépendance est créée avant, pour citer son vrai numéro.
   ```bash
   F=$(mktemp); # corps : besoin, conditions, Dépend de, Hors périmètre, Sensible, Prérequis
   gh issue create --title "<titre>" --label enhancement --body-file "$F"
   ```
   Le numéro est le dernier nombre de l'adresse rendue. Jamais un numéro déduit : les
   demandes de fusion prennent la même suite. Puis ajouter au corps la ligne
   `Note : <Nom>/05 Tickets/<Nom> - T<n> <titre>.md` et `gh issue edit <n> --body-file "$F"`.
   Copier `_Modèles/Notes/Ticket.md` en `05 Tickets/<Nom> - T<n> <titre court>.md`.
   Propriétés : `projet`, `type: ticket`, `statut: a-faire`, `agent: hermes` ou
   `agent: local` (le mode nuit écrit `agent: hermes-nuit`), `numero`, `issue`, `branche: ""`, `resume`,
   `haut: "[[<Nom> - 05 Tickets]]"`, `source` (la story, ou la spec qui l'a produit).
   Rédiger la note complète avec `execution: En attente`. Ajouter l’issue au GitHub Project lié
   (`gh project item-add <numéro-projet> --owner <compte> --url <issue>`).
   Après relecture, seul un accord explicite sur le ticket ou le lot permet de passer à
   `execution: À exécuter`. L’utilisateur peut aussi changer cette valeur dans Obsidian.
   Une note ancienne sans cette propriété reste en attente.
   Preuve : par ticket, le lien de l'issue et le chemin de la note.

6. **Relire** chaque ticket avec le mode C, étape 1.

7. **Bilan et passation.** Tableau story, tickets, notes. Aucune story sans ticket.
   En local, donner un prompt pour le skill feature dans une nouvelle conversation,
   avec le dossier du projet et les numéros des tickets prêts.
   Avec Hermès : "Le serveur transmet les tickets autorisés dès réception de leur note dans le coffre."

## Étapes, mode B : un ticket isolé

1. Reformuler en deux phrases, confirmer. Bug : demander les étapes de reproduction.
2. Montrer le ticket complet. POINT D'ARRÊT : "go" ou "go hermes".
3. Créer comme au mode A, étape 5. Étiquette `bug` ou `enhancement`. `source` : la note
   qui a motivé le ticket, ou la note projet.
4. Relire, mode C. Preuve : le numéro créé et la relecture.

## Étapes, mode C : relire et corriger

1. **Relire.** `gh issue view <n> --json number,title,body,labels,state`, et la note.
   Grille : qui, quoi, pour quoi ; conditions vérifiables ; hors-périmètre écrit ; un seul
   changement ; une demi-journée ; sensible signalé ; prérequis déclarés ; la story citée
   existe ; les "Dépend de" existent. Preuve : une ligne par point.
2. **Proposer la correction. POINT D'ARRÊT.** Ancien et nouveau, rubrique par rubrique.
   Trop gros : couper, le ticket d'origine garde le premier changement.
3. **Corriger.** `gh issue edit <n> --body-file "$F"`, la même correction dans la note,
   puis `gh issue comment <n> --body "Ticket corrigé : <en une phrase>."`.
   Preuve : l'issue et la note relues.

## Point d'arrêt

- Rien n'est créé ni modifié sans "go". Ticket fermé : en créer un neuf qui le cite.

## Preuve attendue

Les numéros et liens des issues, les chemins des notes, la relecture. Mode A : chaque
story reliée à au moins un ticket, l'ordre tiré du Plan de travail.

## Interdits

- Créer ou modifier sans "go". Fermer un ticket : c'est livrer.
- Écrire `Closes`, `Fixes` ou `Resolves` devant un numéro.
- Supposer un numéro. Créer la note avant l'issue.
- Réinventer la note au lieu de copier le modèle.
- Écrire la valeur d'un secret, ou de vraies données de personnes. Écrire du code.
