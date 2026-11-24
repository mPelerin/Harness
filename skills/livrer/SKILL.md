---
name: livrer
description: Livre le travail sans passer une porte à la place de l'utilisateur. Mode ticket, pousse la branche du worktree, ouvre la demande de fusion vers preprod, attend la CI verte, puis après le go fusionne en squash, ferme le ticket à la main et met sa note à jour. Mode mise en ligne, fusionne preprod dans main après le go de la porte 3, puis tient les notes Déploiement, Vérification et Bilan. À utiliser quand l'utilisateur dit "livre", "go", "go tout", "go 2 4", "fusionne", "mets en ligne" ou "déploie". Ne pas utiliser pour coder (feature), créer un ticket (tickets), ni lancer les contrôles (verifier).
---

# Livrer : de la branche prête à la fusion

## But

Faire arriver un travail vérifié là où il doit aller, sans jamais passer une porte à la
place de l'utilisateur, et tenir la mémoire à jour.
Quatre règles : jamais de push forcé ; un ticket ne se ferme jamais tout seul ; pas de
fusion sans "go" écrit et CI verte ; on fusionne le commit testé (`--match-head-commit`).

## Quand l'utiliser

- Feature arrive à l'étape 9 (mode ticket, étapes 1 à 5).
- L'utilisateur dit "go", "go tout", "go 2 4" après la porte 2, ou "mets en ligne".

## Quand ne pas l'utiliser

- Coder : feature. Lancer seulement les contrôles : verifier.

## Le projet

Règles R1 à R5 du skill projet. Un ticket se livre depuis son worktree `ARBRE`. Après
une fusion, les notes se mettent à jour par un **commit mémoire** dans `BASE` (R3).

## Le contrôle des mots interdits

Il ne doit rien afficher :

```bash
grep -inE '(close[sd]?|fix(e[sd])?|resolve[sd]?)[[:space:]:]+[^[:space:]]*(#|/issues/)[0-9]' "$FICHIER"
```

## Étapes, mode ticket

### Revue Hermès obligatoire

Avec `RELECTEUR_HERMES` renseigné, appliquer ce contrôle pour toute livraison d'un ticket
confié à Hermès (`agent: hermes` ou `hermes-nuit` dans la note de suivi). La carte de
livraison donne `TABLEAU` et `CARTE_CODE`. Les conserver dans le corps de la demande de
fusion et le rapport de porte 2. Une reprise relit ces références et interroge le serveur Hermès.

Sur le serveur Hermès, lire les trois valeurs du `harness.conf` d'instance. Avant le push,
utiliser le SHA entier de HEAD. Avant la porte 2 et avant chaque fusion, relire le SHA de
la demande de fusion avec `gh pr view <pr> --json headRefOid --jq .headRefOid`.
Pour chacun de ces contrôles, utiliser le SHA frais dans `OID`.

```bash
verifier-revue-hermes --board "$TABLEAU" --reviewer "$RELECTEUR_HERMES" \
  --provider "$FOURNISSEUR_REVUE_HERMES" --code-provider "$FOURNISSEUR_CODE_HERMES" \
  "$CARTE_CODE" "$OID"
```

Un code de sortie autre que zéro bloque la livraison. Un rebase, une fusion de mise à
jour ou une correction de CI produisent un nouveau SHA. Faire reprendre le même worktree
par une carte de code `feature` qui cite la demande de fusion si elle existe. Rejouer la
revue avant le nouvel envoi. Utiliser la sortie du dernier contrôle comme preuve.
Si la vérification ne peut être faite depuis le PC, transmettre la livraison au serveur Hermès.

1. **Situer.** Dans `ARBRE` : branche `<n>-<mots-courts>`, `git status --short` vide,
   `gh issue view <n> --json state` donne `OPEN`. Une demande de fusion déjà ouverte :
   étape 5 si son HEAD correspond au candidat, étapes 2 et 3 sinon. Une fois par dépôt, en lecture :
   `gh repo view --json squashMergeAllowed,deleteBranchOnMerge` donne `true` et `false`.
   Sinon arrêt : c'est un réglage de l'utilisateur.

