---
name: preprod
description: Déploie la branche preprod du projet sur son adresse de préproduction Coolify, derrière un login ou Cloudflare Access, puis prouve que l'adresse répond, qu'elle est fermée sans login, et que le commit en ligne est celui de origin/preprod. Les adresses se lisent dans la note projet du vault. Contrôle d'abord les prérequis Coolify. À utiliser quand une carte demande de déployer, ou quand l'utilisateur dit "déploie la préprod" ou "vérifie la préprod". Ne pas utiliser pour la production (livrer, porte 3).
---

# Préprod : déployer, fermer, prouver

## But

Une branche `preprod` poussée n'est pas une préprod accessible. Ce skill crée une fois,
ou réutilise, la ressource Coolify du dépôt, et prouve trois choses : l'adresse répond,
elle est fermée sans login, et la version en ligne est celle de `origin/preprod`.
Il tient la mémoire à jour : l'adresse de préprod s'écrit dans la note projet.

## Quand l'utiliser

- Une carte kanban demande de déployer ou de vérifier la préprod.
- L'utilisateur dit "déploie la préprod" ou "vérifie la préprod".

## Quand ne pas l'utiliser

- La production : skill livrer, porte 3.

## Le projet et le code

Règles R1 à R3 du skill projet. Lire la note projet (`depot`, `preprod`, peut être vide)
et `08 Mise en ligne/<Nom> - Déploiement`. L'appli est dans `code/` du dépôt : la
ressource Coolify se construit depuis le dossier de base `/code`.

## Configuration

Les valeurs sont dans `~/.config/harness/harness.conf`, lues clé par clé avec
`sed -n 's/^CLE=//p' ...`. Une clé utile vide ou absente : **arrêt**, le dire.
Ce skill lit `DOMAINE_PREPROD`, `PROJET_COOLIFY`, `SOURCE_COOLIFY`,
`UUID_SOURCE_COOLIFY`, `FICHIER_DOPPLER`, et `DOMAINE_PROD` pour le contrôle.

## Prérequis Coolify (réglés une fois par l'utilisateur)

L'agent ne les règle jamais. Un prérequis manque : **arrêt**, avec son nom.
1. L'API Coolify est activée.
2. L'adresse d'où l'on appelle est autorisée (appel sur `http://127.0.0.1:8000/api/v1`,
   jamais `localhost`).
3. Le jeton `COOLIFY_API_TOKEN` a les permissions `read`, `write`, `deploy`, et son
   propriétaire est administrateur.
4. Dépôt privé : la source GitHub existe dans Coolify, son identifiant est
   `UUID_SOURCE_COOLIFY`. Ne pas chercher à la lister par l'API.

## Étapes

1. **Vérifier les secrets.** Le profil reçoit `COOLIFY_API_TOKEN` et une protection :
   - Mode Access : `PREPROD_ACCESS_CLIENT_ID` et `PREPROD_ACCESS_CLIENT_SECRET`.
   - Mode login : `PREPROD_LOGIN` et `PREPROD_MOT_DE_PASSE`.
   Ni l'un ni l'autre complet : **arrêt**. Aucune valeur ne s'affiche, nulle part :
   ```bash
   for v in COOLIFY_API_TOKEN PREPROD_ACCESS_CLIENT_ID PREPROD_ACCESS_CLIENT_SECRET PREPROD_LOGIN PREPROD_MOT_DE_PASSE; do
     [ -n "${!v:+x}" ] && echo "$v présent" || echo "$v absent"; done
   ```

2. **Contrôler les prérequis, en lecture seule**, sans `set -x` :
   ```bash
   curl -sS -o /dev/null -w '%{http_code}' \
     -H "Authorization: Bearer $COOLIFY_API_TOKEN" http://127.0.0.1:8000/api/v1/teams/current
   ```
   200 : tout va bien. Autre code : relancer sans `-o /dev/null`, citer le message,
   s'arrêter. Preuve : le code HTTP.

3. **Adresse.** `https://<dépôt en minuscules>.<DOMAINE_PREPROD>`, sauf adresse écrite
   dans la note projet. Le DNS n'est pas à toucher.

