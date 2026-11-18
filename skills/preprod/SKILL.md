---
name: preprod
description: Déploie la branche preprod d'un projet sur son adresse de préproduction, derrière un login, puis prouve que l'adresse répond, qu'elle est fermée sans login, et que le commit en ligne est bien celui de origin/preprod. Contrôle d'abord les prérequis Coolify (API, adresse autorisée, jeton, source GitHub). À utiliser quand une carte demande de déployer ou de vérifier une préprod, ou quand l'utilisateur dit "déploie la préprod" ou "mets-la en préprod".
---

# Préprod : déployer, fermer, prouver

## But

Une branche `preprod` poussée n'est pas une préprod accessible. Ce skill crée une fois, ou réutilise, la ressource Coolify du dépôt, la laisse se redéployer sur la branche `preprod`, et prouve trois choses : l'adresse répond, elle est fermée sans login, et la version en ligne est celle de `origin/preprod`.

Ce skill est l'étape 6 et l'étape 7 du mode nuit, sorties en un seul endroit pour être confiées à une carte `platform-engineer`.

## Configuration

Les valeurs propres à l'utilisateur sont dans `~/.config/harness/harness.conf`. Les lire avec `sed -n 's/^CLE=//p' ~/.config/harness/harness.conf`, en remplaçant `CLE`. Une clé utile vide ou absente : **arrêt**, le dire. Ce skill lit `DOMAINE_PROD`, `DOMAINE_PREPROD`, `PROJET_COOLIFY`, `SOURCE_COOLIFY`, `UUID_SOURCE_COOLIFY` et `FICHIER_DOPPLER`.

## Prérequis Coolify

Ils sont réglés **une seule fois, par l'utilisateur**. L'agent ne les règle jamais : un prérequis manque, c'est un arrêt, avec le nom du prérequis dans le message.

1. **L'API est activée.** Sur un Coolify auto-hébergé, un administrateur active l'accès à l'API dans les réglages avancés. Sinon la réponse est "API is disabled".
2. **L'adresse d'où l'on appelle est autorisée.** L'agent appelle depuis le serveur, sur `http://127.0.0.1:8000/api/v1`, jamais `localhost`. Quand Coolify tourne dans Docker, l'appel passe par `docker-proxy` : Coolify voit alors l'adresse de la passerelle de son réseau Docker, pas `127.0.0.1`. C'est cette adresse qu'il faut autoriser. Elle dépend de l'installation : elle ne s'écrit pas dans ce skill.
3. **Le jeton `COOLIFY_API_TOKEN` a les permissions `read`, `write` et `deploy`**, et son propriétaire est administrateur de l'équipe. Il n'est pas limité à un projet : sur l'instance vérifiée, un jeton limité à un projet recevait 403 "Only an admin can place resources on the server that runs Coolify".
4. **Dépôt privé : la source GitHub existe déjà dans Coolify.** Son identifiant est `UUID_SOURCE_COOLIFY`. Le jeton ne peut pas toujours lister les sources (403 sur `/api/v1/github-apps`, observé) : ne pas chercher à la lire, prendre la valeur de `harness.conf`.

Sources : documentation de Coolify, pages API Authorization et API Permissions (coolify.io/docs/api/authorization et coolify.io/docs/api/permissions), lues le 18/11/2026.

## Quand l'utiliser

- La carte de déploiement du mode nuit.
- L'utilisateur dit "déploie la préprod", "mets-la en préprod", "vérifie la préprod".

## Quand ne pas l'utiliser

- Mise en ligne en production, sur un domaine en `DOMAINE_PROD` : porte 3, skill livrer.
- Le projet n'a pas encore de code sur `preprod`.

## Étapes

1. **Lire avant d'agir.** Le `AGENTS.md` du projet : tableau Technologies (type de construction) et adresse en ligne. Le cadrage si l'adresse n'y est pas.
2. **Vérifier les secrets.** Le profil reçoit `COOLIFY_API_TOKEN`, `PREPROD_LOGIN` et `PREPROD_MOT_DE_PASSE`. Aucune de ces valeurs ne s'affiche, nulle part. L'une manque : **arrêt**, le dire.
3. **Contrôler les prérequis Coolify, en lecture seule.** Sans `set -x`, pour que le jeton ne s'écrive nulle part :

   ```bash
   curl -sS -o /dev/null -w '%{http_code}' \
     -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
     http://127.0.0.1:8000/api/v1/teams/current
   ```

   **200** : les prérequis 1 à 3 sont tenus. Autre code : relancer sans `-o /dev/null`, lire le message (il ne contient pas de secret), le citer, puis s'arrêter.

   | Réponse | Prérequis qui manque |
   | --- | --- |
   | "API is disabled" | 1, l'API n'est pas activée |
   | 403 qui refuse l'adresse | 2, l'adresse vue par Coolify n'est pas autorisée |
   | 403 "Only an admin can place resources…" | 3, jeton limité à un projet |
   | 401 | jeton absent, faux ou expiré |

   Preuve : le code, et la ligne du tableau si ce n'est pas 200.
