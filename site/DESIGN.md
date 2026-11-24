# Design du site Harness

Le guide fourni inspire le contraste entre le bandeau bleu nuit et les pages claires. Le site garde ses six pages HTML et son identité Harness. La feuille `assets/style.css` et le script `assets/site.js` sont communs à toutes les pages.

| Élément | Traitement |
| --- | --- |
| Fond clair | Blanc, avec des sections gris doux et des cartes plates |
| Bandeau | Bleu nuit `#1a2129`, photo d’atelier sur l’accueil |
| Action principale | Bleu `#1c69d4`, texte blanc, bouton rectangulaire |
| Titres et texte | Inter, titres à 700 et texte courant à 300, avec repli système |
| Navigation | Barre fixe en haut, lien actif souligné et menu sur mobile |
| Accessibilité | Lien d’évitement, focus visible, mouvement réduit et mode clair ou sombre |

Les six pages ont chacune un sujet.

- **Accueil** présente le Harness et oriente vers les guides.
- **Méthode** décrit le coffre Obsidian, le cycle du ticket et les validations.
- **Installation** distingue l’installation du moteur, le parcours par le coffre et le raccourci Next.js.
- **OpenCode** explique la lecture des règles, la reprise d’une session et la revue.
- **Hermès** décrit le relais depuis Obsidian et le mode nuit.
- **GitHub** couvre l’initialisation du dépôt, Projects, les demandes de fusion et les contrôles.

Ouvrir `index.html` depuis le dossier `site/`. Le style, les scripts et le visuel de l’accueil sont chargés depuis `assets/`. Sur téléphone, vérifier le menu et le défilement des tableaux. Le choix de thème est partagé entre les pages via `harness-theme`.
