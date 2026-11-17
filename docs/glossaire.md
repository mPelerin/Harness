# Glossaire

Les mots techniques du harness, expliqués simplement. Classés par ordre alphabétique.

Chaque entrée a une définition courte et un exemple concret.

## Agent

Un assistant IA qui peut agir, pas seulement répondre. Il lit des fichiers, lance des commandes, modifie du code.

**Exemple.** Claude Code et OpenCode sont des agents. Un simple chat qui répond à une question n'en est pas un.

## AGENTS.md

Le fichier de règles que lisent les agents au démarrage. C'est un format ouvert, compris par plusieurs outils.

**Exemple.** C'est le plan de chantier posé sur l'établi. Tous les ouvriers le lisent avant de commencer.

## Branche

Une ligne de travail dans Git. La branche principale s'appelle **main** : c'est toujours la branche par défaut du dépôt GitHub, et celle qui publie en production.

**Exemple.** Main, c'est le plan officiel. Une branche, c'est une copie du plan sur laquelle on teste une idée sans risquer l'original.

## CI

Une machine de GitHub qui relance les contrôles du projet à chaque demande de fusion. Elle part de zéro, donc elle voit ce qui ne marche que sur votre PC. CI veut dire "intégration continue".

**Exemple.** Le contrôleur qui repasse derrière l'artisan avec sa propre règle et son propre niveau.

## CLAUDE.md

Le fichier de règles propre à Claude Code. Dans le harness, il ne contient qu'une ligne qui renvoie vers AGENTS.md, pour ne pas écrire les règles deux fois.

## Claude Code

L'agent principal du harness. Il travaille dans votre terminal ou votre application, avec accès à vos fichiers.

## Commit

Un enregistrement daté dans Git, avec une phrase qui dit ce qui a changé.

**Exemple.** C'est une photo du chantier avec une légende. On peut toujours revenir à cette photo.

## Conteneur

Une boîte fermée dans laquelle tourne un programme, séparée du reste de la machine.

**Exemple.** Un caisson de cuisine monté en atelier : il a ses propres vis et ses propres pièces, il ne mélange rien avec le caisson d'à côté. Docker fabrique ces boîtes.

## Coolify

Le programme du serveur qui gère les conteneurs et les mises en ligne d'applications. Le harness a le droit d'y ajouter une nouvelle appli, mais jamais de toucher à ce qui tourne déjà.

## Demande de fusion

La demande d'ajouter le travail d'une branche dans une autre. GitHub l'appelle "pull request", ou PR. On y lit le changement, les preuves et le résultat de la CI avant de dire "go".

**Exemple.** Le bon de réception d'un meuble : on vérifie avant de signer.

## Dependabot

Un robot de GitHub qui propose les mises à jour des bibliothèques, par demande de fusion. Les failles de sécurité arrivent tout de suite, le reste une fois par semaine.

## Dépôt

Un dossier suivi par Git, qui garde l'historique de tous ses changements. Le dépôt du harness s'appelle **harness** et vit aussi sur GitHub.

## Docker

L'outil qui crée et fait tourner les conteneurs.

## Essai à blanc

Lancer une commande en mode "pour voir", sans rien modifier. L'installateur le propose avec `--essai`.

**Exemple.** Monter le meuble à sec avant de coller.

## Fiche QA

La liste des tests à faire à la main sur un ticket, préparée par l'agent. QA veut dire "contrôle qualité". L'agent prouve ce qu'une commande peut prouver, vous testez ce qui demande des yeux.

**Exemple.** La fiche de contrôle avant livraison : les portes ferment, les tiroirs coulissent.

## Frontmatter (l'en-tête)

Les premières lignes d'un fichier, entre deux lignes `---`, qui donnent ses informations d'identité.

**Exemple.** Dans un skill : le nom et la description. C'est l'étiquette sur la boîte, que l'agent lit sans ouvrir la boîte.

## Gabarit

Le modèle de départ d'un nouveau projet : règles, contrôles, hooks, CI. La commande `nouveau-projet` le copie.

**Exemple.** Le gabarit de perçage : on ne retrace pas les trous à chaque caisson.

## Git

Le logiciel qui garde l'historique d'un dossier. Il permet de revenir en arrière et de synchroniser plusieurs machines.

## GitHub

Le site où Git envoie une copie du dépôt. Votre dépôt y est **privé** : vous seul le voyez.

## GitHub Issues

La liste de tâches intégrée à GitHub. C'est le seul outil de suivi choisi pour le harness.

## Harness

Le mot anglais pour "harnais". Ici, l'ensemble des règles, skills et méthodes qui encadrent le travail des agents. Il les guide sans les remplacer.

