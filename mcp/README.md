# Outils MCP du harness

Un MCP est un serveur qui donne des outils en plus à un agent : lire une documentation, piloter un navigateur. Chaque outil déclaré prend un peu de place dans le contexte de l'agent, comme un outil rangé dans la camionnette.

Ce dossier contient la liste courte, réglée pour Claude Code et pour OpenCode. Aucun secret ici : une clé ne s'écrit jamais, seulement le nom de sa variable.

## La liste courte

Mesures faites avec `scripts/mesurer-mcp.mjs` (Context7 par une requête directe). Les jetons sont estimés à 4 octets par jeton. Vercel et Sentry demandent une connexion à votre compte : leur liste d'outils n'est pas mesurée.

| Outil | Version | Sert à | Outils | Taille de la liste | Mode |
| --- | --- | --- | --- | --- | --- |
| Context7 | serveur distant | Lire la doc d'une bibliothèque, à la bonne version | 2 | ~1 300 jetons | Toujours là |
| Playwright MCP | 0.0.85 | Parcourir l'appli comme un utilisateur, faire une capture | 25 | ~5 300 jetons | Toujours là |
| Next.js DevTools MCP | 0.4.0 | Lire les erreurs, les routes et les logs de l'appli Next.js qui tourne en dev | 4 | ~1 428 jetons | Toujours là, non prouvé |
| Chrome DevTools MCP | 1.13.0 | Déboguer : console, réseau, performances | 33 | ~8 100 jetons | À la demande |
| Agentation | 1.3.2 | Lire et résoudre les annotations posées sur l'écran | 9 | ~950 jetons | À la demande, non prouvé |
| Vercel MCP | serveur distant | Suivre les déploiements et les logs de build sur Vercel | non mesuré | non mesuré | En attente, coupé |
| Sentry MCP | serveur distant | Lire les erreurs de l'appli en ligne | non mesuré | non mesuré | En attente, coupé |

## Où en sont les preuves

| Outil | Claude Code | OpenCode |
| --- | --- | --- |
| Context7 | Prouvé : identifiant `/vercel/next.js/v16.4.5` et ligne Source citée | Prouvé : même identifiant, même ligne Source |
| Playwright | Prouvé : parcours et capture PNG 1280 x 720 | Prouvé : capture dans `.playwright-mcp/` |
| Next.js DevTools | Liste d'outils mesurée, jamais joué | Jamais joué |
| Chrome DevTools | Coût mesuré, jamais joué | Jamais joué |
| Agentation | **Non prouvé** | **Non prouvé** |
| Vercel, Sentry | Jamais connectés | Jamais connectés |

Choix retenu : pas d'autre preuve en bac à sable. Agentation, Next.js DevTools et le passage par le circuit complet (ticket, feature, livrer) se prouvent sur un vrai projet. Vercel et Sentry sont posés dès maintenant, coupés.

Mesure dans une vraie session de Claude Code (`claude -p`, avant Next.js DevTools) : 27 527 jetons au démarrage sans MCP, 28 201 avec Context7 et Playwright (+674), 28 790 en ajoutant Chrome DevTools (+589 pour 33 outils). Claude Code ne charge que les noms des outils au départ.

