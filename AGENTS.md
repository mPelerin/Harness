# Règles du harness

Ces règles valent pour tous les agents et tous les projets.
Si le fichier AGENTS.md d'un projet dit autre chose, c'est lui qui gagne pour ce projet.

L'installeur ajoute à la suite le profil de l'utilisateur : son prénom, sa façon de travailler et de recevoir les réponses. Le profil précise ces règles, il ne les annule pas.

## Recherche préalable

- Dès que le sujet touche un marché, un outil ou une règle, faire une courte recherche web avant de répondre.
- Chercher trois choses : ce qui existe déjà, ce qui se fait couramment, ce qui n'est pas possible.
- Citer les sources et leurs dates.

## Travailler

- Avant toute question, lire ce qui existe déjà dans le projet : AGENTS.md du projet, README, dossier docs/. Ne demander à l'utilisateur que ce qui n'est écrit nulle part.
- Pour un projet ou un gros travail, cadrer d'abord le besoin et les bonnes pratiques : poser les questions qui restent avant de produire. Pour une demande simple, répondre directement.
- Une réponse de l'utilisateur qui resservira est notée dans le dossier docs/ du projet, pour ne jamais la redemander.
- Une modification à la fois, testée avant la suivante.
- Chaque "ça marche" vient avec sa preuve : la commande lancée et la sortie obtenue.
- Séparer le vérifié, l'hypothèse et la recommandation.
- Une nouvelle idée va dans le parking à idées. L'utilisateur décide si on la lance.

## Changer de conversation

- En échange avec l'utilisateur, à la fin d'une phase ou d'un skill utilisé comme
  étape principale, terminer par un court prompt de reprise prêt à copier. La
  conversation suivante commence dans le dossier du projet avec ce prompt.
- Indiquer dans le prompt le projet et son dossier exact, le prochain skill et
  son point de reprise, les notes ou liens utiles et tout accord encore attendu.
  Utiliser les références vérifiées. Garder les secrets hors du prompt. En début
  de reprise, relire ces références et vérifier l'état avant d'agir.
- S'arrêter après le prompt. Un feu vert encore attendu doit venir de l'utilisateur
  dans la nouvelle conversation. Les contrôles utilisés à l'intérieur d'un skill
  et les cartes Hermès continuent selon leur propre procédure.
- Dans Claude Code, faire copier le prompt avant de suggérer `/clear`. Sur une
  autre interface, indiquer d'ouvrir une nouvelle conversation dans le projet.

## Déployer sur le serveur

- Autorisé : créer et déployer une nouvelle appli dans son propre conteneur, via Coolify.
- Jamais tête baissée. Avant le premier déploiement d'une appli, cadrer : lire les documents du projet, poser à l'utilisateur les seules questions qui restent, écrire le plan de déploiement, ne rien créer avant ses réponses.
- Une fois le plan validé, l'appli du projet en cours se redéploie sans redemander. Ses conteneurs peuvent alors être remplacés ou relancés.
- Redéployer passe toujours par le circuit prévu : push sur GitHub (GitHub Action) ou redéploiement de cette appli dans Coolify. Jamais par une commande Docker directe.
- Après un redéploiement, vérifier que l'appli répond et donner la preuve.
- Tout le reste du serveur est protégé (voir les interdits).

## Branches et déploiement

- Deux branches durables par projet, jamais trois : `main` et `preprod`.
- `main` est la production. Elle publie sur `DOMAINE_PROD`. Rien ne s'y écrit directement : une mise en ligne est une fusion de `preprod` vers `main`.
- `preprod` découle de `main` et ne le remplace jamais. Elle publie sur `DOMAINE_PREPROD`, derrière un login.
- **La branche par défaut d'un dépôt GitHub est toujours `main`.** Jamais `preprod`. GitHub prend la première branche poussée comme branche par défaut : un dépôt neuf pousse donc `main` en premier, avec au moins un commit, puis crée `preprod` à partir d'elle.
- Les deux domaines viennent de `config/harness.conf` (`DOMAINE_PROD` et `DOMAINE_PREPROD`). Ils ne s'écrivent jamais en dur dans un projet.
- Contrôle avant de dire qu'un dépôt est prêt : `gh repo view <compte>/<dépôt> --json defaultBranchRef` affiche `main`. Sinon : `gh repo edit <compte>/<dépôt> --default-branch main`.

## Interdits

- Ne jamais afficher, recopier ni citer un secret (clé, jeton, mot de passe), même tronqué, même « pour vérifier ». Un secret traverse directement le coffre et le service (`doppler run -- …`) : il ne passe ni par la conversation, ni par un journal, ni par un fichier. On vérifie qu'une variable existe, jamais ce qu'elle vaut.
- Ne jamais modifier, arrêter ni supprimer un conteneur ou un service qui n'appartient pas à l'appli du projet en cours.
- Ne jamais changer les réglages de Docker ni de Coolify.
- Ne rien installer de tiers sans montrer son contenu et son origine. Version fixée, jamais "latest".
- Ne jamais dire qu'une chose est faite ou sauvegardée sans l'avoir vérifié.

## Où va un changement du harness

Le harness vit dans deux dépôts. Le dépôt `harness` est le moteur, commun à tous. Le dépôt d'instance de l'utilisateur garde sa configuration et son profil. Le moteur ne connaît jamais l'instance.

| Le changement… | Va dans |
| --- | --- |
| améliore la méthode pour tout le monde | `harness` |
| contient un nom, une adresse, un serveur, le profil de l'utilisateur | le dépôt d'instance |
| les deux | `harness` avec une variable, la valeur dans `harness.conf` |

Au moindre doute, le changement va dans le dépôt d'instance.

## Règle test

Si on te demande le mot de contrôle du harness, réponds exactement : copeau-42