2. **Contrôler avant l'envoi.** `git fetch origin`. `preprod` a avancé et la branche n'est
   pas poussée : `git rebase origin/preprod`. Déjà poussée : `git merge origin/preprod`.
   Pas encore poussée : `git rev-list --count origin/preprod..HEAD` affiche 1.
   Mots interdits sur les messages de commit. Aucun `.env` dans le diff. Puis verifier.
   Pour la préparation de `feature`, s'arrêter ici et demander la revue. En livraison
   Hermès, une actualisation qui changerait le SHA repart chez le codeur avant tout envoi.

3. **Pousser.** Si la revue est exigée, contrôler HEAD et pousser le SHA approuvé avec
   `git push origin "$OID:refs/heads/$BRANCHE"`, puis relier la branche locale à son suivi
   distant. Dans les autres cas, `git push -u origin <branche>`. Refusé : corriger la cause,
   jamais forcer.
   Preuve : `git ls-remote origin refs/heads/<branche>` égale `git rev-parse HEAD`.

4. **Ouvrir ou mettre à jour la demande de fusion.** Corps rempli depuis `.github/PULL_REQUEST_TEMPLATE.md`
   dans un fichier : `Ticket : #<n>`, ce qui est fait, preuves, fiche QA (chemin de la
   note), base de données. Mots interdits.
   `gh pr create --base preprod --head <branche> --title "<titre> (ticket #<n>)" --body-file "$F"`.
   Si une demande existe, garder son numéro et actualiser les preuves avec `gh pr edit`.
   Lire le numéro rendu. Preuve : `gh pr view <pr> --json baseRefName` donne `preprod`.

5. **Attendre la CI.** `gh pr checks <pr> --watch --fail-fast`, code de sortie 0.
   "no checks reported" : réessayer toutes les 15 secondes, 6 fois. Toujours rien :
   arrêt, sauf pour le ticket socle qui apporte la CI (elle tourne alors sur sa propre
   demande). Rouge : boucle de correction, trois tentatives. Sur une carte de livraison
   soumise à revue, toute correction de code repart chez le codeur. Après la CI, contrôler
   le verdict sur le `headRefOid` actuel. Appelé par feature : rendre la main.

6. **POINT D'ARRÊT : porte 2.** Seul : le lien, la fiche QA, à tester à l'écran oui ou
   non, le commit, et les cases "Porte 2" de `_Méthode/Portes.md` non cochées.
   "Dites go, go tout, go 2 4, ou ce qui ne va pas." Preuve : le "go" écrit.
   Sur une carte Hermès en mode normal, transmettre le rapport avec la preuve de revue
   par le canal habituel du ticket, puis terminer la carte en attente du feu vert. Le mode nuit autorisé
   poursuit à l'étape 7 avec sa propre autorisation et les mêmes preuves.

7. **Fusionner, dans l'ordre des dépendances.** CI verte, `headRefOid` égal au commit du
   rapport. Sur une livraison Hermès, exiger à nouveau la preuve de revue sur ce même SHA.
   `gh pr merge <pr> --squash --delete-branch --match-head-commit <oid>
   --subject "<titre> (ticket #<n>)" --body-file "$F"`. Conflit : merge
   d'`origin/preprod` dans la branche, verifier, push, la porte 2 se rejoue. Si la revue
   est exigée, faire reprendre le candidat par le codeur avant un nouveau push.
   Preuve : état `MERGED`.
   En mode nuit, arrêter la carte de livraison ici. Le ticket reste ouvert jusqu'au matin.

8. **Fermer le ticket et tenir la note.**
   `gh issue close <n> --comment "Livré dans preprod par la demande de fusion #<pr>, commit <code>. Pas encore en ligne."`
   Commit mémoire (R3) : dans la note du ticket, `statut: valide` et une ligne datée en
   fin de "Journal de l'agent", "Livré dans preprod, #<pr>, pas encore en ligne".
   Preuve : l'issue fermée, le commit mémoire poussé.

