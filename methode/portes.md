<!-- Adapté de kit-agents-ia, Mathis Gorvien, licence MIT (voir LICENCES-TIERS.md). -->

# Les trois portes humaines

Une porte est un point d'arrêt. L'agent prépare, propose et prouve. **Vous, vous ouvrez la porte.** Il n'en passe aucune seul.

```
Ticket ➡️ PORTE 1 ➡️ l'agent code ➡️ PORTE 2 ➡️ PORTE 3 ➡️ en ligne
          décider               tester      fusionner
```

Comment s'en servir : à chaque porte, vous lisez la liste. Une case que vous ne pouvez pas cocher veut dire "on n'ouvre pas encore".

**Deux branches durables.** `main` = ce qui est en ligne. `preprod` = le travail validé, pas encore en ligne. La branche par défaut du dépôt GitHub est toujours `main`, jamais `preprod`.

```
Cadrage ➡️ PORTE 1 ➡️ tickets ➡️ [ par ticket : code ➡️ PORTE 2 ➡️ fusion dans preprod ] ➡️ PORTE 3 ➡️ en ligne
          go écrit                                     tester     ticket fermé à la main      preprod vers main
```

- La porte 1 du cadrage est votre "go" écrit après lecture des notes de cadrage du projet (`02 Cadrage/` et `03 Design/` dans le vault).
- La porte 1 d'un ticket est votre "go" à sa création. L'agent ne redemande avant le code que s'il lui reste une question, ou si le ticket est sensible : argent, droits d'accès, données personnelles, base de données, nouvelle bibliothèque.
- Plusieurs tickets se font d'affilée. La porte 2 arrive une fois pour tout le lot : "go tout", ou "go 2 4".
- Après la porte 2, l'agent fusionne le ticket dans `preprod`, puis le ferme à la main. Rien n'est en ligne.
- La porte 3 revient à chaque mise en ligne : la fusion de `preprod` vers main. Elle peut emporter plusieurs tickets.
- Un ticket ne se ferme jamais tout seul : aucun `Closes #`, nulle part.

---

## Porte 1 : décider, avant le code

**Qui décide :** vous. Pas l'agent.
**Quand :** à la création du ticket. Pour un ticket sensible, encore une fois avant la première ligne de code.

- [ ] Au cadrage : `AGENTS.md` est rempli, sans `<...>`, et je l'ai relu avec les documents.
- [ ] S'il restait des questions, l'agent me les a posées, en un seul message, et j'ai répondu.
- [ ] Le ticket dit ce qu'on fait, et ce qu'on **ne fait pas**.
- [ ] La rubrique "C'est fini quand" du ticket contient des phrases que je peux vérifier moi-même.
- [ ] Si le ticket touche à l'argent, aux droits d'accès ou à des données personnelles, c'est écrit dans le ticket.
- [ ] Si une nouvelle bibliothèque est demandée, j'ai vu son origine et sa version exacte.

**Pourquoi cette porte.** Les tests ne savent pas ce que "fini" veut dire pour vous. L'auteur du kit a trouvé à l'écran quatre défauts que ses tests ne voyaient pas, dont un titre coupé sur téléphone.

---

## Porte 2 : tester, avant le "go" de fusion

**Qui décide :** vous, après avoir testé. Une CI verte n'est pas un "oui".
**Quand :** la demande de fusion est ouverte, la CI est verte.
**Où :** en local, sur la branche du ticket. Il n'y a pas de serveur d'essai entre votre PC et la version en ligne.

