"""Structure d'un dossier projet dans le vault « Projets ».

Source unique : le modèle, la commande `nouveau` et le vérificateur lisent tous cette liste.
Chaque note : (titre sans le préfixe projet, type, agent, résumé, corps).
Sources : pipeline-projet.md (agents et livrables), skill cadrage du harness (PRD, écrans, stories),
BMAD-METHOD (brief, PRD, DESIGN.md, EXPERIENCE.md, décision, ticket, atelier discovery, entretien),
Teresa Torres (arbre opportunités-solutions), cartographie des hypothèses (Strategyzer).
"""

SECTIONS = [
    {
        "dossier": "01 Discovery",
        "sujet": "Comprendre le problème avant de choisir une solution.",
        "profil_phase": """# Discovery · Responsable produit

## Mission

Vous êtes le responsable produit (`product-manager`). Aidez l'utilisateur à décider
si un problème mérite d'être résolu, pour qui et avec quel résultat attendu.
Cherchez d'abord le travail que la personne essaie d'accomplir, la difficulté
qu'elle rencontre et ce qu'elle fait déjà pour la contourner.

## Posture

- Une idée est un point de départ. Accueillez-la dans les mots de l'utilisateur,
  puis cherchez ce qui pourrait la confirmer ou l'infirmer.
- Demandez un épisode récent et concret. Faites préciser le déclencheur, les étapes,
  les personnes impliquées et les conséquences de la difficulté.
- Distinguez ce qu'une personne a dit, ce qu'elle a fait et votre interprétation.
  Indiquez l'origine d'un constat et la date d'une source. Un seul entretien
  peut révéler une piste. Pour dire qu'elle revient, indiquez chez qui.
- Pour une affirmation qui change la suite, revenez à la source directe.
  Comparez avec une observation indépendante quand c'est possible.
- Présentez les contradictions qui changent la décision. Si une preuve manque,
  dites comment l'obtenir sans lancer tout le projet.

## Méthode

1. Lisez **Idée brute** et les résumés de la phase. Ouvrez les notes d'entretien
   ou de recherche qui répondent aux questions encore ouvertes.
2. Décrivez le problème en une phrase. Précisez la situation, les personnes visées,
   le contournement actuel et le résultat observable qui compterait pour elles.
3. Utilisez **Entretiens** pour rassembler les constats et leurs liens. Dans
   **Recherche et existant**, comparez les alternatives réelles, y compris les méthodes
   manuelles. Notez pour chacune ce qu'elle résout et ce qui reste à vérifier.
4. Construisez dans **Problème et opportunité** un arbre qui relie le résultat visé
   aux difficultés à résoudre, puis aux pistes à tester.
5. Dans **Hypothèses et risques**, commencez par l'hypothèse dont l'échec ferait le
   plus changer le projet. Associez-lui un test faisable et un signal de réussite.
6. Faites émerger les arbitrages avec les séries de questions du skill. Reliez chaque
   question importante à une incertitude qui peut changer la suite.

## Livrable et passage de phase

- **Synthèse discovery** contient le problème, la cible, les constats les plus solides,
  les hypothèses encore ouvertes et la recommandation pour la suite.
- Pour recommander de poursuivre, réorienter ou arrêter, indiquez le constat qui pèse
  le plus et ce qui pourrait faire changer l'avis. L'utilisateur tranche.
- Le prochain cadrage doit pouvoir retrouver les sources et les questions à reprendre
  depuis la synthèse. Vérifiez que les notes liées permettent de remonter aux constats.
""",
        "notes": [
            ("Idée brute", "discovery", "HUMAIN",
             "L'idée telle qu'elle est venue, sans tri.",
             """## L'idée en vrac
<!-- Coller la note vocale, le message ou le texte d'origine. Rien n'est corrigé ici. -->

## Pourquoi maintenant
-

## Ce qui me ferait dire « c'est réussi »
-
"""),
            ("Problème et opportunité", "discovery", "product-manager",
             "Le problème, pour qui, et la preuve qu'il existe.",
             """## Le problème en une phrase
<!-- Qui souffre de quoi, dans quelle situation. Pas de solution dans cette phrase. -->

## Comment il est contourné aujourd'hui
-

## Preuves
| Preuve | Source | Date |
| --- | --- | --- |
|  |  |  |

## Résultat visé
<!-- Un résultat mesurable, pas une fonctionnalité. Racine de l'arbre opportunités-solutions. -->

## Arbre opportunités-solutions
<!-- Au moins 3 opportunités avant de choisir. Pour chacune : solutions envisagées, puis l'expérience qui la teste. -->
- Résultat :
  - Opportunité 1 :
    - Solution :
      - Test :
  - Opportunité 2 :
  - Opportunité 3 :
"""),
            ("Utilisateurs et personas", "discovery", "ux-designer",
             "Qui utilise le produit, avec des personnes nommées.",
             """## Personnes
<!-- Une personne nommée et située, pas « l'utilisateur ». Ex. : Mamie Jo, 78 ans, sur sa tablette le dimanche. -->
| Personne | Situation | Ce qu'elle veut accomplir | Ce qui la freine | Appareil |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Tâches à accomplir (jobs to be done)
- Quand …, je veux …, pour …

## Qui n'est pas visé
-
"""),
            ("Entretiens", "discovery", "researcher",
             "Ce que les utilisateurs disent et font, séparé de notre interprétation.",
             """## Entretiens menés
<!-- Une note par entretien, créée avec le modèle « Entretien utilisateur », liée ici. -->
-

## Ce qui revient
| Constat | Entendu chez | Combien de fois |
| --- | --- | --- |
|  |  |  |

## Ce qui nous a surpris
-
"""),
            ("Recherche et existant", "discovery", "researcher",
             "Ce qui existe, ce qui se fait, ce qui n'est pas possible, sources datées.",
             """## Ce qui existe déjà
| Solution | Ce qu'elle fait bien | Ce qui manque | Prix | Source et date |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Ce qui se fait couramment
-

## Ce qui n'est pas possible
<!-- Limite technique, légale ou commerciale, avec sa source. -->
-

## Ce qu'on en retient pour le projet
-
"""),
            ("Hypothèses et risques", "discovery", "cpo",
             "Les paris du projet, classés, et comment les tester.",
             """## Cartographie des hypothèses
<!-- Classer : importance (le projet tombe si c'est faux) × preuve (ce qu'on sait déjà). On teste d'abord « important et peu prouvé ». -->
| Hypothèse | Nature | Importance | Preuve | Test prévu | Résultat |
| --- | --- | --- | --- | --- | --- |
|  | désirabilité |  |  |  |  |
|  | faisabilité |  |  |  |  |
|  | viabilité |  |  |  |  |
|  | légalité |  |  |  |  |

## Risques
| Risque | Probabilité | Impact | Parade |
| --- | --- | --- | --- |
|  |  |  |  |
"""),
            ("Synthèse discovery", "discovery", "product-manager",
             "La décision de sortie de discovery : on y va, on change, ou on arrête.",
             """## En une page
- Problème :
- Pour qui :
- Ce qui rend la solution différente :
- Critères de réussite :
- Périmètre de départ :

## Décision
<!-- On y va / on pivote / on arrête. Reportée au journal des décisions. -->

## Questions encore ouvertes
-
"""),
        ],
    },
    {
        "dossier": "02 Cadrage",
        "profil_phase": """# Cadrage · Responsable de la stratégie produit

## Mission

Vous êtes le responsable de la stratégie produit (`cpo`). Transformez la conclusion
de Discovery en engagement de produit clair. À la fin, chacun doit savoir pour qui
on construit, ce que la première version permet de faire et comment on jugera son résultat.

## Posture

- Faites apparaître le prix d'un ajout. Précisez ce qu'il décale, complique ou rend
  plus difficile à valider. Proposez un arbitrage que l'utilisateur peut comprendre.
- Distinguez les contraintes confirmées, les préférences et les hypothèses.
  Pour un chiffre incertain, indiquez le scénario et les éléments du calcul.
- Présentez une mesure de réussite du produit et un test de la fonctionnalité
  comme deux choses distinctes. Un export peut fonctionner sans faire gagner du temps.
- Pour une priorité fondée sur une hypothèse, précisez quand la réévaluer
  et quel résultat ferait changer de direction.
- Quand deux objectifs s'opposent, formulez les options avec leurs effets.
  Conservez la décision validée et sa raison dans le journal.

## Méthode

1. Lisez la **Synthèse discovery**. Reprenez le public visé, le problème confirmé
   et les questions ouvertes. Identifiez celles qui bloquent le périmètre.
2. Écrivez le **PRD**, la note des exigences produit. Décrivez le résultat à atteindre,
   les usages couverts et les limites qui doivent être comprises par la suite.
3. Dans **Priorités**, définissez la plus petite version qui rend un service complet
   à une personne réelle. Justifiez les priorités par le besoin, les dépendances
   et l'effort ou l'incertitude connus. Signalez les paris à tester.
4. Dans **Stories**, décrivez une action et son résultat du point de vue de l'utilisateur.
   Pour chaque story retenue, liez au moins un critère observable dans
   **Critères d'acceptation**, avec un cas limite si le résultat peut être ambigu.
5. Adoptez le regard indiqué dans **Contraintes techniques**, **Juridique et données**
   et **Coûts**. Faites remonter tôt les contraintes qui changent le périmètre,
   la faisabilité ou le budget. Distinguez une obligation sourcée d'un point à vérifier.
6. Faites valider les arbitrages encore ouverts. Notez clairement dans le PRD ce qui
   est hors périmètre et les retraits décidés en cours de cadrage.

## Livrable et passage de phase

- PRD, priorités, stories et critères doivent se correspondre. Une priorité sans
  besoin démontré ou une exigence sans moyen de vérification reste ouverte.
- Le design doit pouvoir identifier les parcours prioritaires et leurs limites.
  La conception doit retrouver les contraintes et les décisions qui les justifient.
- Dans la passation, indiquez les arbitrages validés et les questions qui restent,
  avec le lien vers la note concernée.
""",
        "sujet": "Fixer ce qu'on construit, ce qu'on ne construit pas, et comment on saura que c'est fini.",
        "notes": [
            ("Pilotage", "cadrage", "orchestrator",
             "Quels agents sont appelés, dans quel ordre, avec quelles cartes, et qui est sauté et pourquoi.",
             """## Agents par phase
<!-- Copie rognée du modèle pipeline-projet de l'orchestrateur : une raison écrite par agent retiré. -->
| Phase | Agent | Note livrée | Carte |
| --- | --- | --- | --- |
|  |  |  |  |

## Séquence
-

## Contrôle de fin de projet
| Agent | Appelé | Note livrée | Sinon, pourquoi |
| --- | --- | --- | --- |
|  |  |  |  |
"""),
            ("PRD", "cadrage", "product-manager",
             "Le besoin, le périmètre et ce qu'on ne fait pas.",
             """## Problème
<!-- Repris de la synthèse discovery, en trois phrases au plus. -->

## Utilisateurs
<!-- Renvoyer aux personnes nommées de la discovery. -->

## Ce que ça fait
-

## C'est fini quand
- [ ]

## Hors périmètre
-

## Retiré du périmètre
<!-- Ce qui était prévu puis retiré, avec la date et la raison. -->
-

## Points sensibles
<!-- Données personnelles, argent, sécurité, accessibilité. -->
-

## Hypothèses
-

## Mesures de réussite
| Mesure | Valeur de départ | Cible | Comment on la lit |
| --- | --- | --- | --- |
|  |  |  |  |
"""),
            ("Priorités", "cadrage", "cpo",
             "Ce qui passe en premier, et pourquoi.",
             """## Version minimale (MVP)
<!-- Le plus petit ensemble qui résout le problème pour une personne nommée. -->
-

## Classement
| Élément | Doit / Devrait / Pourrait / Pas maintenant | Raison |
| --- | --- | --- |
|  |  |  |
"""),
            ("Stories", "cadrage", "product-manager",
             "Les user stories, source des tickets.",
             """## S1 : titre court
En tant que …, je veux …, pour ….
C'est fini quand :
- [ ] condition vérifiable
"""),
            ("Contraintes techniques", "cadrage", "cto",
             "Les contraintes techniques et ce qu'on s'interdit.",
             """## Plateformes visées
- Mobile / web / ordinateur :

## Pile imposée ou préférée
-

## Ce qu'on s'interdit
-

## Hébergement
- Production : DOMAINE_PROD (voir harness.conf)
- Préproduction : DOMAINE_PREPROD, derrière un login
"""),
            ("Juridique et données", "cadrage", "clo",
             "Licences, données personnelles, obligations.",
             """## Données personnelles
| Donnée | Pourquoi | Durée de conservation | Qui y accède |
| --- | --- | --- | --- |
|  |  |  |  |

## Licences des dépendances et contenus
-

## Obligations (RGPD, consentement, mentions)
-
"""),
            ("Coûts", "cadrage", "cfo",
             "Ce que le projet coûte à faire tourner, et s'il tient.",
             """## Coûts mensuels
| Poste | Montant | Source |
| --- | --- | --- |
|  |  |  |

## Viabilité
-
"""),
            ("Critères d'acceptation", "cadrage", "qa-engineer",
             "Comment on saura que c'est fini, vérifiable par commande ou par geste.",
             """## Critères
| Critère | Comment le vérifier | Preuve attendue |
| --- | --- | --- |
|  |  |  |
"""),
        ],
    },
    {
        "dossier": "03 Design",
        "profil_phase": """# Design · Spécialiste de l'expérience utilisateur

## Mission

Vous êtes le spécialiste de l'expérience utilisateur (`ux-designer`).
Traduisez les besoins validés en parcours qu'on peut comprendre, parcourir et
tester. Aidez l'utilisateur à décider des comportements et de l'identité visuelle.

## Posture

- Jugez un parcours depuis le point de vue de la personne qui s'en sert. Précisez
  ce qu'elle cherche, ce qu'elle sait à ce moment et ce qui lui confirme la suite.
- Demandez des retours sur un écran, une décision ou une tâche précise. Pour un
  désaccord, montrez les effets concrets des options sur le parcours.
- Traitez dès le départ la lecture, le clavier, la visibilité du focus et les
  messages d'erreur. Vérifiez les contrastes et notez le résultat mesuré.
- Pour une référence visuelle, relevez le principe qui est utile au projet,
  par exemple une hiérarchie claire ou une formulation d'erreur facile à comprendre.
- Réutilisez le même comportement pour des actions équivalentes. Avant de fixer
  l'apparence d'un composant, vérifiez comment on l'utilise et quel retour il donne.

## Méthode

1. Lisez le **PRD**, les **Stories** prioritaires et les **Critères d'acceptation**.
   Repérez les appareils, les contextes et les besoins d'accès qui influencent l'usage.
2. Dans **Expérience (UX)**, décrivez les parcours prioritaires.
   Pour chacun, indiquez le point d'entrée, les choix, le résultat et la reprise
   si la personne interrompt la tâche ou se trompe.
3. Dans **Écrans et états**, associez les étapes aux écrans et couvrez les états
   attendus par le skill. Précisez les libellés, confirmations et erreurs qui
   changent la compréhension ou l'action possible.
4. Dans **Identité visuelle** et **Thèmes**, adoptez le regard du designer de marque.
   Justifiez les choix de contraste, de typographie et de hiérarchie par leur usage.
5. Liez la maquette de référence depuis **Maquettes**. Faites parcourir
   une tâche de bout en bout et relevez où l'utilisateur hésite, perd le fil
   ou interprète mal un retour. Notez les corrections décidées.

## Livrable et passage de phase

- Chaque besoin prioritaire mène à un parcours et chaque parcours à des écrans ou
  des résultats identifiables. Les états et erreurs importants sont décrits.
- La maquette indique ce qui a été validé et ce qui reste à tester.
  Une interaction simulée est signalée comme telle.
- La conception reçoit les comportements à reproduire, les contraintes
  d'accessibilité et les choix visuels qui ont un impact technique.
""",
        "sujet": "L'expérience (UX), l'identité visuelle (UI) et les thèmes.",
        "notes": [
            ("Inspirations", "design", "ux-designer",
             "Ce qu'on aime, ce qu'on refuse, avec des exemples.",
             """## Références qui inspirent
| Référence | Ce qu'on en garde | Lien |
| --- | --- | --- |
|  |  |  |

## Anti-modèles
<!-- Ce qu'on refuse de reproduire, et pourquoi. -->
-
"""),
            ("Expérience (UX)", "design", "ux-designer",
             "Fondations, architecture de l'information, parcours, ton et accessibilité.",
             """## Fondations
- Format : mobile / web / ordinateur / plusieurs
- Système d'interface : (shadcn, natif, maison…)

## Architecture de l'information
<!-- Chaque besoin a un écran, chaque écran a un parcours qui y mène. -->
-

## Parcours clés
<!-- Un parcours raconté avec une personne nommée, en étapes numérotées, jusqu'au moment fort. -->
### Parcours 1 :
1.

## Voix et ton
<!-- Microcopie : boutons, erreurs, confirmations. -->
-

## Comportements des composants
-

## Accessibilité (plancher)
- Clavier, lecteur d'écran, cibles tactiles, mouvement réduit :

## Sujets à surveiller
<!-- Hors ligne, notifications, langues, densité d'information, mode sombre… -->
-
"""),
            ("Écrans et états", "design", "ux-designer",
             "Chaque écran, comment on y arrive, et ses six états.",
             """## Nom de l'écran
- Sert à : une phrase.
- On y arrive par : écran ou action.
- États :
  - vide :
  - chargement :
  - erreur :
  - plein :
  - partiel :
  - succès :
"""),
            ("Identité visuelle (UI)", "design", "brand-designer",
             "Marque et style, couleurs, typographie, espacements, formes, composants.",
             """## Marque et style
-

## Couleurs
| Jeton | Rôle | Valeur | Contraste mesuré |
| --- | --- | --- | --- |
| primaire |  |  |  |
| fond |  |  |  |
| texte |  |  |  |

## Typographie
| Niveau | Police | Taille | Graisse |
| --- | --- | --- | --- |
|  |  |  |  |

## Espacements et grille
-

## Profondeur et formes
- Ombres, arrondis :

## Composants
-

## À faire / à éviter
-
"""),
            ("Thèmes", "design", "brand-designer",
             "Thème clair, thème sombre, et les contrastes mesurés.",
             """## Thème clair
| Jeton | Valeur | Contraste |
| --- | --- | --- |
|  |  |  |

## Thème sombre
| Jeton | Valeur | Contraste |
| --- | --- | --- |
|  |  |  |

## Règles
- Le contraste du texte courant atteint 4,5:1 au moins (WCAG AA), mesuré, pas estimé.
"""),
            ("Maquettes", "design", "ux-designer",
             "Où sont les maquettes, et laquelle fait foi.",
             """## Maquette de référence
<!-- Lien vers le fichier (HTML, Figma, Excalidraw). Elle fait foi pour couleurs, typographie et espacements. -->
-

## Versions précédentes
-
"""),
        ],
    },
    {
        "dossier": "04 Conception",
        "profil_phase": """# Conception · Architecte technique

## Mission

Vous êtes l'architecte technique (`technical-architect`). Traduisez le périmètre,
les parcours et les contraintes en un plan de construction que l'équipe pourra
réaliser, vérifier et faire évoluer.

## Posture

- Préférez la structure la plus simple qui couvre les usages et les contraintes
  validés. Pour une dépendance ou un service de plus, expliquez le besoin qu'il couvre
  et ce qu'il ajoute en exploitation.
- Rendez visibles les choix coûteux à inverser. Présentez les options réalistes,
  leurs conséquences et le compromis recommandé. Faites valider les arbitrages ouverts.
- Indiquez ce qui a été vérifié, ce qui repose sur une hypothèse et ce qui nécessite
  une vérification avant de construire. Exprimez une contrainte sous une forme testable.
- Suivez le chemin des données et les défaillances. Pour un échange important,
  demandez qui appelle qui, où se trouve l'état et comment le système reprend.

## Méthode

1. Lisez les **Critères d'acceptation**, les **Contraintes techniques** et les notes
   de design utiles. Repérez les décisions qui engagent plusieurs composants,
   des données personnelles ou des opérations difficiles à annuler.
2. Dans **Architecture**, situez les utilisateurs, composants et services externes.
   Décrivez les échanges importants, les responsabilités et les modes de panne.
   Pour chaque décision structurante, liez une note datée qui donne le contexte,
   les options envisagées, la raison du choix et ses conséquences.
3. Dans **Données**, précisez quelles données sont créées, par qui, où elles vivent
   et comment on les conserve, les supprime ou les restaure. Dans **Sécurité**,
   relevez les accès et opérations sensibles, leurs contrôles et leurs vérifications.
4. Dans **Specs**, reliez les comportements attendus aux stories et aux tests.
   Décrivez les cas d'échec qui changent le résultat, comme une opération interrompue
   ou une saisie invalide, et le comportement attendu à la reprise.
5. Dans **Plan de travail**, ordonnez les lots par dépendance. Chaque lot a un
   résultat observable et une façon de le vérifier. Faites remonter tôt les
   incertitudes qui peuvent bloquer plusieurs lots.

## Livrable et passage de phase

- Vérifiez qu'un besoin prioritaire se retrouve dans les composants, les
  spécifications et le plan de travail. Les choix sensibles et les questions
  résiduelles doivent être faciles à retrouver.
- Pour le skill tickets, rendez clair l'ordre des lots, leurs dépendances
  et les critères qui serviront à vérifier chaque résultat.
- Présentez les décisions attendues avant la porte 1 selon le skill de cadrage.
""",
        "sujet": "Comment le produit est construit, avant d'écrire le code.",
        "notes": [
            ("Architecture", "conception", "technical-architect",
             "Frontières, contrats, modes de panne.",
             """## Schéma d'ensemble
```mermaid
flowchart LR
  utilisateur --> appli --> donnees[(données)]
```

## Décisions d'architecture
<!-- Une ligne par décision, détail dans le journal des décisions. -->
-

## Modes de panne
| Panne | Ce que voit l'utilisateur | Parade |
| --- | --- | --- |
|  |  |  |
"""),
            ("Données", "conception", "data-architect",
             "Schémas, stockage, durée de conservation.",
             """## Modèle de données
-

## Stockage et sauvegarde
-
"""),
            ("Sécurité", "conception", "security-engineer",
             "Menaces, données sensibles, points d'entrée.",
             """## Points d'entrée
-

## Menaces et parades
| Menace | Parade |
| --- | --- |
|  |  |
"""),
            ("Specs", "conception", "spec-driven-development",
             "Les spécifications exécutables, découpées en tâches.",
             """## Spécifications
-
"""),
            ("Plan de travail", "conception", "implementation-planner",
             "Découpage, dépendances, chemin critique.",
             """## Chemin critique
-

## Lots
| Lot | Dépend de | Tickets |
| --- | --- | --- |
|  |  |  |
"""),
        ],
    },
    {
        "dossier": "05 Tickets",
        "sujet": "Le travail découpé, une note par ticket, reliée à son issue GitHub.",
        "notes": [],
    },
    {
        "dossier": "06 Qualité",
        "sujet": "Les preuves que ça marche, et ce qui a cassé.",
        "notes": [
            ("Plan de test", "qualite", "qa-engineer",
             "Ce qu'on teste, comment, et la non-régression.",
             """## Tests automatisés
-

## Tests à la main
| Geste | Résultat attendu |
| --- | --- |
|  |  |
"""),
            ("Pannes", "qualite", "debugger",
             "Chaque panne, sa cause racine et sa correction.",
             """## Pannes
| Date | Symptôme | Cause racine | Correction | Ticket |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
"""),
            ("Vérification", "qualite", "verifier",
             "La porte de sortie, preuves à l'appui.",
             """## Preuves
| Critère | Commande ou geste | Sortie obtenue |
| --- | --- | --- |
|  |  |  |
"""),
        ],
    },
    {
        "dossier": "07 Décisions",
        "sujet": "Ce qui a été tranché, par qui, et pourquoi.",
        "notes": [
            ("Journal des décisions", "decision", "HUMAIN",
             "Une ligne par décision tranchée.",
             """Une décision écrite ici ne se rouvre pas sans raison écrite.
Une décision lourde a sa propre note (modèle « Décision »), liée dans la colonne Détail.

| Date | Décision | Raison | Décidé par | Détail |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
"""),
        ],
    },
    {
        "dossier": "08 Mise en ligne",
        "sujet": "Déployer, prouver, puis faire le bilan.",
        "notes": [
            ("Déploiement", "mise-en-ligne", "platform-engineer",
             "Chaîne de déploiement, environnements, preuve que l'appli répond.",
             """## Environnements
| Environnement | Adresse | Branche |
| --- | --- | --- |
| production |  | main |
| préproduction |  | preprod |

## Dernière mise en ligne
- Date :
- Preuve :
"""),
            ("Bilan", "mise-en-ligne", "chief-of-staff",
             "Ce qui reste ouvert après la mise en ligne.",
             """## Ce qui reste ouvert
-

## Ce qu'on garde pour les prochains projets
-
"""),
        ],
    },
    {
        "dossier": "09 Journal",
        "sujet": "Comptes rendus de séances et de réunions, dans l'ordre.",
        "notes": [],
    },
]

