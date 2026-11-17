# Comment écrire un skill du harness

Le modèle à copier est `skills/test-harness/SKILL.md`.
Ces règles ont été vérifiées le 12 nov. 2026 pour Claude Code et OpenCode.

## Emplacement

- Un dossier par skill, dans `skills/`, au premier niveau.
- Dans ce dossier, un fichier nommé exactement `SKILL.md`, en majuscules.
- installer.sh pose un lien par skill dans `~/.claude/skills/`. Les deux agents lisent ce dossier.

## En-tête (entre les deux lignes "---")

| Champ | Règle |
| --- | --- |
| name | Identique au nom du dossier. Minuscules, chiffres et tirets seulement. Pas d'accent. 64 caractères au plus. |
| description | Dit ce que fait le skill ET quand l'utiliser. 1024 caractères au plus. C'est elle qui déclenche le skill. |

Pas d'autre champ dans l'en-tête, sauf besoin prouvé. Un champ propre à un seul agent casse l'agnostique.

## Corps du skill, toujours dans cet ordre

1. **But** : une ou deux phrases.
2. **Quand l'utiliser** : les demandes qui le déclenchent.
3. **Quand ne pas l'utiliser** : les cas voisins qui prêtent à confusion.
4. **Étapes** : numérotées, une action par étape.
5. **Point d'arrêt** : où l'agent s'arrête et attend l'utilisateur.
6. **Preuve attendue** : ce que la réponse doit contenir pour être valable.
7. **Interdits** : ce que le skill ne fait jamais.

## Style

- En français. Phrases courtes.
- Moins de 200 lignes par SKILL.md. Le détail va dans un sous-dossier `references/`.
- Un seul skill par étape de la méthode. 10 skills au plus au départ.

## Sources

- OpenCode, skills : https://opencode.ai/docs/skills
- Spécification Agent Skills : https://agentskills.io/specification
- Claude Code, skills : https://code.claude.com/docs/en/skills
