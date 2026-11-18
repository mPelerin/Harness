# Harness

Une boîte à outils pour travailler avec des agents IA de code : des règles, des skills et une méthode, de l'idée à la mise en ligne. Elle est écrite une seule fois, et Claude Code comme OpenCode la lisent.

## À quoi ça sert

Sans harness, chaque agent repart de zéro et il faut tout lui réexpliquer. Avec le harness, les règles de base sont déjà là au démarrage, les mêmes pour tous les agents.

## Deux dépôts : le moteur et votre instance

Ce dépôt est le **moteur**. Il ne contient rien de personnel.

Votre **instance** vit dans un dépôt à vous, privé. Elle contient un dossier `config/` :

| Fichier | Contenu |
| --- | --- |
| `harness.conf` | Prénom, compte GitHub, domaines, serveur, commande de l'orchestrateur. Format `CLE=valeur`, aucun secret. Modèle : `harness.conf.exemple` |
| `profil.md` | Votre façon de travailler et de recevoir les réponses. Ajouté aux règles du moteur |
| `interdits.txt` | Les mots qui ne doivent jamais entrer dans le moteur (liste noire du hook) |

Vos skills perso vont dans un dossier `skills/` à côté de `config/`.

Le moteur ne connaît jamais l'instance. L'installeur assemble les deux sur votre PC.

## Où est quoi

```
harness/
  AGENTS.md              les règles communes, lues par les agents
  harness.conf.exemple   le modèle de configuration de l'instance
  docs/                  modèles, format des skills, glossaire
  scripts/
    installer.sh           branche les agents sur le moteur et l'instance
    verifier-install.sh    contrôle que tout est bien branché
    nouveau-projet.sh      crée un projet depuis le gabarit (commande nouveau-projet)
    orchestrateur.sh       dépose une demande chez l'orchestrateur et suit la carte
    pre-vol.sh             liste les blocages humains avant de coder ou de lancer la nuit
    mesurer-mcp.mjs        mesure la place que prend un outil MCP
  skills/                les skills de méthode, plus le skill témoin test-harness
  template-projet/       le socle commun à tous les projets
  profils/nextjs/        le profil TypeScript et Next.js : hooks, CI, Dependabot
  mcp/                   les outils MCP, réglés pour Claude Code et OpenCode
```

## Installer

Depuis le dossier de ce dépôt :

```bash
bash scripts/installer.sh --essai --config <votre-instance>/config
bash scripts/installer.sh --config <votre-instance>/config
bash scripts/verifier-install.sh
```

Le premier montre ce qui serait fait, sans rien changer. Le deuxième le fait. Le troisième contrôle et finit par **OK** ou **STOP**.

Ce que fait l'installeur :

- il relie `~/.config/harness` au dossier `config/` de votre instance ;
- il génère les règles des agents : `AGENTS.md` du moteur, puis votre `profil.md` ;
- il relie les skills du moteur, puis ceux de l'instance, dans `~/.claude/skills/` ;
- il relie la commande `nouveau-projet`.

Il ne supprime jamais rien. Ce qui gêne est mis de côté dans un dossier daté (`DOSSIER_SAUVEGARDES` de `harness.conf`, sinon `~/.local/state/harness/sauvegardes/`).

Sans instance, il installe le moteur seul.

Les règles sont **générées** : après un changement de `AGENTS.md` ou de `profil.md`, relancez l'installeur. Le vérificateur signale des règles qui ne sont plus à jour.

## La méthode, de l'idée à la mise en ligne

Chaque ligne est un skill. Vous dites le mot, l'agent déroule, et il s'arrête aux portes.

| Vous dites | Ce que fait l'agent | Où il s'arrête |
| --- | --- | --- |
| cadrage | Pose les questions, écrit le PRD, les écrans, les stories, remplit AGENTS.md | Porte 1 : votre "go" après relecture |
| tickets | Découpe les stories en tickets GitHub | Votre "go" sur le découpage |
| feature tout | Code chaque ticket avec ses tests, vérifie, relit, prépare la fiche QA, ouvre la demande de fusion | Porte 2 : un seul tableau pour tout le lot |
| go tout | Fusionne dans `preprod`, ferme les tickets à la main | Nulle part |
| mets en ligne | Prépare la fusion de `preprod` vers main | Porte 3 : votre "go mise en ligne" |
| retro | Transforme une erreur en contrôle ou en règle | Votre "go" avant de toucher au harness |
| fini, reprends | Écrit la passation, ou repart de la dernière | Nulle part |