9. **Ranger.** `git -C "$BASE" worktree remove "$ARBRE"`, branche locale retirée.
   Après le lot, CI de `preprod` : rouge, alerter, ne plus rien fusionner.

**L'utilisateur a fusionné lui-même.** Vérifier l'état, puis étapes 8 et 9. Un commit de
fusion au lieu d'un squash : le signaler.

## Boucle de correction, après le premier push

Un nouveau commit sur la branche, jamais `--amend`, jamais de rebase. La correction et
une ligne datée dans le "Journal de l'agent" de la note. Verifier, push, porte 2 rejouée.

## Étapes, mode mise en ligne

1. **Situer**, dans `BASE` : `git fetch origin`, `git rev-list --count origin/main..origin/preprod`
   supérieur à 0, tickets cités `CLOSED`, mots interdits, CI de `preprod` verte.

2. **Préparer la porte 3** avec les cases "Porte 3" de `_Méthode/Portes.md` : la base
   change-t-elle et quoi appliquer avant ; la commande de retour arrière ; le déploiement
   Coolify est-il activé. Lire `08 Mise en ligne/<Nom> - Déploiement`.

3. **Ouvrir la demande de fusion.** `gh pr create --base main --head preprod --title
   "Mise en ligne : <résumé>" --body-file "$F"`, corps `Tickets : #2, #3`. Puis
   `gh pr checks <pr> --watch --fail-fast`.

4. **POINT D'ARRÊT : porte 3.** Tickets, commit, base, retour arrière, cases non
   cochées. "Fusionner met en ligne. Dites go mise en ligne." Un "ok" ne suffit pas.

5. **Fusionner, en fusion normale.** `gh pr merge <pr> --merge --match-head-commit <oid>`.
   Jamais `--squash`, jamais `--delete-branch`. Preuve : `MERGED`, `preprod` visible.

6. **Prouver en ligne.** Déploiement activé : attendre la CI de déploiement, puis
   `curl -fsS -o /dev/null -w '%{http_code}' <adresse>`. Comparer la version affichée au
   commit de fusion, sinon "Version non vérifiée". Sans déploiement automatique :
   "Non vérifié : aucun déploiement automatique."

7. **Tenir la mémoire**, par un commit mémoire (R3) :
   - note projet : `prod: <adresse>`, `phase: en-ligne` à la première mise en ligne ;
   - `08 Mise en ligne/<Nom> - Déploiement` : environnements, "Dernière mise en ligne"
     avec la date et la preuve HTTP ;
   - `06 Qualité/<Nom> - Vérification` : une ligne par critère prouvé en ligne ;
   - `08 Mise en ligne/<Nom> - Bilan` : ce qui reste ouvert (tickets ouverts, non
     vérifié, gestes à refaire par l'utilisateur), et ce qu'on garde pour les prochains
     projets.
   Preuve : le code HTTP, le commit mémoire poussé.

## Points d'arrêt

- Porte 2, étape 6. Porte 3, étape 4. Aucune fusion sans "go" écrit.
- Arrêt de tout : fetch en échec, dossier pas propre, CI absente, mot interdit, réglages
  du dépôt faux, CI rouge sur `preprod` après une fusion.
- La mise en ligne casse : ne rien réparer seul. L'état, la preuve, le retour arrière.

## Preuve attendue

Par ticket : la demande de fusion, le commit testé, la CI, le "go" cité, l'issue fermée,
le commit mémoire de la note. Mise en ligne : la preuve HTTP, les quatre notes à jour.

## Interdits

- Pousser en force. `--no-verify`. `--admin`. `--auto`. `--amend` après le premier push.
- Fusionner sans "go" écrit, sur une CI rouge ou un commit non testé.
- Écrire `Closes`, `Fixes` ou `Resolves` devant un numéro.
- Déduire un numéro de demande de fusion.
- Commiter du code sur `main` ou `preprod`. Supprimer `preprod`.
- Dire "en ligne" ou "ça marche" sans la sortie citée.
- Lire un `.env` ou un secret. Changer un réglage de Docker, de Coolify ou du dépôt.
