<!--
  Adapté de kit-agents-ia, Mathis Gorvien, licence MIT (voir LICENCES-TIERS.md).

  MODE D'EMPLOI
  Le skill cadrage remplit chaque <...>. Feature refuse de coder tant qu'il en reste un.
  Les commentaires comme celui-ci disent POURQUOI la section existe.
  Vous pouvez les effacer une fois le fichier rempli.

  Ce fichier est lu à chaque conversation, par Claude Code et par OpenCode.
  Tout ce qui y est coûte du contexte à chaque fois.
  Écrivez ce que l'agent ne peut pas deviner en lisant le code.

  Les règles globales du harness (vouvoiement, preuves, interdits) s'appliquent déjà.
  Ne les recopiez pas ici. Si ce fichier dit autre chose, c'est lui qui gagne pour ce projet.
-->

# <Nom du projet> : règles pour l'agent

## Projet

<!-- POURQUOI : sans ça, l'agent devine le métier à partir des noms de fichiers. Deux ou trois phrases. -->

<Nom du projet> est <une appli / un outil> qui permet à <qui> de <faire quoi>.
Les utilisateurs sont <qui>. Le projet sert à <quel résultat concret>.

## Documents à lire avant de coder

<!-- POURQUOI : la spécification vit dans le dépôt, pas dans un chat. -->

- `docs/decisions.md` : le journal des décisions de cadrage. Une décision tranchée ne se rouvre pas sans raison écrite. Les décisions prises pendant un ticket sont dans son `feature.md`, rubrique "Décisions".
- `docs/<besoin>.md` : ce que fait le produit, les parcours.
- `docs/qa/` : les fiches de test, une par ticket.
- `docs/tickets/` : un dossier par ticket, avec `feature.md` (l'instruction) et `log.md` (le journal de l'agent).
- `docs/portes.md` : les trois portes humaines. L'agent n'en passe aucune seul.

## Technologies

<!-- POURQUOI : évite que l'agent ajoute une deuxième bibliothèque qui fait la même chose que la première. -->

| Rôle | Technologie |
| --- | --- |
| Interface | <framework et langage> |
| Serveur | <framework> |
| Base de données | <moteur> |
| Connexion des utilisateurs | <solution, ou "aucune"> |
| Hébergement | <Coolify sur votre serveur, Vercel, ou "pas encore choisi"> |
| Adresse en ligne | <adresse de l'appli, ou "pas encore en ligne"> |

Ajouter une bibliothèque : dire laquelle, pourquoi, son origine et sa version exacte. Attendre le "go".

## Rangement du dépôt

<!-- POURQUOI : l'agent sait où ranger un fichier sans créer de dossier parallèle. -->

```
<racine>/
├── <dossier du code>/   # <rôle>
├── docs/                # décisions, besoin, fiches QA
├── .github/             # modèles de ticket et de demande de fusion, CI
└── AGENTS.md            # ce fichier
```

## Conventions

<!-- POURQUOI : des règles simples et vérifiables. Préférez "toujours X" à "essayer de faire X". -->

- **Langue du code** : <anglais> (variables, fonctions, commentaires).
- **Langue de l'interface** : français.
- **Messages de commit** : en français, une phrase qui dit ce que le changement apporte, puis `(ticket #<numéro>)`. Jamais `Closes`, `Fixes` ni `Resolves` devant un numéro.
- **Un ticket = un changement = un commit.** Le code, le test, la fiche QA, le dossier `docs/tickets/<numéro>-<mots-courts>/` (`feature.md` et `log.md`) vont dans ce commit. Une branche de ticket ne touche pas à `docs/decisions.md` : deux tickets qui y ajoutent une ligne se bloquent à la fusion. Jamais deux changements dans un commit : un ticket qui en demande deux est découpé.
- **Avant le push**, chaque ajout se fait avec `git commit --amend`. Contrôle : `git rev-list --count preprod..HEAD` affiche 1.
- **Après le push**, une correction est un commit de plus sur la branche. La fusion par squash les réunit en un seul.
- **Jamais de push forcé**, sur aucune branche.
- Ajouter les fichiers un par un, jamais `git add -A`.

## Règles métier critiques

<!--
  POURQUOI : la section la plus importante. Ce sont les règles qui, cassées, coûtent de l'argent ou de la confiance.
  Numérotez-les : vous pourrez dire "ça viole la règle 2".
  Écrivez la règle ET la raison. Une règle sans raison se fait contourner.
-->

1. **<Règle>** : <ce qui doit toujours être vrai>. Raison : <pourquoi>.
2. **<Règle>** : <ce qui ne doit jamais arriver>. Raison : <pourquoi>.

## Sécurité

- Ne jamais écrire dans les journaux un mot de passe, un jeton ou une adresse e-mail en clair.
- Les secrets vivent dans les variables d'environnement, jamais dans le code ni dans ce fichier.
- Les noms des variables sont dans `.env.example`. Les valeurs ne s'écrivent nulle part dans le dépôt.

## Commandes de vérification

<!-- POURQUOI : l'agent ne dit pas "les tests passent". Il lance une commande et colle la sortie. -->

```bash
<commande d'installation>   # installer les bibliothèques
<commande de lancement>     # lancer en local
<commande de vérification>  # tout contrôler d'un coup (profil Next.js : npm run verifier)
```

Avant de dire "fini" : la commande de vérification passe au vert, et sa dernière ligne est citée.

