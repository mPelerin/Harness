---
name: retro
description: Transforme une erreur en garde-fou pour qu'elle ne revienne pas. Établit les faits avec preuve, remonte à la cause, puis choisit le garde-fou le plus solide (contrôle automatique d'abord, règle écrite ensuite) et le pose par le bon circuit : un ticket, une règle dans le AGENTS.md du dépôt, ou une entrée au parking à idées du vault. À utiliser quand l'utilisateur dit "retro", "ça a encore planté", "pourquoi c'est arrivé", "plus jamais ça", ou quand une même erreur revient deux fois. Ne pas utiliser pour corriger le défaut (tickets puis feature) ni clore la session (cloture-session).
---

# Retro : une erreur, un garde-fou

## But

Une erreur payée une fois ne doit pas l'être deux fois.
Le résultat d'une retro n'est pas un texte : c'est un contrôle ou une règle, posé et
prouvé. La leçon s'écrit là où le prochain projet la lira.

## Quand l'utiliser

- Une même erreur revient. L'utilisateur dit "retro", "plus jamais ça".

## Quand ne pas l'utiliser

- Corriger le défaut : tickets puis feature. Clore la session : cloture-session.

## Le projet et le code

Règles R1 à R3 et R6 du skill projet. Les preuves se lisent dans le dépôt `BASE`.

## Étapes

1. **Les faits.**
   Ce qui s'est passé, quand, sur quel commit, ticket ou demande de fusion. Avec la
   preuve : sortie, lien, `fichier:ligne`. Pas de coupable : on cherche le trou dans la
   méthode. Preuve : les faits, chacun avec sa preuve.

2. **La cause.**
   Demander "pourquoi" jusqu'à trois fois. Chaque réponse s'appuie sur une preuve.
   S'arrêter à la première cause sur laquelle on peut agir. Une cause non prouvée est
   écrite "hypothèse". Preuve : la chaîne des pourquoi.

3. **Le garde-fou, du plus solide au plus faible.**
   1. Un **contrôle automatique** : un test, une règle de lint, une étape de CI, un
      hook, un contrôle dans un script.
   2. Une **étape ou un interdit dans un skill** du harness.
   3. Une **ligne dans "Pièges connus"** de `AGENTS.md` (par un ticket, mode B).
   4. Une **note au parking** du vault, si rien d'autre n'est possible maintenant.
   Prendre le premier possible. Dire pourquoi les plus solides ne le sont pas.
   Preuve : le garde-fou choisi et sa place.

4. **Le poser par le bon circuit.**
   - **Dans le projet** : un ticket, par le skill tickets (mode B). Il passe ensuite par
     feature et livrer, comme tout changement.
   - **Dans le dépôt harness, ou le dépôt d'instance** (table "Où va un changement" du
     AGENTS.md du harness) : montrer le changement exact, ancien et nouveau texte.
     POINT D'ARRÊT : attendre le "go". Puis commit, avec sa ligne dans
     `docs/retour-arriere.md` du dépôt d'instance.
   - **Au parking** : une entrée datée dans `_Méthode/Parking à idées.md`, au format des
     entrées existantes, en fin de fichier. Rien n'est décidé au parking : l'utilisateur
     tranche.
   Preuve : le numéro du ticket, le commit, ou l'entrée du parking.

5. **Prouver que le garde-fou attrape l'erreur.**
   Contrôle automatique : le faire tourner sur un cas qui reproduit l'erreur. Rouge.
   Règle écrite : citer la ligne et l'endroit exact où l'agent la lira.
   Preuve : la sortie rouge, ou la ligne citée.

6. **Tenir la mémoire.**
   Si l'erreur a produit une panne visible, une ligne dans le tableau de
   `06 Qualité/<Nom> - Pannes` du vault : date, symptôme, cause racine, correction,
   ticket. Une décision qui en découle va au journal des décisions. Une leçon utile aux
   autres projets va aussi dans "Ce qu'on garde" de `08 Mise en ligne/<Nom> - Bilan`.
   Preuve : les notes relues.

7. **Rapport, cinq lignes.** Fait, cause, garde-fou, où il vit, preuve.

## Point d'arrêt

- Avant tout changement dans le dépôt harness : "go" écrit de l'utilisateur.
- Un ticket passe par les arrêts du skill tickets.

## Preuve attendue

Le rapport de l'étape 7, avec un lien ou une commande pour chaque ligne.

## Interdits

- Finir une retro sans garde-fou posé ou noté.
- Écrire une règle quand un contrôle automatique est possible, sans dire pourquoi.
- Modifier le dépôt harness sans "go".
- Commiter directement sur `main` ou sur `preprod`.
- Chercher un coupable, ou écrire une cause sans preuve sans le mot "hypothèse".
- Décider à la place de l'utilisateur au parking.
- Lire un fichier `.env` ou un secret.