4. **Adresse.** `https://<nom du dépôt en minuscules>.<DOMAINE_PREPROD>`, sauf si le `AGENTS.md` du projet en écrit une autre dans ce domaine. Le DNS n'est pas à toucher : `*.<DOMAINE_PREPROD>` doit déjà arriver sur le serveur.
5. **Chercher la ressource Coolify** qui suit ce dépôt et la branche `preprod`.
   - **Elle existe** : Coolify la redéploie seule à chaque push sur `preprod`. Attendre la fin du déploiement.
   - **Elle n'existe pas** : en créer **une seule**, dans le projet `PROJET_COOLIFY`, environnement de préprod (lire son nom exact dans Coolify), source `SOURCE_COOLIFY`, branche `preprod`, cette adresse, le type de construction du tableau Technologies, et la protection par login (HTTP Basic Auth) activée avec les deux variables.
   - **Dépôt privé** : `POST /api/v1/applications/private-github-app`. Champs : `project_uuid`, `server_uuid`, `environment_name`, `github_app_uuid` (= `UUID_SOURCE_COOLIFY`), `git_repository`, `git_branch` (= `preprod`), `build_pack`, `ports_exposes`. Lire `project_uuid` et `server_uuid` par l'API, sans les deviner. Lire le schéma exact de l'instance avant le premier appel.
   - **Dépôt public** : non vérifié. Lire la documentation de l'instance avant le premier appel, et le dire dans la preuve.
   - `PREPROD_LOGIN` ou `PREPROD_MOT_DE_PASSE` vide : **ne pas créer** la ressource. Une préprod sans login ne sort jamais.
   - L'appli a besoin d'un autre secret ou d'une base pour démarrer : **ne rien inventer**, arrêt.
   - **Pas de volume en préprod**, sauf si le `AGENTS.md` du projet en demande un. Les fichiers écrits par l'appli sont alors effacés à chaque redéploiement. Ce n'est pas un blocage : le dire dans la preuve.
6. **Poser les variables de l'appli, sans les lire.** Une appli a besoin de variables pour tourner (identifiant et empreinte du mot de passe, par exemple). Elles vivent dans le coffre Doppler du serveur : le fichier `FICHIER_DOPPLER` porte le jeton, en root, en `600`. Les écrire dans la ressource Coolify par l'API, en les faisant **traverser** le coffre et le service sans jamais les afficher :

   ```bash
   set -a; . "$FICHIER_DOPPLER"; set +a
   doppler run -- <appel à l'API Coolify qui crée ou met à jour la variable>
   ```

   Le corps de la requête ne s'écrit ni dans un fichier, ni dans un ticket, ni dans un journal. Une variable absente du coffre : ne rien inventer, s'arrêter, et le dire dans la preuve. Ne jamais afficher la valeur, même tronquée, même pour « vérifier » : on vérifie qu'elle existe, pas ce qu'elle vaut.

7. **Prouver.** Sans login : `curl -sS -o /dev/null -w '%{http_code}' <adresse>` affiche **401**. Un 200 veut dire que la préprod est ouverte à tous : le corriger, ou le dire en premier.
   Avec login : `curl -fsS -u "$PREPROD_LOGIN:$PREPROD_MOT_DE_PASSE" -o /dev/null -w '%{http_code}' <adresse>` affiche **200**. Toutes les 15 secondes, 20 essais au plus.
   Si l'appli affiche sa version ou son commit, le comparer à `origin/preprod`. Sinon écrire « Version non vérifiée ».
8. **Rendre la preuve.** Le code du contrôle des prérequis, le nom de la ressource, l'adresse, les deux codes HTTP avec leur commande, le commit déployé, et la liste des variables posées **par leur nom seulement**. Si l'appli écrit des fichiers en local : la phrase « Fichiers effacés à chaque redéploiement, pas de volume en préprod. »

## État de vérification

- **Vérifié une fois en conditions réelles** : création d'une ressource pour un dépôt privé, par une source GitHub, sur un Coolify auto-hébergé appelé depuis le serveur lui-même.
- **Non vérifié** : dépôt public, jeton d'une autre forme, Coolify Cloud, une autre version de Coolify. Dans ces cas, le dire dans la preuve.

## Points d'arrêt

- Login de préprod absent, secret ou base manquants : ne rien créer, le dire.
- Un prérequis Coolify manque (étape 3) : ne rien créer, nommer le prérequis, laisser l'utilisateur le régler.
- L'API Coolify refuse en cours de route, ou l'appli ne répond pas après 20 essais : le code reste dans `preprod`, le dire.
- Le dépôt ne suit pas encore `preprod` : s'arrêter avant de créer quoi que ce soit.

## Interdits

- Créer plus d'une ressource Coolify. Modifier, arrêter, redémarrer ou supprimer une autre ressource.
- Changer un réglage de Coolify : activation de l'API, adresses autorisées, permissions d'un jeton. Lancer une commande Docker directe.
- Contourner un refus 403. Un refus arrête la carte.
- Toucher à l'environnement de production ou à une adresse en `DOMAINE_PROD`.
- Lire, afficher ou inventer un secret. Écrire un mot de passe dans un message, un ticket ou un fichier.
- Dire « en préprod » ou « ça marche » sans la sortie citée.
