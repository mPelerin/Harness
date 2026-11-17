<!-- Adapté de kit-agents-ia, Mathis Gorvien, licence MIT (voir LICENCES-TIERS.md). -->

## <Titre court du ticket>

<!-- Jamais Closes, Fixes ou Resolves devant un numéro : un ticket ne se ferme pas tout seul. -->

Ticket : #<numéro du ticket>

**Base :** preprod. Fusion par squash.
**Dossier du ticket :** `docs/tickets/<numéro>-<mots-courts>/`

### Fait

- <Ce qui change pour l'utilisateur, en une ligne>

### Preuves

- `<commande de vérification>` → `<dernière ligne>`, commit `<code>`
- `git rev-list --count preprod..HEAD` → `1`

### Base de données

Aucun changement / <fichier>, à appliquer **avant** la fusion.

### Fiche QA

`docs/qa/<numéro>-<mots-courts>.md` (à tester à l'écran : <oui / non>)
