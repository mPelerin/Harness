---
name: tickets
description: Crée, relit et corrige les tickets GitHub d'un projet. Transforme les user stories de docs/cadrage/stories.md en tickets fins qui traversent toute l'appli, crée un ticket isolé pour un bug ou une petite fonction, ou corrige un ticket flou. À utiliser quand l'utilisateur dit "tickets", "crée les tickets", "découpe en tickets", "crée un ticket", "ouvre une issue", "relis le ticket 12", "corrige le ticket" ou "il y a un bug". Ne pas utiliser pour cadrer une idée floue (cadrage) ni pour réaliser un ticket (feature).
---

# Tickets : créer, relire, corriger

## But

Des tickets GitHub que n'importe quel agent peut réaliser sans deviner.
Chaque ticket est petit, livrable seul, et finit par des conditions que l'utilisateur peut vérifier.
**Un ticket = un changement = un commit.** C'est ce skill qui le garantit, en découpant.
Ce skill n'écrit rien dans le dépôt. Il travaille seulement sur les tickets GitHub.
**Le "go" de l'utilisateur à la création vaut porte 1** pour les tickets qui ne touchent ni à l'argent, ni aux droits d'accès, ni aux données personnelles, ni à la base, ni à une nouvelle bibliothèque. Feature les code ensuite sans redemander.
Un ticket sensible le dit dans ses Notes (`Sensible : <quoi>`) : feature attendra un "go" écrit avant de le coder.

## Quand l'utiliser

- Des user stories validées dans `docs/cadrage/stories.md`, à transformer en tickets.
- Un bug ou une petite fonction à noter en ticket.
- Un ticket existant à relire ou à corriger, par exemple quand feature l'a jugé flou.

## Quand ne pas l'utiliser

- Idée floue, sans stories, qui demande plus d'un ticket : skill cadrage.
- Réaliser le ticket : skill feature.

## La branche de base

C'est toujours `preprod`. Les tickets partent de `preprod` et y reviennent. `main` ne reçoit que des mises en ligne.
Chaque ticket l'écrit dans ses Notes. Feature y crée sa branche.
Arrêt si `git ls-remote --heads origin preprod` ne renvoie rien : le cadrage n'est pas fait.

## Ce qu'est un bon ticket

- **Une tranche verticale** : il traverse toutes les couches utiles (écran, logique, données) pour un petit résultat visible.
  Exemple de chantier : poser un petit meuble complet, plutôt que tous les caissons de la cuisine puis toutes les portes.
- **Un seul changement.** Il se dit en une phrase, sans "et aussi". Il donnera un seul commit.
  Si deux parties pourraient être livrées l'une sans l'autre, ce sont deux tickets.
  Exemple : "ajouter l'export CSV" et "renommer le menu" font deux tickets, même s'ils sont petits.
- **Une demi-journée de travail d'agent au plus.** Plus gros : le couper.
- **Le modèle du projet** : `.github/ISSUE_TEMPLATE/fonction.md` ou `bug.md`.
- **Des conditions vérifiables** : "le bouton Exporter télécharge un fichier CSV", pas "l'export marche bien".
- **Ses liens, dans les Notes** :
  - `Story : docs/cadrage/stories.md, S3` quand il vient d'une story.
  - `Branche de base : preprod`.
  - `Dépend de : #<numéro>` quand il en dépend.
  - `Prérequis : <noms de variables, compte, migration, service>` quand il en faut avant de coder, ou `Prérequis : aucun`. Des noms seulement, jamais une valeur. Pour une variable, écrire son lieu : `NOM (coffre)`, `NOM (GitHub dev)`, `NOM (GitHub depot)`. Le pré-vol s'en sert avant de lancer le codage ou la nuit.
  - `Sensible : <argent, droits, données personnelles, base, bibliothèque>` quand il en touche.

## Étapes, mode A : des stories aux tickets

1. **Lire les stories.**
   `git fetch origin`, puis `git show origin/preprod:docs/cadrage/stories.md`. Lire aussi `prd.md` et `ux.md` du même dossier.
   Arrêt si le fichier manque sur GitHub : le cadrage n'est pas passé par la porte 1. Retour au skill cadrage.
   Preuve : la liste des stories, numéro et titre.

2. **Lire le code et les tickets ouverts.** `gh issue list --state open --limit 30`.
   Repérer ce qui existe déjà et les tickets en double.
   Preuve : la liste de ce qui existe, en `chemin:ligne` ou numéro de ticket.