Pourquoi trois outils "toujours là" : Claude Code ne charge que les noms des outils MCP et va chercher le reste au besoin (recherche d'outils, active par défaut). OpenCode 2 fait de même avec son Code Mode. Le vrai coût vient de ce qu'un outil renvoie quand on s'en sert, surtout les pages lues par Playwright.

## Fiches d'audit

**Next.js DevTools MCP** (registre npm)
- Paquet `next-devtools-mcp` 0.4.0, licence MIT, dépôt github.com/vercel/next-devtools-mcp, publié par Vercel.
- Aucun script d'installation. Dépendances : `@modelcontextprotocol/sdk` 1.25.2, `zod` 3.25.76, `pid-port` 2.0.0, `find-process` 2.0.0, `undici` ^7.18.2 (seule version non fixée).
- Empreinte : `sha512-PTIoi+TihyztSTPkl+YIesL81wU3pRDo6QCg1wgjvLGfBlXv3yamvQyoI8j/I2t7gqDStXoa7jtn/YUdvcBQuw==`.
- Il cherche les serveurs Next.js 16 en marche et passe par leur point d'accès intégré `/_next/mcp`. Sans serveur de dev lancé, il ne voit rien.
- Télémétrie : coupée par `NEXT_TELEMETRY_DISABLED=1`, posé dans les deux fichiers. Données locales dans `~/.next-devtools-mcp/`.
- ⚠️ Son outil `browser_eval` propose d'installer `agent-browser` en global (`npm install -g`). Interdit dans le harness : le navigateur passe par Playwright.
- Le dépôt ne cite pas OpenCode parmi les agents testés. Hypothèse : ça marche quand même, c'est un serveur MCP standard.

**Vercel MCP** (vercel.com/docs, page mise à jour le 15 septembre 2026)
- Serveur officiel distant `https://mcp.vercel.com`, connexion OAuth, aucune clé.
- Claude Code et OpenCode sont dans la liste des agents acceptés par Vercel.
- ⚠️ Il donne à l'agent les mêmes droits que votre compte Vercel, et il sait déployer. Pas de mode lecture seule documenté. La consigne du harness le limite à la lecture.

**Sentry MCP** (mcp.sentry.dev)
- Serveur officiel distant `https://mcp.sentry.dev/mcp`, connexion OAuth, aucune clé. Licence FSL-1.1-Apache-2.0, lue à la source (`LICENSE.md` du dépôt github.com/getsentry/sentry-mcp).
- À l'activation, ajouter l'organisation et le projet à l'adresse : `https://mcp.sentry.dev/mcp/ORGANISATION/PROJET`. Sentry le recommande.
- OpenCode n'est pas cité, mais tout agent qui parle MCP en HTTP est accepté. Hypothèse, non testé.

## Hors liste

| Outil | Pourquoi | Quand le revoir |
| --- | --- | --- |
| Figma MCP | Siège gratuit ou View : 20 appels par mois | Siège Dev ou Full payant |
| Supabase MCP | Aucun projet ne l'utilise | Un projet sur Supabase, en lecture seule et limité à ce projet |
| GitHub MCP | La commande `gh` suffit et coûte moins | Jamais pour l'instant |
| Plugins d'agent (ex. plugin Sentry pour Claude Code) | Lus par un seul agent : contraire au harness agnostique | Jamais pour l'instant |

## Les fichiers

| Fichier | Agent | Rôle |
| --- | --- | --- |
| `claude/projet.mcp.json` | Claude Code | Copié en `.mcp.json` dans chaque projet neuf. Context7, Playwright, Next.js DevTools |
| `claude/devtools.json` | Claude Code | Chrome DevTools, à la demande |
| `claude/agentation.json` | Claude Code | Agentation, à la demande |
| `claude/vercel.json` | Claude Code | Vercel, à la demande |
| `claude/sentry.json` | Claude Code | Sentry, à la demande |
| `opencode/opencode.json` | OpenCode | Copié en `opencode.json` dans chaque projet neuf. Les sept outils, quatre coupés |

Il faut deux formats : Claude Code lit `.mcp.json` (clé `mcpServers`, variables `${NOM}`), OpenCode lit `opencode.json` (clé `mcp`, variables `{env:NOM}`). Le fichier OpenCode est écrit au format V1, que la V2 accepte aussi.

## Activer un outil à la demande

Claude Code, depuis le dossier du projet. Remplacez `<harness>` par le dossier du dépôt harness :

```bash
claude --mcp-config <harness>/mcp/claude/devtools.json
claude --mcp-config <harness>/mcp/claude/agentation.json
claude --mcp-config <harness>/mcp/claude/vercel.json
claude --mcp-config <harness>/mcp/claude/sentry.json
```

Vercel et Sentry : à la première utilisation, taper `/mcp` dans Claude Code et se connecter.

OpenCode : dans `opencode.json` du projet, passer `"enabled"` de l'outil à `true`, puis rouvrir le projet.

## Règles

- **Captures Playwright.** Un nom de fichier donné à la capture part du dossier où l'agent travaille, pas de `--output-dir`. Le nom commence donc toujours par `.playwright-mcp/`. Constaté avec la version 0.0.85.
- **Versions épinglées.** Jamais `@latest`, même si la doc de l'éditeur le montre. Une nouvelle version passe par l'audit : origine, licence, scripts d'installation, empreinte, puis mesure avec `scripts/mesurer-mcp.mjs`.
- **Télémétrie coupée.** Chrome DevTools MCP : `--no-usage-statistics` et `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=1`. Next.js DevTools : `NEXT_TELEMETRY_DISABLED=1`.
- **Navigateur isolé.** `--isolated` : le profil reste en mémoire, rien ne s'écrit dans votre Chrome.
- **Pas d'installation par un outil MCP.** Si un outil propose d'installer un programme (ex. `agent-browser`), l'agent refuse et le signale.
- **Vercel et Sentry en lecture seule.** L'agent lit les déploiements, les logs et les erreurs. Il ne déploie pas, n'achète rien, ne change aucun réglage et ne ferme aucun ticket par ces outils. La mise en ligne passe par le skill livrer et la porte 3.
- **Une clé ne s'écrit jamais.** Context7 marche sans clé, avec une limite basse. Pour en ajouter une, dans `.mcp.json` : `"headers": { "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}" }`, et la valeur reste dans votre environnement. Vercel et Sentry passent par OAuth : aucune clé du tout.
- **Licences.** Agentation : PolyForm Shield 1.0.0, usage perso permis, ce n'est pas de l'open source. Sentry MCP : FSL-1.1-Apache-2.0, même idée. L'usage est permis, sauf pour en faire un produit concurrent, et le code passe sous licence Apache 2.0 au bout de deux ans.

## Mesurer un serveur

```bash
node scripts/mesurer-mcp.mjs playwright -- npx -y @playwright/mcp@0.0.85 --headless --isolated
```

La ligne `OK` donne le nombre d'outils, la taille et une estimation en jetons.
