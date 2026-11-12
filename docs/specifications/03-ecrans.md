# 03 — Écrans et règles d'interface

## 1. Règles communes à tous les écrans

- Un seul fichier `web/index.html`, JavaScript ES5, aucune bibliothèque.
- Téléphone d'abord (largeur 320 px minimum), puis ordinateur. Aucun
  défilement horizontal de la page ; un tableau large défile dans son
  propre cadre.
- Zones tactiles d'au moins 44 px. Contraste du texte d'au moins 4,5 pour
  1. Tout se fait aussi au clavier. Thème clair et thème sombre.
- **Chaque nombre est un bouton** qui ouvre sa fiche source : valeur
  exacte, unité, période, document d'origine (lien), date de publication,
  date de connaissance, formule et entrées s'il est calculé, contrôles de
  qualité, bouton « signaler une erreur ».
- Chaque écran affiche l'âge des données et, s'il y en a, le bandeau
  « données d'exemple ».
- Chaque écran porte la mention « Information, pas conseil en
  investissement ».
- Un sélecteur « Vu à la date du » permet de remonter le temps partout où
  cela a un sens.
- Bascule Essentiel / Pro visible en permanence ; le choix est mémorisé.
- Tout mot technique du mode Essentiel s'explique au toucher (lexique).
- États à prévoir pour chaque bloc : chargement, vide, erreur, donnée
  ancienne.
- Aucun texte en dur dans le code de l'écran : tout passe par le
  dictionnaire de langues.
- Formats selon la langue : séparateur décimal, date, devise.

## 2. Navigation

Barre du bas sur téléphone, barre latérale sur ordinateur :
Accueil · Recherche · Portefeuille · Investisseurs · Alertes · Compte.
L'adresse de la page reflète l'écran affiché (`#/societe/NVDA`), pour
pouvoir partager un lien et revenir en arrière.

## 3. Les huit écrans

### 3.1 Accueil

| Bloc | Essentiel | Pro |
| --- | --- | --- |
| Barre de question | toujours en haut | idem, avec historique des questions |
| Brief du jour | trois faits qui touchent ses titres, en phrases | différentiel complet depuis hier, par position |
| Marchés | grands indices en une ligne | indices, taux, devises, matières premières, cryptos |
| À venir | prochains résultats de ses titres | calendrier des résultats et des chiffres économiques |

Sans portefeuille : le brief porte sur les sociétés les plus suivies et
invite à ajouter des titres.

### 3.2 Réponse de l'IA

- Réponse en texte, chaque nombre cliquable jusqu'à sa source.
- Tableau ou graphique quand la question s'y prête.
- Liste des sources en bas, avec l'heure des données.
- Mention claire quand l'IA ne sait pas ou quand les sources divergent.
- Boutons : partager (lien avec sources), signaler une erreur, « voir en
  mode Pro ».
- Tant que l'IA n'est pas branchée : la barre répond aux questions que le
  code sait traiter seul (voir `04-ia.md`, section « sans modèle »).

### 3.3 Fiche d'un actif

| Bloc | Essentiel | Pro |
| --- | --- | --- |
| En-tête | nom, ce que fait l'entreprise en une phrase, cours et âge du cours | idem plus bourse, secteur, capitalisation, prochaine publication |
| Santé | cinq indicateurs expliqués : croissance, rentabilité, dette, trésorerie, promesses tenues | tous les ratios de `02-calculs.md`, sur 5 ans |
| Comptes | chiffre d'affaires et bénéfice, en courbe simple | compte de résultat, bilan, flux, par trimestre et par exercice, export CSV |
| Promesses | phrase de synthèse et dernier verdict | tableau complet, fourchettes, écarts, ruptures |
| Qui détient | « X grands investisseurs en détiennent » | détenteurs, mouvements du trimestre, opérations de dirigeants |
| Événements | dates clés marquées sur la courbe | liste des dépôts et communiqués avec liens |
| Comparaison | — | jusqu'à cinq sociétés côte à côte |

### 3.4 Portefeuille et liste de suivi

- Ajout à la main (symbole, quantité, prix de revient, date) ou import
  CSV. Aucune connexion à un courtier en version 1.
- Essentiel : valeur, répartition, plus gros poids, risque principal en une
  phrase.
- Pro : poids, plus-values, répartition par secteur, pays et devise,
  concentration, corrélations, performance comparée à un indice.
- Plusieurs listes de suivi nommées.
- Sans compte, tout reste dans le navigateur.

### 3.5 Mémoire des promesses

- Par société : chaque prévision, sa source, sa fourchette, le résultat,
  le verdict, l'écart.
- Profil : taux de promesses tenues, écart moyen, ruptures d'habitude.
- Une prévision reconstituée à partir d'une source indirecte est marquée
  « déduite ».
- Vue d'ensemble : classement des sociétés par régularité, présenté comme
  un constat et pas comme une recommandation.

### 3.6 Grands investisseurs

Voir `06-grands-investisseurs.md`.

### 3.7 Alertes

Voir `07-portefeuille-alertes-brief.md`.

### 3.8 Compte et réglages

Mode par défaut, langue, thème, devise d'affichage, notifications, export
et suppression de ses données, sources et méthode, mentions légales.

## 4. Graphiques

Tracés en SVG par du code maison, sans bibliothèque.

- Courbe simple, barres, barres groupées.
- Axes lisibles, valeurs au toucher, événements marqués.
- Chaque point renvoie au fait qu'il représente.
- Un graphique a toujours un tableau équivalent accessible.
- Les graphiques avancés de trading sont hors version 1.

## 5. Partage et pages publiques

- Toute fiche et toute réponse a une adresse partageable, lisible sans
  compte.
- Une page publique par société : promesses tenues ou non, grands
  investisseurs présents. Titre, description et données structurées
  pensés pour les moteurs de recherche.
- Version imprimable.