3. **Proposer le découpage. POINT D'ARRÊT.**
   Un tableau : ordre, titre, story, résultat visible, dépend de, conditions "C'est fini quand".
   Une story peut donner plusieurs tickets. Chaque condition de chaque story est couverte par au moins un ticket : le dire, story par story.
   Chaque ligne du tableau porte un seul changement. Une ligne qui en contient deux est coupée avant de montrer le tableau.
   Attendre le "go". Corriger et remontrer tant que l'utilisateur demande des changements.
   Preuve : le tableau, et le "go" de l'utilisateur.

4. **Créer les tickets, dans l'ordre des dépendances.**
   Pour chacun : corps écrit dans un fichier temporaire (`F=$(mktemp)`), puis
   `gh issue create --title "<titre>" --label enhancement --body-file "$F"`.
   Un ticket qui dépend d'un autre est créé après lui, pour citer son vrai numéro.
   **Le numéro est celui que la commande rend** : `gh issue create` affiche l'adresse, son dernier nombre est le numéro. Ne jamais le déduire du dernier ticket vu : les demandes de fusion prennent les mêmes numéros, donc la suite saute.
   Relire le numéro rendu avant de créer le suivant.
   Preuve : la liste des numéros et des liens créés, chacun avec la sortie de `gh issue create`.

5. **Faire le bilan.**
   Un tableau story, tickets créés. Aucune story sans ticket.
   Annoncer : "Tickets créés. Dites feature tout, ou feature et des numéros (feature 2 3 4)."
   Preuve : le tableau, avec les liens.

6. **Relire ce qui a été créé.** Mode C, étape 1, sur chaque ticket.

## Étapes, mode B : un ticket isolé

1. Reformuler le bug ou la fonction en deux phrases. Confirmer avec l'utilisateur.
2. Bug : demander les étapes pour reproduire, si elles manquent. Ne pas les inventer.
3. Trouver la branche de base. Montrer le ticket complet. **POINT D'ARRÊT** : attendre le "go".
4. Créer avec `gh issue create`, étiquette `bug` ou `enhancement`. Lire le numéro dans la sortie, jamais un numéro supposé.
5. Relire avec le mode C, étape 1.
   Preuve : le numéro créé et le résultat de la relecture.

## Étapes, mode C : relire et corriger

1. **Relire.** `gh issue view <numéro> --json number,title,body,labels,state`, puis passer la grille :
   - Le besoin dit qui, quoi, pour quel résultat.
   - Chaque condition de "C'est fini quand" est vérifiable par l'utilisateur.
   - Le hors-périmètre est écrit, même "rien".
   - Il porte un seul changement, qui tiendra dans un seul commit.
   - Il tient en une demi-journée d'agent.
   - Argent, droits d'accès, données personnelles : signalés s'ils sont touchés.
   - Les prérequis bloquants sont déclarés : noms de variables, compte, migration, service. Ou `Prérequis : aucun`.
   - La branche de base est écrite, et c'est la bonne.
   - La story citée existe dans `stories.md`. Les tickets de "Dépend de" existent.
   Preuve : la grille, une ligne par point, conforme ou écart.

2. **Proposer la correction. POINT D'ARRÊT.**
   Montrer l'ancien texte et le nouveau, rubrique par rubrique.
   Trop gros, ou plusieurs changements : proposer de le couper. Le ticket d'origine garde le premier changement, les autres deviennent des tickets neufs qui le citent.
   Preuve : le "go" de l'utilisateur.

3. **Corriger.** `gh issue edit <numéro> --body-file "$F"`.
   Puis `gh issue comment <numéro> --body "Ticket corrigé : <ce qui a changé, en une phrase>."`, pour garder la trace.
   Preuve : `gh issue view <numéro>` relu après la modification.

## Point d'arrêt

- Rien n'est créé ni modifié sur GitHub sans "go".
- Ticket fermé : ne pas le modifier. En créer un neuf qui le cite.

## Preuve attendue

- Les numéros et liens des tickets créés ou corrigés.
- Leur relecture après coup, sur GitHub.
- En mode A : chaque story reliée à au moins un ticket.

## Interdits

- Créer ou modifier un ticket sans "go".
- Fermer un ticket. C'est le rôle du skill livrer, à la main après la fusion dans `preprod`, ou de l'utilisateur.
- Écrire `Closes`, `Fixes` ou `Resolves` devant un numéro : un ticket ne se ferme jamais tout seul.
- Créer un ticket qui réunit plusieurs changements indépendants.
- Modifier les fichiers de `docs/cadrage/` : c'est le rôle du skill cadrage.
- Effacer le texte d'un ticket sans laisser de commentaire de trace.
- Inventer des étapes de reproduction ou des conditions.
- Supposer un numéro au lieu de lire celui que la commande rend.
- Omettre un prérequis bloquant, ou écrire la valeur d'un secret à sa place.
- Mettre de vraies données de personnes, un secret ou un extrait de `.env` dans un ticket.
- Écrire du code.