4. **Chercher la ressource Coolify** qui suit ce dépôt et la branche `preprod`.
   - Elle existe : elle se redéploie seule à chaque push. Attendre la fin.
   - Elle n'existe pas : en créer **une seule**, dans le projet `PROJET_COOLIFY`,
     environnement de préprod, source `SOURCE_COOLIFY`, branche `preprod`, dossier de
     base `/code`, cette adresse. En mode login, activer le Basic Auth. En mode Access, ne pas l'activer.
     Dépôt privé : `POST /api/v1/applications/private-github-app`, en lisant
     `project_uuid` et `server_uuid` par l'API, jamais en les devinant.
     Aucune protection complète : **ne rien créer**. Secret ou base manquants : ne rien
     inventer, arrêt. Pas de volume en préprod, sauf demande écrite : le dire.

5. **Poser les variables de l'appli, sans les lire.** Elles traversent le coffre Doppler
   (`FICHIER_DOPPLER`) : `set -a; . "$FICHIER_DOPPLER"; set +a; doppler run -- <appel
   API>`. Le corps de la requête ne s'écrit nulle part. Une variable absente du coffre :
   ne rien inventer, s'arrêter, le dire. On vérifie qu'une variable existe, jamais ce
   qu'elle vaut.

6. **Prouver.** Un 200 sans login veut dire que la préprod est ouverte à tous : le
   corriger, ou le dire en premier.
   - Mode Access : sans jeton, 302 vers `cloudflareaccess.com` (ne citer que l'adresse
     avant le `?`). Avec jeton, en-têtes passés par `<( )` : 200 attendu.
   - Mode login : 401 sans login, 200 avec `curl -fsS -u "$PREPROD_LOGIN:$PREPROD_MOT_DE_PASSE"`.
   Dans les deux modes, toutes les 15 secondes, 20 essais au plus.
   Comparer la version affichée à `origin/preprod`, sinon "Version non vérifiée".

7. **Tenir la mémoire**, par un commit mémoire (règle R3 du skill projet) : `preprod:
   <adresse>` dans la note projet ; dans `08 Mise en ligne/<Nom> - Déploiement`, la ligne
   préproduction du tableau (adresse, branche `preprod`).
   Preuve : le commit mémoire poussé, les deux notes relues.

8. **Rendre la preuve.** Le code du contrôle, le nom de la ressource, l'adresse, les
   deux codes HTTP avec leur commande, le commit déployé, la liste des variables posées
   **par leur nom seulement**. Appli qui écrit des fichiers en local : "Fichiers effacés
   à chaque redéploiement, pas de volume en préprod."

## État de vérification

- Vérifié une fois en conditions réelles : création d'une ressource pour un dépôt
  privé, sur un Coolify auto-hébergé appelé depuis le serveur lui-même.
- Mode Access vérifié le 19/11/2026 depuis le serveur : 200 avec jeton, 302 sans jeton,
  401 avec un faux jeton. Piège : si le domaine nu d'Access est couvert, il doit exister
  dans le DNS, sinon `DNS_PROBE_FINISHED_NXDOMAIN`.
- Non vérifié : dépôt public, Coolify Cloud, autre version. Le dire dans la preuve.

## Points d'arrêt

- Protection incomplète, secret ou base manquants : ne rien créer, le dire.
- Un prérequis Coolify manque : le nommer, laisser l'utilisateur le régler.
- L'API refuse en cours de route, ou l'appli ne répond pas après 20 essais : le dire.
- Le dépôt ne suit pas `preprod` : s'arrêter avant de créer quoi que ce soit.

## Preuve attendue

Le bloc de l'étape 8, complet, et le commit mémoire de l'étape 7.

## Interdits

- Créer plus d'une ressource. Modifier, arrêter ou supprimer une autre ressource.
- Changer un réglage de Coolify. Lancer une commande Docker directe.
- Contourner un refus 403. Toucher à la production ou à une adresse en `DOMAINE_PROD`.
- Lire, afficher ou inventer un secret. Écrire un mot de passe dans un message.
- Dire "en préprod" ou "ça marche" sans la sortie citée.
