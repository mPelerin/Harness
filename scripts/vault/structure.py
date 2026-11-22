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
