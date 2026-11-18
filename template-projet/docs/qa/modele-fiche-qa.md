<!-- Adapté de kit-agents-ia, Mathis Gorvien, licence MIT (voir LICENCES-TIERS.md). -->

# Modèle de fiche QA

Une fiche par ticket. Copiez ce fichier sous le nom `<numéro>-<mots-courts>.md`, dans ce même dossier.
L'agent la prépare. L'humain la déroule et remplit la colonne Commentaire.

**Qui teste quoi.**

- **Machine** : l'agent le prouve lui-même, avant de vous donner la fiche. La preuve est déjà dans la colonne Résultat.
- **Écran** : un humain le fait, sur ordinateur et sur téléphone.
- **En ligne** : sur la version déployée par Coolify, avec les comptes de test.

**Résultat.** ✅ conforme, ❌ écart (écrire attendu et obtenu), ⚠️ partiel, vide si pas encore testé.

---

## #<numéro> : <titre court>

**À tester à l'écran :** <oui / "Rien à tester à l'écran. Les preuves Machine suffisent.">
**⛔ À faire avant de tester :** <migration à appliquer, variable à poser, compte à créer, avec la commande ou l'endroit exact. "Aucun" sinon. Jamais une valeur de secret.>
**Version testée :** demande de fusion #<numéro>, commit <code de 7 caractères>

**Pour tester :**

```bash
git fetch origin && git switch <branche> && <commande d'installation> && <commande de lancement>
```

Puis ouvrir <adresse locale et page>. Pour revenir : `git switch preprod`.

**Comptes de test :** <rôle A> : <compte A>, <rôle B> : <compte B>
**État de départ :** <données à préparer avant de commencer>

| # | Étape | Attendu | Qui | Résultat | Commentaire |
| --- | --- | --- | --- | --- | --- |
| 1 | <Action précise : où cliquer, quoi saisir> | <Ce qui doit se passer> | Écran | | |
| 2 | <Action> | <Attendu> | Machine | ✅ <preuve courte de l'agent> | |
| 3 | <Le même parcours avec le mauvais compte> | <Accès refusé, rien ne fuit> | En ligne | | |
| 4 | <Saisie fausse ou double clic> | <Message clair, pas de doublon> | Écran | | |
| 5 | <Écran de téléphone, 390 pixels de large> | <Rien de coupé, rien qui déborde> | Écran | | |

**Remise à zéro :** <comment revenir à l'état de départ pour rejouer la fiche>

---

## Écrire une bonne étape

- **Précise.** "Cliquer sur Exporter en haut à droite", pas "tester l'export".
- **Qui peut échouer.** Cette étape serait-elle rouge sur une version buguée ? Sinon, elle ne teste rien.
- **Avec le mauvais compte.** Au moins une étape par ticket vérifie qu'un compte sans droit ne voit rien.
- **Colonne Commentaire vide.** C'est la place de l'humain. L'agent ne la remplit pas.
- **Rien pour l'humain qu'une commande peut prouver.** L'agent lance la commande et met la preuve.
- **Prérequis en tête.** Une migration, une variable, un compte : en haut de la fiche. Tant que ce n'est pas réglé, la fiche n'est pas prête.
