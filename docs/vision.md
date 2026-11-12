# Vision du produit

Ce document est la référence. En cas de doute sur ce qu'il faut construire,
c'est lui qui tranche, puis les fichiers de `docs/specifications/`.
Les études qui le justifient sont dans `docs/analyse-de-marche.md` et
`docs/plan-de-creation.md`.

## La promesse

**La plus précise des applis d'information financière accessibles à tous.**

- Gratuite et sans limite pour les particuliers.
- Une IA qui répond à toute question financière et montre la source de
  chaque chiffre.
- Deux interfaces sur les mêmes données : Essentiel (débutants) et Pro
  (investisseurs avancés et traders).
- Des informations nouvelles, obtenues en reliant des données que personne
  ne relie.
- Pour le monde entier, dans toutes les langues.

Le message en une phrase : « La réponse juste, avec la preuve. »

## Ce que l'appli n'est pas

- Pas un courtier : aucun passage d'ordres.
- Pas un conseiller : jamais « achète » ni « vends », jamais de
  recommandation personnalisée.
- Pas un média financé par la publicité, pas d'incitation à trader.
- Pas un concurrent de Bloomberg sur la milliseconde : on vise la seconde
  pour les cours et quelques secondes pour les nouvelles.

## Les règles qui ne se négocient pas

1. **Un chiffre ne voyage jamais sans sa source** : adresse du document,
   date de publication, date à laquelle nous l'avons connu.
2. **On ne remplace jamais, on ajoute** : une révision crée une nouvelle
   version. On peut toujours afficher ce qui était connu à une date passée.
3. **Aucun nombre ne sort de l'IA** : tout nombre vient de la base de faits
   ou d'un calcul fait par du code testé, avec sa formule et ses entrées.
4. **Toute information affiche son âge** : une donnée en retard est
   signalée, jamais présentée comme actuelle.
5. **L'appli dit quand elle ne sait pas** : pas de donnée, pas de réponse
   inventée.
6. **Les erreurs sont mesurées et publiées.**
7. **Information, pas conseil** : chaque écran le rappelle ; chaque lien
   rémunéré est affiché comme tel.
8. **Les données d'exemple sont toujours marquées comme telles.**

## Pour qui

| Profil | Ce qu'il veut | Ce que l'appli lui donne |
| --- | --- | --- |
| Débutant | Comprendre avant d'agir | Mode Essentiel : peu de chiffres, des phrases claires, chaque mot technique expliqué au toucher |
| Investisseur avancé | Fondamentaux fiables, comparaisons, monde entier | Mode Pro : comptes complets, ratios, comparables, historique « tel que connu » |
| Trader actif | Le signal sans le bruit | Alertes combinées, différentiel du matin, ondes de choc |
| Professionnel | Tout tracer jusqu'au document | Source et calcul derrière chaque chiffre, export, piste d'audit (offre Équipes) |

Le pont entre les modes : mêmes données, même portefeuille ; tout élément
du mode Essentiel s'ouvre en version Pro.

## Ce que l'appli crée de nouveau

| Création | En une phrase | Version |
| --- | --- | --- |
| Mémoire des promesses | Chaque engagement chiffré d'un dirigeant, vérifié trimestre après trimestre | 1 |
| Grands investisseurs | Les portefeuilles et mouvements des meilleurs, avec l'âge de l'information et le pourquoi probable | 1 |
| Thèse vivante | L'utilisateur écrit pourquoi il détient un titre ; l'appli suit si les conditions tiennent | 1 simple, 2 complète |
| Ondes de choc | Un événement arrive : qui est touché ensuite, et est-ce dans mon portefeuille | 2 |
| Écart récit-réalité | La divergence entre ce que dit la direction, ce que disent les médias et ce que montrent les faits | 2 |
| Jumeaux historiques | Les situations passées les plus ressemblantes et ce qui a suivi | 2 |
| Avance par la langue | Ce qui est publié en japonais, coréen, chinois ou allemand et pas encore repris en anglais | 3 |
| Indice d'attention mondial | Ce que chaque pays regarde, anonyme et agrégé | 3 |
| Miroir de l'investisseur | Les biais récurrents de chacun, à partir de son journal | 3 |
| Bulletin de notes de l'IA | La fiabilité de notre IA, mesurée et publiée | 1 |

Réserve : ces indicateurs sont des estimations, pas des prédictions. Ils
s'affichent avec leur méthode, leur historique et leurs limites. Un score
sur une entreprise peut être traité comme une recommandation selon les
pays : validation juridique avant toute mise en ligne publique.

## Les trois versions

| | Version 1 | Version 2 | Version 3 |
| --- | --- | --- | --- |
| Marchés | Actions et ETF américains, cryptos | Europe puis Asie, un marché à la fois | Monde |
| Données | Comptes officiels, cours différés, cryptos en direct | Temps réel pour l'offre Équipes | Données alternatives |
| IA | Questions-réponses sourcées, brief du jour | Thèse vivante complète, contradicteur, scénarios | Agents, accès pour IA externes |
| Écrans | Les huit écrans de base | Screener, graphiques avancés, espaces d'équipe | Pages des sociétés, place de marché |
| Langues | IA dans toutes les langues, interface français et anglais | Six langues de plus | Lecture des sources en langue locale |
| Revenus | Partenariats courtiers | Offre Équipes par poste | Licences de données, API commerciale |

## Les huit écrans de la version 1

1. Accueil : brief du jour et barre de question.
2. Réponse de l'IA : texte, chiffres cliquables jusqu'à la source, graphique.
3. Fiche d'un actif, modes Essentiel et Pro.
4. Portefeuille et liste de suivi.
5. Mémoire des promesses.
6. Grands investisseurs.
7. Alertes.
8. Compte et réglages : mode, langue.

## Monétisation

1. **Partenariats courtiers** dès le lancement : commission par compte
   ouvert, lien affiché comme rémunéré. Courtiers en produits à effet de
   levier exclus.
2. **Offre Équipes** : abonnement par poste pour conseillers, petits fonds
   et cabinets. Ils paient le partage, la piste d'audit, la conformité,
   l'administration et le temps réel ; jamais les fonctions d'analyse, qui
   restent gratuites pour les particuliers.
3. **Données et API** quand l'audience est là : licences sur nos
   indicateurs, API payante pour les usages commerciaux.

Jamais : publicité, vente de données personnelles, incitation à trader.

## Où en est le code

Le socle existe : base de faits datés, calculs, mémoire des promesses,
API, écran Essentiel/Pro, tests. Voir `README.md`. La suite est dans
`TACHES.md`, phase par phase.

## Ce que le code seul ne peut pas faire

Ces points dépendent du propriétaire, pas de l'agent. Ils sont listés dans
`TACHES.md`, section « Décisions du propriétaire ».

- Clé d'accès à un modèle de langage (pour l'IA).
- Contrat avec un fournisseur de cours (droits d'affichage).
- Avis d'un avocat en droit financier avant le lancement public.
- Hébergement, nom de domaine, nom et marque de l'appli.
- Publication sur les boutiques d'applis.
