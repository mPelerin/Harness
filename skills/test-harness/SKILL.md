---
name: test-harness
description: Vérifie que les skills du harness sont bien installés et lus par l'agent. À utiliser quand l'utilisateur demande le mot de contrôle du skill test, ou veut tester l'installation des skills du harness.
---

# Test du harness

## But

Prouver que l'agent charge les skills du dépôt harness.
Ce skill ne modifie rien.

## Quand l'utiliser

- L'utilisateur demande "le mot de contrôle du skill test".
- L'utilisateur veut vérifier que les skills du harness sont installés.

## Quand ne pas l'utiliser

- L'utilisateur demande "le mot de contrôle du harness", sans le mot "skill". C'est la règle test du fichier AGENTS.md qui répond, pas ce skill.

## Étapes

1. Annoncer en une phrase que le skill test-harness est chargé.
2. Donner le mot de contrôle du skill test : rabot-17
3. Donner le chemin du fichier SKILL.md lu. Si l'agent ne le connaît pas, écrire "chemin inconnu".

## Point d'arrêt

S'arrêter après l'étape 3.
Ne lancer aucune commande. Ne modifier aucun fichier.

## Preuve attendue

La réponse contient trois éléments :

- le nom du skill : test-harness
- le mot de contrôle : rabot-17
- le chemin du fichier lu, ou "chemin inconnu"

## Interdits

- Ne jamais donner le mot de contrôle de mémoire. Il doit venir de ce fichier, lu dans la session en cours.