## Hook

Un contrôle que Git lance tout seul avant un commit ou un push. S'il échoue, le commit ou le push est refusé. Dans les projets du harness, l'outil Lefthook les gère.

**Exemple.** La butée sur la scie : elle arrête la mauvaise coupe avant qu'elle arrive.

## Installateur

Le script `installer.sh`. Il crée les liens entre les agents et le dépôt.

## Lien symbolique

Un raccourci vers un fichier ou un dossier. Ouvrir le raccourci, c'est ouvrir l'original.

**Exemple.** Une étiquette sur l'étagère qui dit "l'équerre est dans le tiroir du bas". On ne la déplace pas, on la retrouve. Modifier l'original change ce que voit tout le monde.

## Lot

Plusieurs tickets réalisés d'affilée par l'agent, avec une seule porte 2 à la fin. On le lance avec "feature tout" ou "feature 2 3 4".

## MCP

Un serveur qui donne des outils en plus à un agent : lire une documentation, piloter un navigateur. MCP veut dire "Model Context Protocol".

**Exemple.** Une machine en plus dans la camionnette. Utile, mais chacune prend de la place.

## Mot de contrôle

Un mot secret placé dans une règle ou un skill, pour prouver qu'un agent l'a bien lu. Dans le harness : **copeau-42** pour les règles, **rabot-17** pour le skill test.

## Obsidian

Le logiciel de notes dans lequel le dossier `docs/` s'ouvre comme un coffre de notes.

## OpenCode

Le deuxième agent du harness. Il donne un deuxième avis, avec les modèles Synthetic.

## Parking à idées

Une liste où l'on range une nouvelle idée sans l'exécuter. On garde la priorité en cours, et c'est vous qui décidez de changer ou non.

## Passation

La note de fin de session écrite par le skill cloture-session. Elle dit l'état réel et la prochaine action, pour qu'une session neuve reparte tout de suite.

**Exemple.** Le mot laissé au collègue qui reprend le chantier le lendemain.

## Phase

Une grande étape du projet. Il y en a de 0 à 7, une seule à la fois, et on ne passe à la suivante qu'avec votre accord écrit.

## Porte humaine

Un point d'arrêt où l'agent doit s'arrêter et attendre votre décision avant d'aller plus loin.

**Exemple.** Le feu rouge avant de coller : l'agent ne le brûle pas.

## Preprod

La branche où arrive le travail validé, avant la mise en ligne. Elle découle de `main`, ne le remplace jamais, et publie sur le domaine de préproduction, derrière un login. Les tickets en partent et y reviennent. La branche main ne reçoit que les mises en ligne.

**Exemple.** L'atelier où le meuble est monté à blanc, avant la pose chez le client.

## Pull

Récupérer sur ce PC les changements qui sont sur GitHub. Commande : `git pull`.

## Push

Envoyer sur GitHub les enregistrements faits sur ce PC. Commande : `git push`.

## Règle

Une consigne écrite dans AGENTS.md, valable tout le temps et pour tous les agents.

**À ne pas confondre avec un skill** : une règle s'applique toujours, un skill s'utilise sur demande.

## Skill

Un mode d'emploi pour une tâche précise. L'agent ne le lit en entier que quand la tâche correspond.

**Exemple.** Une fiche de pose pour une plinthe. On la sort quand on pose une plinthe, pas le reste du temps.

## SKILL.md

Le fichier d'un skill. Son nom s'écrit en **majuscules**, sinon l'agent ne le trouve pas.

## Squash

Une fusion qui réunit tous les commits d'une branche en un seul. Un ticket arrive ainsi dans preprod en un seul commit, facile à relire et à annuler.

## SSH

La façon sécurisée dont votre PC prouve son identité à GitHub, avec une clé, sans mot de passe à retaper.

**Exemple.** Un badge d'accès à la place d'un code qu'on oublie.

## Synthetic

Le service qui fournit les modèles utilisés par OpenCode.

## TDD

Écrire le test avant le code. On voit le test échouer, on écrit le code, on le voit passer. TDD veut dire "développement piloté par les tests".

**Exemple.** Poser le gabarit de contrôle avant d'usiner la pièce.

## Ticket

Une demande de travail écrite dans GitHub Issues : une fonction à ajouter ou un bug à corriger. Dans le harness, un ticket = un changement = un commit.

## Vérificateur

Le script `verifier-install.sh`. Il contrôle que tout est bien branché et ne modifie rien.

## Worktree

Une deuxième copie de travail du même dépôt, dans un autre dossier, pour avancer sur deux sujets en parallèle sans les mélanger. Prévu pour une phase suivante.