# Modèles de notes isolées, pour le plugin natif « Modèles » d'Obsidian ({{title}}, {{date}}).
MODELES_NOTES = {
    "Ticket": """---
projet: "[[PROJET]]"
type: ticket
statut: a-faire
agent: hermes
execution: En attente
numero:
issue:
branche:
haut: "[[PROJET - 05 Tickets]]"
---

# {{title}}

## Le ticket
<!-- Recopié de l'issue GitHub, avec sa date. -->
- Besoin :
- C'est fini quand :
  - [ ]
- Dépend de :

## Plan
1.

## Décisions
-

## Journal de l'agent
-

## Fiche QA
<!-- Modèle « Fiche QA ». -->
""",
    "Décision": """---
projet: "[[PROJET]]"
type: decision
statut: brouillon
resume:
haut: "[[PROJET - Journal des décisions]]"
---

# {{title}}

## Contexte

## Options envisagées
| Option | Pour | Contre |
| --- | --- | --- |
|  |  |  |

## Décision

## Conséquences

## Comment on vérifiera
""",
    "Entretien utilisateur": """---
projet: "[[PROJET]]"
type: discovery
statut: brouillon
resume:
haut: "[[PROJET - Entretiens]]"
---

# {{title}}

Date : {{date}}

## Participant
- Profil, contexte, appareil :

## Ce qu'il a dit
-

## Ce qu'il fait
-

## Difficultés et objectifs
-

## Notre interprétation
<!-- Séparée de ce qui a été dit. -->
-
""",
    "Atelier discovery": """---
projet: "[[PROJET]]"
type: discovery
statut: brouillon
resume:
haut: "[[PROJET - 01 Discovery]]"
---

# {{title}}

Date : {{date}}

## Objectifs

## Besoins exprimés

## Contraintes

## Hors périmètre

## Risques et inquiétudes

## Décisions

## Questions ouvertes
""",
    "Compte rendu": """---
projet: "[[PROJET]]"
type: journal
statut: valide
resume:
haut: "[[PROJET - 09 Journal]]"
---

# {{title}}

Date : {{date}}

## Ce qui a été fait

## Ce qui a été décidé
<!-- Chaque décision est aussi reportée au journal des décisions. -->

## Ce qui reste
""",
}
