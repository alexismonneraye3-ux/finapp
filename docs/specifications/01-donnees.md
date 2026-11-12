# 01 — Données : base de faits, sources, collecte, fraîcheur

L'exactitude vient des données, pas de l'IA. Ce fichier décrit ce que la
base doit contenir et comment elle se remplit.

## 1. Principes

- Tout ce qui est stocké a une **source** (adresse, type, titre, date de
  publication) et une **date de connaissance** `known_at`.
- Rien n'est modifié ni supprimé. Une correction est une nouvelle ligne
  avec un `known_at` plus récent.
- Toute lecture accepte une date `as_of` et renvoie ce qui était connu à
  cette date. Sans `as_of` : la dernière version connue.
- Les heures sont en UTC, au format ISO 8601. Une date seule (`AAAA-MM-JJ`)
  reste acceptée et vaut le début de la journée UTC.
- Les montants gardent leur unité et leur devise d'origine. Aucune
  conversion silencieuse.
- Les données d'exemple portent `is_sample = 1` et le restent jusqu'à
  l'écran.

## 2. Ce que la base doit savoir stocker

| Objet | Contenu | État |
| --- | --- | --- |
| Société | symbole, nom, identifiant du régulateur (CIK), bourse, pays, devise, secteur, date de fin d'exercice | partiel |
| Source | type, adresse, titre, date de publication, langue | fait (sans langue) |
| Fait comptable | indicateur, période, valeur, unité, source, `known_at` | fait |
| Promesse | indicateur, période visée, fourchette, source, date d'annonce | fait |
| Cours | actif, date ou heure, ouverture, plus haut, plus bas, clôture, volume, fournisseur, `known_at`, différé ou non | à faire |
| Opération sur titre | division d'actions, dividende, date d'effet | à faire |
| Position d'un grand investisseur | déclarant, titre, quantité, valeur, trimestre, source, `known_at` | à faire |
| Opération de dirigeant | personne, fonction, titre, sens, quantité, prix, date de l'opération, date du dépôt | à faire |
| Événement | type, date, sociétés concernées, source, résumé | à faire |
| Lien entre entités | origine, cible, type (fournisseur, client, concurrent, filiale, matière première, pays), poids, source, validité dans le temps | à faire |
| Actualité | titre, adresse, éditeur, heure, langue, sociétés citées, empreinte de dédoublonnage | à faire |
| Contrôle de qualité | donnée concernée, règle, résultat, date | à faire |

## 3. Indicateurs comptables à couvrir

Chaque indicateur a un nom interne stable. Les étiquettes du régulateur
américain sont essayées dans l'ordre indiqué dans `finapp/sec.py`.

- **Compte de résultat** : `revenue`, `cost_of_revenue`, `gross_profit`,
  `rd_expense`, `sga_expense`, `operating_income`, `interest_expense`,
  `income_tax`, `net_income`, `eps_basic`, `eps_diluted`,
  `shares_diluted`.
- **Bilan** (valeurs à une date) : `cash`, `short_term_investments`,
  `receivables`, `inventory`, `total_current_assets`, `total_assets`,
  `total_current_liabilities`, `long_term_debt`, `short_term_debt`,
  `total_liabilities`, `equity`, `shares_outstanding`.
- **Flux de trésorerie** : `operating_cash_flow`, `capex`,
  `dividends_paid`, `buybacks`, `stock_comp`.

Règles :

- Les trimestres durent 80 à 100 jours, les exercices 350 à 380 jours.
- Les flux de trésorerie américains sont publiés en cumul depuis le début
  de l'exercice : le trimestre isolé se calcule par différence de deux
  cumuls consécutifs, et ce calcul garde sa formule et ses entrées.
- Le quatrième trimestre, rarement publié seul, se calcule : exercice
  moins les trois premiers trimestres. La valeur est marquée « calculée ».
- Si deux étiquettes donnent une valeur pour la même période, on garde la
  première de la liste et on enregistre un contrôle de qualité si l'écart
  dépasse 0,5 %.

## 4. Sources de la version 1

| Donnée | Source | Adresse | Remarques |
| --- | --- | --- | --- |
| Liste des sociétés américaines | Régulateur américain (SEC) | `https://www.sec.gov/files/company_tickers.json` | symbole, CIK, nom |
| Comptes | SEC, API companyfacts | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` | CIK sur 10 chiffres |
| Liste des dépôts d'une société | SEC, API submissions | `https://data.sec.gov/submissions/CIK##########.json` | sert à détecter un nouveau dépôt |
| Communiqués de résultats | SEC, formulaire 8-K et pièce 99.1 | archives EDGAR | source des prévisions de la direction |
| Portefeuilles des gérants | SEC, formulaire 13F-HR | archives EDGAR | dû 45 jours après la fin du trimestre |
| Opérations de dirigeants | SEC, formulaire 4 | archives EDGAR | dû sous 2 jours ouvrés |
| Prises de participation | SEC, formulaires 13D et 13G | archives EDGAR | |
| Cours des actions | fournisseur sous licence, à choisir par le propriétaire | — | différé de 15 minutes en gratuit |
| Cryptomonnaies | flux publics des plateformes | à choisir | temps réel |

Règles d'accès à la SEC : en-tête `User-Agent` avec un nom et une adresse
de contact, au plus 10 requêtes par seconde (on se limite à 5).

## 5. Collecte

- Chaque collecteur est une fonction en deux parties : **aller chercher**
  (réseau) et **lire** (aucun réseau). Seule la lecture est testée, sur des
  fichiers d'exemple rangés dans `fixtures/`.
- Aller chercher : délai maximal de 30 secondes, trois essais avec attente
  croissante sur les erreurs 429 et 5xx, message clair en cas d'échec.
- Relancer une collecte n'ajoute rien si rien n'a changé.
- Un journal de collecte garde : source, heure, nombre de lignes ajoutées,
  erreurs.
- Une file d'attente simple (table SQLite) permet de reprendre après un
  arrêt.

## 6. Fraîcheur visée

| Donnée | Délai visé entre publication et présence dans l'appli |
| --- | --- |
| Cours des actions, offre Équipes | moins d'une seconde |
| Cours des actions, gratuit | différé de 15 minutes, affiché comme tel |
| Cryptomonnaies | temps réel |
| Communiqués et dépôts | une minute |
| Comptes extraits d'un dépôt | quelques minutes |

Chaque donnée affichée porte son âge. Au-delà d'un seuil par type (valeurs
de départ : cours 20 minutes pendant les heures de marché, comptes 100
jours après la fin de période), l'écran affiche « donnée ancienne ».

## 7. Contrôles de qualité

Chaque contrôle écrit une ligne dans la table des contrôles ; aucun ne
corrige une donnée tout seul.

1. Égalité comptable : actif = passif + capitaux propres, à 0,5 % près.
2. Marge brute = chiffre d'affaires − coût des ventes, à 0,5 % près.
3. Somme des quatre trimestres = exercice, à 0,5 % près.
4. Variation de plus de 300 % d'un trimestre à l'autre : à vérifier.
5. Changement d'unité apparent (facteur 1 000 ou 1 000 000) : à vérifier.
6. Quand deux fournisseurs existent : écart supérieur à 0,5 % signalé.
7. Trou dans une série (trimestre manquant) : signalé.

L'écran Pro montre, pour chaque chiffre, si un contrôle l'a signalé.

## 8. Signalement d'erreur

Chaque chiffre a un bouton « signaler une erreur ». Le signalement stocke :
le fait visé, le message, la date. Objectif : traitement sous 24 heures.
Le nombre de signalements et le délai de correction font partie des
mesures publiées.