**Exception, le mode nuit** (skill nuit, s'il est installé). Vous l'avez demandé la veille, en disant oui au mode nuit. Le lot est alors déjà fusionné dans `preprod` et visible sur l'adresse de préprod (`DOMAINE_PREPROD` de `harness.conf`), derrière un login. Vous testez là. Les tickets sont encore ouverts : votre "go" les ferme. Rien n'est en ligne.

- [ ] Chaque "c'est bon" de la demande de fusion pointe vers une **preuve** : commande et sortie, lien ou capture.
- [ ] J'ai lu le compte rendu de l'agent : ce qu'il n'a **pas fait** ou **pas pu vérifier**. Rien ne m'y surprend.
- [ ] J'ai déroulé les étapes **Écran** de la fiche QA, sur ordinateur **et** sur téléphone. S'il n'y en a pas, j'ai lu les preuves.
- [ ] J'ai testé le chemin qui doit **échouer** : mauvaise saisie, mauvais compte, double clic.
- [ ] S'il y a des comptes, j'ai vérifié avec de vrais comptes de test que l'un ne voit pas les données de l'autre.
- [ ] S'il y a une base de données, le changement a tourné sur une vraie base, pas seulement dans des tests qui l'imitent.
- [ ] La demande de fusion vise `preprod` et cite le bon ticket : `Ticket : #<numéro>`, sans `Closes`.
- [ ] La note du ticket (`05 Tickets/<Projet> - T<numéro> …` dans le vault) contient le plan, le journal de l'agent et la fiche QA.
- [ ] La branche porte un seul changement. Au premier envoi, elle avait un seul commit. La fusion se fera par squash.
- [ ] `gh pr checks` est tout vert.

**Pourquoi cette porte.** L'auteur du kit avait plus de 2 000 tests verts et une CI verte. Un appel au serveur tombait pourtant en erreur à chaque fois. Les tests imitaient la base : la vraie fonction n'avait jamais tourné.

---

## Porte 3 : fusionner preprod sur main, donc mettre en ligne

**Qui décide :** vous, et personne d'autre.
**Quand :** la porte 2 est passée. L'agent attend votre "go" écrit.

⚠️ Quand le déploiement Coolify du projet est activé, **fusionner sur main met en ligne**. Le "go" de fusion est donc aussi le "go" de mise en ligne.

Avant le "go" :

- [ ] Si la base de données change, le changement est listé et appliqué **avant** le code. J'ai vérifié son effet.
- [ ] Je sais comment revenir en arrière si ça casse. La commande est écrite.
- [ ] Ce n'est pas un moment où je ne pourrai pas surveiller ensuite.

Après la fusion :

- [ ] L'agent m'a donné la preuve que **la bonne version** est en ligne, pas seulement que le site répond.
- [ ] J'ai refait le parcours principal en ligne, avec un compte de test.
- [ ] Les tickets mis en ligne étaient déjà fermés un par un, à leur fusion dans `preprod`.
- [ ] Je jette un oeil aux erreurs dans l'heure qui suit.

**Pourquoi cette porte.** Le code se déploie tout seul, la base de données non. L'auteur du kit a eu une fonction cassée environ deux heures pour un changement de base oublié.

---

## À chaque porte

**Secrets**

- [ ] Aucun secret (clé, jeton, mot de passe) dans la conversation, le code, les commits ou la demande de fusion.
- [ ] Les fichiers `.env` restent hors de portée de l'agent. Je ne les colle jamais dans un chat.

**Données personnelles**

- [ ] Aucune vraie donnée de personne dans mes messages à l'agent : pas de vrai nom, e-mail, téléphone, adresse. Des données inventées.
- [ ] Les captures et les journaux que je colle sont nettoyés.

**Coût**

- [ ] Un agent qui tourne en boucle sans avancer, je l'arrête.
- [ ] Une fois par semaine, je regarde mes crédits d'agent et mes minutes de CI GitHub.

---

## Ce que l'agent ne fait jamais seul

| Action | Il lui faut |
| --- | --- |
| Commencer à coder un ticket | Votre "go" à sa création, et vos réponses s'il restait des questions. Un "go" de plus si le ticket est sensible. |
| Fusionner un ticket dans `preprod` | Votre "go" écrit de la porte 2, et une CI toute verte. En mode nuit : votre "oui" au mode nuit de la veille, et une CI toute verte |
| Pousser en force | Rien. C'est interdit. |
| Fusionner sur main | Votre "go" écrit de la porte 3, et une CI toute verte |
| Commiter directement sur main | Rien. C'est interdit. |
| Changer la base de données en ligne | Votre "go" écrit, à part |
| Ajouter une bibliothèque | Votre "go", après origine et version montrées |
| Contourner un hook avec `--no-verify` | Rien. C'est interdit. |