## Outils MCP

<!-- POURQUOI : l'agent utilise la doc de la bonne version et prouve l'écran lui-même. Réglages dans `.mcp.json` (Claude Code) et `opencode.json` (OpenCode). -->

- **Context7** : avant d'utiliser l'API d'une bibliothèque, lire sa version dans `package.json`, puis sa doc dans Context7. Citer l'identifiant Context7 et la version dans `log.md`.
- **Playwright** : pour un ticket qui change un écran, lancer l'appli, faire le parcours avec Playwright et prendre une capture. Son nom commence toujours par `.playwright-mcp/` (exemple : `.playwright-mcp/12-accueil.png`), sinon elle tombe à la racine du dépôt. Citer ce chemin dans `log.md`. Ce que la capture prouve ne va plus dans les étapes Écran de la fiche QA.
- **Next.js DevTools** : pour une erreur dans un projet Next.js, lancer le serveur de dev, puis lire erreurs, routes et logs avec `nextjs_index` et `nextjs_call`. Citer l'erreur lue dans `log.md`. Si l'outil propose d'installer un programme (`agent-browser`), refuser et le signaler : le navigateur passe par Playwright.
- **Chrome DevTools**, **Agentation**, **Vercel** et **Sentry** sont coupés. Ils s'activent à la demande, pour déboguer, lire les annotations d'écran, suivre un déploiement Vercel ou lire les erreurs en ligne.
- **Vercel et Sentry en lecture seule.** Lire les déploiements, les logs et les erreurs. Jamais déployer, acheter, changer un réglage ou fermer un ticket par ces outils : la mise en ligne passe par livrer et la porte 3.
- Aucune clé dans ces fichiers. Seulement le nom de la variable.

## Pièges connus de ce dépôt

<!--
  POURQUOI : un piège payé une fois ne doit pas l'être deux fois.
  Ajoutez une ligne dès qu'un défaut arrive pour la deuxième fois.
-->

- Le code se déploie tout seul après la fusion sur main. Le schéma de la base non : il se change à part, et on vérifie son effet.
- <Piège suivant>.

## Tickets : GitHub Issues

<!-- POURQUOI : si l'état des tickets ment, on pilote à l'aveugle. -->

Les tickets vivent dans les Issues GitHub de ce dépôt. L'agent les lit avec `gh issue view <numéro>`.

- **Un ticket = une branche.** Une conversation neuve par ticket, ou un sous-agent neuf par ticket dans un lot. Nom de branche : `<numéro>-<mots-courts>`, par exemple `12-export-csv`.
- **Deux branches durables.** `main` = ce qui est en ligne, publié sur le domaine de production. `preprod` = le travail validé, pas encore en ligne, publié sur le domaine de préproduction. La branche par défaut du dépôt GitHub est toujours `main`, jamais `preprod`. Les documents de cadrage (`docs/cadrage/`) vivent sur `preprod`.
- **Chaque branche de ticket part de `preprod` et y revient** par une demande de fusion, après la porte 2. Le ticket y est résolu.
- **Mise en ligne.** Une demande de fusion de `preprod` vers main, fusion normale (pas squash), après le "go" de <prénom> : c'est la porte 3. Elle peut emporter plusieurs tickets.
- **Fermer le ticket.** Jamais tout seul. Aucun `Closes #` dans les demandes de fusion ni dans les commits. L'agent ferme le ticket à la main, avec un commentaire, après la fusion dans `preprod` acceptée par <prénom>.
- **Dependabot** vise `preprod`. Exception : ses correctifs de sécurité visent toujours main. L'agent redirige la demande vers `preprod` (`gh pr edit <n> --base preprod`).
- **La batterie de tests.** `npm run verifier` passe en local et dans la CI, sur chaque demande de fusion. On ne fusionne jamais si `gh pr checks` n'est pas tout vert.
- **Fusion par squash** d'un ticket dans `preprod`. Un ticket y arrive en un seul commit.
- **Livré en partie** : on ferme, et on ouvre un ticket neuf pour le reste. Jamais de "presque fini" qui traîne.
- **Abandonné** : on ferme avec "Close as not planned", avec la raison en commentaire. On garde la trace.
- **On ne remplit jamais après coup** une estimation ou une date. Un champ vide veut dire "pas mesuré".

## Comment l'agent travaille ici

- Lire le code concerné **avant** de proposer quoi que ce soit. Un ticket est souvent déjà fait en partie.
- Le "go" de <prénom> à la création d'un ticket vaut porte 1. Avant de coder, l'agent ne redemande que s'il lui reste une question produit, ou si le ticket est sensible (argent, droits d'accès, données personnelles, base de données, nouvelle bibliothèque). Ne jamais deviner un arbitrage.
- Plusieurs tickets se font d'affilée, un à la fois, puis une seule porte 2 pour tout le lot.
- Tout fait cité dans une demande de fusion renvoie à `fichier:ligne`, une commande ou un lien.
- La demande de fusion suit le modèle : fait, preuves, fiche QA. Ce qui n'est pas fait ou pas vérifié va dans le compte rendu de l'agent.
- L'agent ne fusionne ni sur main ni sur `preprod` sans un "go" explicite de <prénom> et une CI toute verte. Fusionner sur main déclenche le déploiement.
- Rien ne se commite directement sur main. Sur `preprod`, seuls les documents de cadrage.
