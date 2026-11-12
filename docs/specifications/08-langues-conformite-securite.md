# 08 — Langues, conformité, comptes, sécurité, mise en ligne

Ce qui touche au droit dans ce fichier est une base de travail à faire
valider par un avocat en droit financier. Il n'a pas valeur d'avis
juridique.

## 1. Langues

- Tous les textes de l'interface sont dans des dictionnaires, un par
  langue, avec les mêmes clés. Un test vérifie qu'aucune clé ne manque.
- Version 1 : français (par défaut) et anglais. Version 2 : espagnol,
  allemand, portugais, italien, japonais, chinois simplifié. Ensuite :
  coréen, arabe, hindi et les autres.
- Formats par langue : nombres, dates, devises, pluriels.
- Écriture de droite à gauche prévue dans la mise en page.
- Les phrases du mode Essentiel sont des modèles par langue, pas des
  traductions mot à mot.
- Le lexique (définitions des termes) existe dans chaque langue, en deux
  niveaux : débutant et avancé.
- Les documents d'origine restent dans leur langue ; l'appli affiche le
  passage d'origine à côté de sa traduction.
- L'IA répond dans la langue de la question.

## 2. Information, pas conseil

- Aucune recommandation personnalisée d'acheter, vendre ou conserver.
- Pas d'objectif de cours, pas de note d'achat ou de vente.
- Les classements et indicateurs sont présentés comme des constats, avec
  leur méthode publiée.
- Mention visible sur chaque écran : « Information, pas conseil en
  investissement. »
- Page « Méthode et sources » : d'où viennent les données, comment chaque
  indicateur est calculé, quelles sont les limites.
- Page « Comment nous gagnons de l'argent » : chaque lien rémunéré est
  marqué « partenaire rémunéré » là où il apparaît.
- Journal des réponses de l'IA conservé pour pouvoir justifier ce qui a
  été affiché.
- Liste de formulations interdites, testée automatiquement.

## 3. Données personnelles

- Le moins de données possible. L'appli fonctionne sans compte.
- Portefeuilles et questions sont des données sensibles : stockage
  chiffré, jamais vendus, jamais utilisés pour de la publicité.
- Export et suppression de ses données en un geste.
- Consentement explicite et séparé pour toute statistique d'usage ;
  l'indice d'attention n'utilise que des données agrégées.
- Hébergement dans l'Union européenne.
- Registre des traitements tenu dans `docs/`.

## 4. Comptes

- Création par adresse électronique et lien de connexion, sans mot de
  passe en version 1 ; double facteur ensuite.
- Sessions à durée limitée, déconnexion de tous les appareils.
- Rôles : particulier ; pour l'offre Équipes : membre, administrateur.
- Offre Équipes : espaces partagés, listes et thèses communes, piste
  d'audit (qui a vu et exporté quoi), administration des postes,
  facturation.

## 5. Sécurité

- Entrées toujours validées ; requêtes SQL toujours paramétrées.
- Aucune clé ni secret dans le dépôt ; lecture dans des variables
  d'environnement.
- En-têtes de sécurité sur toutes les réponses ; politique de contenu
  stricte ; aucun script externe.
- Limite de débit par adresse sur l'API.
- Journal des accès sans donnée personnelle inutile.
- Sauvegardes testées.
- Test d'intrusion par un prestataire avant le lancement public.

## 6. Fiabilité

- Objectif : disponible pendant les heures de marché, y compris les jours
  agités, qui sont le premier reproche fait aux applis concurrentes.
- Chaque brique critique a un second fournisseur ; la bascule est testée.
- Page d'état publique : fraîcheur de chaque source, incidents.
- Supervision : retard de collecte, erreurs, temps de réponse.

## 7. Mise en ligne

Le serveur actuel sert au développement. Pour une mise en ligne :

- Base de données de production (PostgreSQL), en gardant le même schéma
  et les mêmes règles ; SQLite reste pour les tests.
- Serveur d'application derrière un répartiteur, en HTTPS.
- Tâches de collecte séparées du service web.
- Environnements : développement, recette, production.
- Tests lancés automatiquement à chaque proposition de modification.
- Applis téléphone : d'abord l'appli web installable sur l'écran
  d'accueil ; applis natives ensuite, à partir du même code d'interface
  autant que possible.

Ces choix d'hébergement demandent une décision et un budget du
propriétaire avant d'être exécutés.

## 8. Mesures de pilotage

| Famille | Mesure |
| --- | --- |
| Précision | taux d'erreur sur le jeu de questions ; part des réponses entièrement sourcées ; délai entre publication et présence dans l'appli |
| Fiabilité | disponibilité aux heures de marché ; temps de réponse |
| Usage | utilisateurs actifs par semaine ; retour après quatre semaines ; questions par utilisateur |
| Confiance | erreurs signalées ; délai de correction |
| Coûts | coût par question ; coût des données par utilisateur |
| Revenus | comptes ouverts chez les partenaires ; entreprises clientes ; revenu récurrent |

## 9. Définition de « terminé » pour une tâche

1. Le comportement décrit existe, dans les deux modes s'il touche l'écran.
2. Les tests passent et couvrent le cas normal et les cas limites.
3. Chaque nombre nouveau ouvre sa source.
4. Les textes passent par le dictionnaire de langues.
5. L'écran tient sur un téléphone de 320 px sans défilement horizontal.
6. `README.md` est à jour si une commande ou un fichier change.
7. La description de la proposition dit, en français simple, ce qui change
   pour l'utilisateur et comment le vérifier.
