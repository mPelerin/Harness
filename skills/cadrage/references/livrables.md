# Contrôles des livrables de cadrage

Consulter la section de la phase en cours. Dans toutes les phases, désigner les
personnes par un rôle ou un prénom inventé.

## Discovery

- Dater les sources.
- Construire un arbre des opportunités avec le problème en haut et au moins trois
  opportunités, chacune sur sa branche.
- Conclure la synthèse par la décision de poursuivre, de réorienter ou d'arrêter.

## Cadrage

- Reprendre la synthèse Discovery dans le PRD. Dater chaque entrée de la rubrique
  « Retiré du périmètre ».
- Numéroter les stories S1, S2 et ainsi de suite. Donner à chacune des conditions
  vérifiables par commande ou par geste. Reporter les critères d'acceptation dans
  les règles métier de `AGENTS.md` à la finalisation.
- Dans **Pilotage**, ordonner les profils Hermès appelés et donner une raison pour
  chaque profil écarté. L'orchestrateur lit la note avant de répartir le travail.
- Dans **Contraintes techniques**, déterminer le type d'application (landing, web,
  Android, Android et web, service sans écran) d'après les appareils des personas.
  Choisir ensuite la pile d'après les besoins, sans pile par défaut. Indiquer le rôle,
  l'origine et la version de chaque bibliothèque. Le ticket socle installe uniquement
  la pile choisie.

## Design

- Si l'application est sans écran, passer la phase et inscrire la raison dans
  chaque note concernée.
- Mesurer les contrastes.
- Dans **Écrans et états**, couvrir les six états prévus par le modèle pour chaque écran.

## Conception

- **Architecture** indique les frontières et les modes de panne.
- **Données** contient le schéma et les durées de conservation.
- **Sécurité** indique les points d'entrée et les données sensibles. Elle sert à
  déterminer quels tickets portent la mention `Sensible`.
- **Specs** découpe le travail en tâches.
- **Plan de travail** décrit les lots, leurs dépendances et le chemin critique.
  Le skill tickets s'appuie sur ce plan pour établir l'ordre de réalisation.
