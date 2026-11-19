# DESIGN.md : le style du site du harness

Ce fichier guide toute modification de `site/`. Il résume le style choisi pour le site et la façon dont il est appliqué ici, en HTML et CSS simples, sans framework.

Le style s'inspire d'un modèle de page éditoriale relevé à la date du 18.11.2026 (un modèle Next.js vendu sur shadcnblocks.com). On reprend l'esprit et le niveau d'animation. Aucun texte, logo ni image n'en vient.

## L'esprit

Un carnet papier haut de gamme. Fond crème, encre presque noire, une seule couleur d'accent ocre, titres serif énormes et serrés, petites étiquettes en police mono. Les animations sont lentes, floues puis nettes, jamais rebondissantes.

Trois règles font l'essentiel du rendu :

1. Un seul accent, l'ocre. Tout le reste en crème et en brun-noir.
2. Titres serif géants, espacement des lettres à -0.05em, interligne 1.
3. Chaque apparition combine opacité, flou de 4px et petite montée. Jamais d'apparition sèche.

## Couleurs

Les variables sont dans `assets/style.css`, en haut. Le site suit le réglage clair ou sombre du système (`prefers-color-scheme`). Le bouton lune ou soleil de la navigation force l'un des deux : il pose `data-theme` sur `html` et garde le choix dans le navigateur (`harness-theme`). Les variables sombres existent donc deux fois dans le CSS : sous la media query, et sous `:root[data-theme="dark"]`. Une couleur changée doit l'être aux deux endroits.

| Rôle | Clair | Sombre |
| --- | --- | --- |
| Fond | `#f4f3ee` | `#13110d` |
| Encre | `#1f1c18` | `#e8e6e1` |
| Carte | `#fefdfc` | `#1a1714` |
| Texte gris | `#625f5b` | `#a09c96` |
| Accent ocre | `#bc8b4c` | `#c99858` |
| Accent clair | `#e7d7be` | `#3e3323` |
| Fond de badge | `#f3ede3` | `#231e17` |
| Bordure | `#d9d7d2` | `#302d29` |

L'accent ne sert qu'à : un mot en italique dans les titres, les chiffres clés, les numéros 01 / 02, les étiquettes mono, les badges et le bouton d'appel final.

Un seul bloc sombre par page (`.sombre`). En mode sombre, il s'inverse pour rester le seul contraste fort.

## Typographie

| Rôle | Police | Taille | Espacement |
| --- | --- | --- | --- |
| Titre de page (h1) | DM Serif Display | 48 à 112px | -0.05em, interligne 1 |
| Titre de section (h2) | DM Serif Display | 36 à 60px | -0.05em, interligne 1 |
| Titre de carte (h3) | DM Serif Display | 22 à 24px | -0.025em |
| Texte | DM Sans | 18px (17px sur téléphone) | interligne 1.625 |
| Étiquettes | JetBrains Mono | 11 à 13px | majuscules, espacées |

Les polices viennent de Google Fonts. Sans elles, des polices système de la même famille prennent le relais.

## Mise en page

- Conteneur de 1024px au plus, marges de 40px, 16px sur téléphone.
- Sections très aérées (96px, 64px sur téléphone).
- Titres de section alignés à gauche, sous-titre gris de deux lignes environ.
- Séparateurs fins, pointillés entre les lignes d'une liste, ligne dégradée sous le haut de page.
- Fond en grille de points très pâle derrière le haut de page, qui s'efface en haut et en bas.
- Un "&" géant en filigrane derrière l'appel final de la page d'accueil.
- Rayons : 4px (code), 10px (boutons), 14px (cartes, tableaux), 18px (bloc sombre), pilule pour la navigation et les badges.
- Ombre "objet posé sur la table" : quatre couches très transparentes plutôt qu'une ombre forte.

## Composants

- **Navigation** : pilule flottante en haut, floutée, qui se resserre au défilement. La page en cours est en encre pleine. À droite, toujours visibles : le lien vers le dépôt GitHub (icône seule sur téléphone) et le bouton clair ou sombre. Sur téléphone, les liens de pages défilent à l'horizontale.
- **Boutons** : plein encre, plein ocre pour l'appel final, ou lien texte suivi d'un chevron ocre. Tous rétrécissent un peu au clic.
- **Cartes** : fond carte, bordure fine, badge mono en haut, titre serif, texte gris.
- **Listes numérotées** : numéro mono ocre 01, 02, lignes pointillées.
- **Frise** : ligne verticale avec un point par étape. Les portes humaines ont un point plein. Une barre ocre se remplit quand la frise entre à l'écran.
- **Pile de cartes** (accueil) : quatre cartes empilées qui tournent toutes les 4,5 secondes, en pause au survol.
- **Chiffres** : gros chiffres serif ocre qui comptent jusqu'à leur valeur.

## Animations

Tout est dans `assets/site.js` (aucune bibliothèque) et `assets/style.css`.

- `.apparait` : opacité 0 vers 1, flou 4px vers 0, montée de 20px. Durée 0.8s, courbe `cubic-bezier(.22, 1, .36, 1)`.
- `.masque` : le titre monte depuis sous une ligne invisible, avec un léger flou. Durée 0.9s.
- `data-decale="0.08"` sur un parent : décale l'apparition de ses enfants (0.04 à 0.1s).
- Déclenchement à l'entrée dans l'écran, une seule fois.
- Le mot en italique du h1 change très lentement de teinte (8 secondes).
- `prefers-reduced-motion: reduce` : ni flou, ni déplacement, ni rotation de la pile.
- Sans JavaScript, tout reste visible : le masquage n'existe que si la classe `js` est posée.

## À ne pas faire

- Pas de rebond, pas de deuxième couleur d'accent, pas de dégradé vif.
- Pas d'animation qui se rejoue à chaque passage.
- Pas de flou au-delà de 4 à 6px.
- Pas de tiret long ni de guillemets typographiques dans les textes.
- Aucun nom, domaine, serveur ou valeur propre à une instance : la liste noire bloque le commit.

## Ajouter une page

1. Copier une page existante, garder la navigation et le pied de page.
2. Ajouter le lien dans la navigation et le pied de page des six autres pages.
3. Un seul bloc `.sombre`, des titres en `.masque`, les blocs en `.apparait`.
4. Contrôler : `bash scripts/liste-noire.sh --tout site`, puis la page en largeur téléphone (375px, aucun défilement horizontal).
