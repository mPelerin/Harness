# Quel modèle pour quelle tâche

But : garder Fable pour ce qui compte vraiment, et économiser le crédit sur le reste.
Cette grille est un jugement, pas une mesure. On la corrige quand on aura vu la consommation réelle.

## Les trois niveaux

| Type de tâche | Modèle | Pourquoi |
| --- | --- | --- |
| Script qui modifie le système de l'utilisateur, relecture d'un skill ou outil tiers, conception d'un skill ou d'une architecture, décision difficile à défaire | Fable 5.2 | Une erreur casse quelque chose ou passe inaperçue |
| Script de contrôle, gabarit, configuration, revue de code | Opus 5.5 | Travail soigné, mais facile à vérifier ensuite |
| Guider une commande, lire une sortie, rédiger un README, un glossaire ou un récap | Sonnet 5.5 | Peu de réflexion, beaucoup d'échanges |

## Deux questions pour trancher

1. Une erreur serait-elle coûteuse à défaire ?
2. La tâche demande-t-elle beaucoup de réflexion ?

Deux oui : Fable. Un seul oui : Opus. Aucun : Sonnet.

## Règles de fonctionnement

- À la fin de chaque message, l'agent écrit une phrase : "Pour l'action suivante, utilisez Fable 5.2 / Sonnet 5.5 / Opus 5.5" (un seul des trois).
- L'agent ne peut pas changer de modèle lui-même. L'utilisateur change dans l'appli.
- Changer de modèle en cours de conversation est possible. Le nouveau modèle relit tout l'historique.
- Si la jauge baisse trop vite, l'agent le signale et descend d'un niveau quand la tâche le permet.

