---
name: retro
description: Transforme une erreur en garde-fou pour qu'elle ne revienne pas. Établit les faits avec preuve, remonte à la cause, puis choisit le garde-fou le plus solide (contrôle automatique d'abord, règle écrite ensuite) et le pose par le bon circuit : un ticket dans le projet, ou une proposition pour le dépôt harness. À utiliser quand l'utilisateur dit "retro", "rétro", "bilan", "ça a encore planté", "pourquoi c'est arrivé", "plus jamais ça", ou quand une même erreur revient deux fois. Ne pas utiliser pour corriger le défaut lui-même (tickets puis feature) ni pour clore une session (cloture-session).
---

# Retro : une erreur, un garde-fou

## But

Une erreur payée une fois ne doit pas l'être deux fois.
Le résultat d'une retro n'est pas un texte : c'est un contrôle ou une règle, posé et prouvé.

## Quand l'utiliser

- L'utilisateur la demande.
- Une même erreur arrive pour la deuxième fois.
- Après un incident : CI rouge sur `preprod` après une fusion, mise en ligne cassée, porte 2 refusée deux fois.
- En fin de lot, si un ticket a demandé plus d'une correction : feature la propose en une ligne, sans la lancer.

## Quand ne pas l'utiliser

- Réparer le défaut : skill tickets (mode B), puis feature.
- Clore la session : skill cloture-session.

## Étapes

1. **Les faits.**
   Ce qui s'est passé, quand, sur quel commit, ticket ou demande de fusion. Avec la preuve : sortie, lien, `fichier:ligne`.
   Pas de coupable. On cherche le trou dans la méthode, pas la personne ni l'agent.
   Preuve : les faits, chacun avec sa preuve.

2. **La cause.**
   Demander "pourquoi" jusqu'à trois fois. Chaque réponse s'appuie sur une preuve.
   S'arrêter à la première cause sur laquelle on peut agir.
   Une cause non prouvée est écrite "hypothèse".
   Preuve : la chaîne des pourquoi.

3. **Le garde-fou, du plus solide au plus faible.**
   1. Un **contrôle automatique** : un test, une règle de lint, une étape de CI, un hook, un contrôle dans un script.
   2. Une **étape ou un interdit dans un skill** du harness.
   3. Une **ligne dans "Pièges connus"** du AGENTS.md du projet.
   4. Une **note au parking**, si rien d'autre n'est possible maintenant.
   Prendre le premier possible. Dire pourquoi les plus solides ne le sont pas.
   Preuve : le garde-fou choisi et sa place.

4. **Le poser par le bon circuit.**
   - **Dans le projet** : un ticket, par le skill tickets (mode B). Le garde-fou passe ensuite par feature et livrer, comme tout changement.
   - **Dans le dépôt harness, ou dans le dépôt d'instance de l'utilisateur** (voir la table "Où va un changement" du AGENTS.md du harness) : montrer le changement exact (fichier, ancien texte, nouveau texte). **POINT D'ARRÊT** : attendre le "go". Puis commit dans le dépôt harness, avec sa ligne dans `docs/retour-arriere.md`.
   - **Au parking** : une entrée datée dans le parking à idées de l'utilisateur.
   Preuve : le numéro du ticket, le commit, ou l'entrée du parking.

5. **Prouver que le garde-fou attrape l'erreur.**
   Pour un contrôle automatique : le faire tourner sur un cas qui reproduit l'erreur. Il doit être rouge.
   Pour une règle écrite : citer la ligne et l'endroit où l'agent la lira.
   Preuve : la sortie rouge, ou la ligne citée.

6. **Rapport, cinq lignes.** Fait, cause, garde-fou, où il vit, preuve.

## Point d'arrêt

- Avant tout changement dans le dépôt harness : "go" écrit de l'utilisateur.
- Un ticket passe par les arrêts du skill tickets.

## Preuve attendue

Le rapport de l'étape 6, avec un lien ou une commande pour chaque ligne.

## Interdits

- Finir une retro sans garde-fou posé ou noté.
- Écrire une règle quand un contrôle automatique est possible, sans dire pourquoi.
- Modifier le dépôt harness sans "go".
- Commiter directement sur `main` ou `preprod` d'un projet.
- Chercher un coupable. Écrire une cause sans preuve, sans le mot "hypothèse".
- Lire un fichier `.env` ou un secret.