Les portes sont détaillées dans `template-projet/docs/portes.md`.

**Déléguer à un orchestrateur.** Si `ORCHESTRATEUR` est rempli dans `harness.conf`, `feature` ne code pas ici. Il ouvre une sous-conversation par ticket. Elle dépose la carte chez l'orchestrateur et la suit, sans bruit. La conversation principale ne garde qu'un tableau. `feature local` force le codage sur ce PC. Le pré-vol (`pre-vol --strict`) vérifie avant tout dépôt que les variables, comptes et migrations sont prêts, et qu'aucun ticket ne laisse ses prérequis dans le flou.

## Créer un projet

```bash
nouveau-projet mon-appli
```

La commande crée l'appli Next.js, pose le gabarit, les hooks et les outils MCP, puis lance la vérification complète. Ensuite, dites "cadrage" à l'agent.

## Les deux mots de contrôle

Ils prouvent qu'un agent lit bien le harness. Demandez-les dans une session neuve.

| Question à l'agent | Réponse attendue | Ce que ça prouve |
| --- | --- | --- |
| Quel est le mot de contrôle du harness ? | copeau-42 | Les règles sont lues |
| Quel est le mot de contrôle du skill test ? | rabot-17 | Les skills sont lus |

## Ajouter un skill

1. Lisez `docs/skills.md`, il décrit le format.
2. Un skill pour tout le monde va dans `skills/` de ce dépôt. Un skill personnel va dans `skills/` de votre instance. Un même nom dans les deux est refusé.
3. Relancez l'installeur, puis le vérificateur.
4. Fermez puis rouvrez les agents.

## Où va un changement

| Le changement… | Va dans |
| --- | --- |
| améliore la méthode pour tout le monde | ce dépôt |
| contient un nom, une adresse, un serveur, votre profil | votre instance |
| les deux | ce dépôt avec une variable, la valeur dans `harness.conf` |

## Revenir en arrière

L'installeur ne fait que des liens et un fichier généré.

- Enlever un lien : `unlink ~/.claude/skills/<nom>`. Le fichier visé n'est pas touché.
- Retrouver ce qui a été mis de côté : le dossier de sauvegarde daté, avec l'arborescence d'origine.
- Retirer les règles générées : `unlink ~/.claude/CLAUDE.md` et `unlink ~/.config/opencode/AGENTS.md`, puis remettre l'ancien fichier depuis la sauvegarde.

## Garde-fous avant chaque commit et chaque push

Ce dépôt est public. Deux contrôles bloquent ce qui ne doit pas y entrer :

- **la liste noire** de votre instance (`~/.config/harness/interdits.txt`) : vos domaines, votre serveur, vos noms. Elle n'est jamais copiée ici. Le contrôle regarde les fichiers, les messages de commit, les noms de branche et d'étiquette ;
- **gitleaks**, avec `.gitleaks.toml` : les secrets, les adresses IP privées, les adresses Tailscale et les e-mails. Il tourne aussi dans la CI, sur tout l'historique.

Prérequis : `gitleaks` et `lefthook` installés, versions épinglées. Brancher une fois après le clone :

```bash
lefthook install
```

Avant un tout premier commit, scanner tout le dossier : `bash scripts/liste-noire.sh --tout . && gitleaks dir --redact --no-banner .`

## Règles de travail du dépôt

- Un changement à la fois.
- Aucun secret dans le dépôt (pas de .env, pas de clé).
- Aucune installation tierce sans avoir lu son contenu et vérifié son origine.
- On ajoute les fichiers un par un : `git add -A` peut emporter un fichier qui n'a rien à faire dans le dépôt.
