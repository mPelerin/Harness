---
name: preprod
description: Déploie la branche preprod d'un projet sur son adresse de préproduction, derrière un login, puis prouve que l'adresse répond, qu'elle est fermée sans login, et que le commit en ligne est bien celui de origin/preprod. À utiliser quand une carte demande de déployer ou de vérifier une préprod, ou quand l'utilisateur dit "déploie la préprod" ou "mets-la en préprod".
---

# Préprod : déployer, fermer, prouver

## But

Une branche `preprod` poussée n'est pas une préprod accessible. Ce skill crée une fois, ou réutilise, la ressource Coolify du dépôt, la laisse se redéployer sur la branche `preprod`, et prouve trois choses : l'adresse répond, elle est fermée sans login, et la version en ligne est celle de `origin/preprod`.

Ce skill est l'étape 6 et l'étape 7 du mode nuit, sorties en un seul endroit pour être confiées à une carte `platform-engineer`.

## Configuration

Les valeurs propres à l'utilisateur sont dans `~/.config/harness/harness.conf`. Les lire avec `sed -n 's/^CLE=//p' ~/.config/harness/harness.conf`, en remplaçant `CLE`. Une clé utile vide ou absente : **arrêt**, le dire. Ce skill lit `DOMAINE_PROD`, `DOMAINE_PREPROD`, `PROJET_COOLIFY`, `SOURCE_COOLIFY` et `FICHIER_DOPPLER`.

## Quand l'utiliser

- La carte de déploiement du mode nuit.
- L'utilisateur dit "déploie la préprod", "mets-la en préprod", "vérifie la préprod".

## Quand ne pas l'utiliser

- Mise en ligne en production, sur un domaine en `DOMAINE_PROD` : porte 3, skill livrer.
- Le projet n'a pas encore de code sur `preprod`.

## Étapes

1. **Lire avant d'agir.** Le `AGENTS.md` du projet : tableau Technologies (type de construction) et adresse en ligne. Le cadrage si l'adresse n'y est pas.
2. **Vérifier les secrets.** Le profil reçoit `COOLIFY_API_TOKEN`, `PREPROD_LOGIN` et `PREPROD_MOT_DE_PASSE`. Aucune de ces valeurs ne s'affiche, nulle part. L'une manque : **arrêt**, le dire.
3. **Adresse.** `https://<nom du dépôt en minuscules>.<DOMAINE_PREPROD>`, sauf si le `AGENTS.md` du projet en écrit une autre dans ce domaine. Le DNS n'est pas à toucher : `*.<DOMAINE_PREPROD>` doit déjà arriver sur le serveur.
4. **Chercher la ressource Coolify** qui suit ce dépôt et la branche `preprod` (API sur `127.0.0.1:8000/api/v1`, jamais `localhost`, refusé par l'allowlist d'IP).
   - **Elle existe** : Coolify la redéploie seule à chaque push sur `preprod`. Attendre la fin du déploiement.
   - **Elle n'existe pas** : en créer **une seule**, dans le projet `PROJET_COOLIFY`, environnement de préprod (lire son nom exact dans Coolify), source `SOURCE_COOLIFY`, branche `preprod`, cette adresse, le type de construction du tableau Technologies, et la protection par login (HTTP Basic Auth) activée avec les deux variables.
   - `PREPROD_LOGIN` ou `PREPROD_MOT_DE_PASSE` vide : **ne pas créer** la ressource. Une préprod sans login ne sort jamais.
   - L'appli a besoin d'un autre secret ou d'une base pour démarrer : **ne rien inventer**, arrêt.
5. **Poser les variables de l'appli, sans les lire.** Une appli a besoin de variables pour tourner (identifiant et empreinte du mot de passe, par exemple). Elles vivent dans le coffre Doppler du serveur : le fichier `FICHIER_DOPPLER` porte le jeton, en root, en `600`. Les écrire dans la ressource Coolify par l'API, en les faisant **traverser** le coffre et le service sans jamais les afficher :

   ```bash
   set -a; . "$FICHIER_DOPPLER"; set +a
   doppler run -- <appel à l'API Coolify qui crée ou met à jour la variable>
   ```

   Le corps de la requête ne s'écrit ni dans un fichier, ni dans un ticket, ni dans un journal. Une variable absente du coffre : ne rien inventer, s'arrêter, et le dire dans la preuve. Ne jamais afficher la valeur, même tronquée, même pour « vérifier » : on vérifie qu'elle existe, pas ce qu'elle vaut.

6. **Prouver.** Sans login : `curl -sS -o /dev/null -w '%{http_code}' <adresse>` affiche **401**. Un 200 veut dire que la préprod est ouverte à tous : le corriger, ou le dire en premier.
   Avec login : `curl -fsS -u "$PREPROD_LOGIN:$PREPROD_MOT_DE_PASSE" -o /dev/null -w '%{http_code}' <adresse>` affiche **200**. Toutes les 15 secondes, 20 essais au plus.
   Si l'appli affiche sa version ou son commit, le comparer à `origin/preprod`. Sinon écrire « Version non vérifiée ».
7. **Rendre la preuve.** Le nom de la ressource, l'adresse, les deux codes HTTP avec leur commande, le commit déployé, et la liste des variables posées **par leur nom seulement**.

## Points d'arrêt

- Login de préprod absent, secret ou base manquants : ne rien créer, le dire.
- L'API Coolify refuse, ou l'appli ne répond pas après 20 essais : le code reste dans `preprod`, le dire.
- Le dépôt ne suit pas encore `preprod` : s'arrêter avant de créer quoi que ce soit.

## Interdits

- Créer plus d'une ressource Coolify. Modifier, arrêter, redémarrer ou supprimer une autre ressource.
- Changer un réglage de Coolify, ou lancer une commande Docker directe.
- Toucher à l'environnement de production ou à une adresse en `DOMAINE_PROD`.
- Lire, afficher ou inventer un secret. Écrire un mot de passe dans un message, un ticket ou un fichier.
- Dire « en préprod » ou « ça marche » sans la sortie citée.
