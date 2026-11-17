# Gabarit de projet

Le socle commun à tous les projets du harness. Vous n'avez rien à copier à la main : la commande `nouveau-projet` le pose dans chaque projet neuf, puis ajoute le profil (`profils/nextjs/`) et les outils MCP (`mcp/`).

```bash
nouveau-projet mon-appli
```

Ce README est remplacé par celui du projet au moment de la création.

## Ce qu'il contient

| Fichier | À quoi il sert |
| --- | --- |
| `AGENTS.md` | Les règles du projet pour l'agent. Le skill cadrage le remplit. |
| `CLAUDE.md` | Une seule ligne, `@AGENTS.md`, pour que Claude Code lise les mêmes règles qu'OpenCode. |
| `.github/pull_request_template.md` | Le modèle de demande de fusion : fait, preuves, fiche QA, et le numéro du ticket (sans `Closes #`). |
| `.github/ISSUE_TEMPLATE/fonction.md` | Le modèle de ticket pour une nouvelle fonction. |
| `.github/ISSUE_TEMPLATE/bug.md` | Le modèle de ticket pour un bug. |
| `docs/decisions.md` | Le journal des décisions du projet. |
| `docs/qa/modele-fiche-qa.md` | Le modèle de fiche QA, une par ticket. |
| `docs/portes.md` | La checklist des trois portes humaines : décider, tester, fusionner. |
| `.gitignore` | Empêche les fichiers de secrets `.env` d'entrer dans le dépôt. |
| `LICENCES-TIERS.md` | La licence des textes repris de kit-agents-ia. À garder. |

## Ce que le profil Next.js ajoute

- Lint, format, tests, hooks Git, et la commande `npm run verifier` qui lance tout.
- La CI GitHub et Dependabot.
- Le déploiement Coolify, désactivé par défaut et jamais joué en vrai.

## Bon à savoir

GitHub ne lit les modèles du dossier `.github/` que s'ils sont à la racine du dépôt, sur la branche principale.
Dans le dépôt harness, ils dorment donc. Ils s'activent une fois copiés dans un vrai projet.
