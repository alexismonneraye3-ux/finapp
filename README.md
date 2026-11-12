# Socle de l'appli d'information financière

Première brique réelle du produit : une base de faits où chaque chiffre porte
sa source et la date à laquelle il a été connu, des calculs faits par du code
testé, et la « mémoire des promesses » (prévisions de la direction comparées
aux résultats publiés).

Aucune dépendance à installer : Python 3.10 ou plus récent suffit.

## Démarrer

```
python3 -m finapp seed          # charge l'exemple Nvidia
python3 -m finapp serve         # ouvre l'appli sur http://127.0.0.1:8000
python3 -m unittest discover tests
```

Autres commandes :

```
python3 -m finapp show NVDA --as-of 2026-06-01    # la fiche telle que connue à cette date
python3 -m finapp export-demo                     # écrit dist/demo.html, page autonome
python3 -m finapp ingest-sec --cik 1045810 --ticker NVDA --user-agent "MonAppli contact@exemple.com"
```

## Ce que contient le code

| Fichier | Rôle |
| --- | --- |
| `finapp/db.py` | Schéma SQLite : sociétés, sources, faits, promesses |
| `finapp/facts.py` | Écriture et lecture des faits, lecture « tel que connu à une date » |
| `finapp/sec.py` | Collecte et lecture des comptes au format SEC companyfacts |
| `finapp/calc.py` | Variations, marges, écarts : chaque résultat garde sa formule et ses entrées |
| `finapp/promises.py` | Verdict de chaque prévision, habitude de l'entreprise, ruptures d'habitude |
| `finapp/views.py` | Assemble la fiche d'une société : chiffre d'affaires par trimestre et par exercice, marges par trimestre, promesses |
| `finapp/api.py` | API JSON (`/api/companies`, `/api/company/<ticker>?as_of=AAAA-MM-JJ`) et service de l'écran |
| `web/index.html` | Écran unique, modes Essentiel et Pro, téléphone et ordinateur |
| `fixtures/` | Jeu d'exemple Nvidia |
| `tests/` | 55 tests automatiques |

## Les trois règles du socle

1. **Un chiffre ne voyage jamais sans sa source.** Toute valeur renvoyée par
   l'API contient l'adresse du document d'origine et sa date de publication.
2. **On ne remplace jamais, on ajoute.** Un chiffre révisé devient une nouvelle
   version ; l'ancienne reste, ce qui permet d'afficher ce qui était connu à
   n'importe quelle date passée.
3. **Les calculs sont faits par du code.** L'IA, quand elle sera branchée,
   lira ces résultats et les expliquera ; elle ne produira aucun nombre.

## Limites actuelles

- **Marges vides dans l'exemple.** Le mode Pro affiche la marge brute, la
  marge opérationnelle et la marge nette par trimestre. Le jeu d'exemple
  Nvidia ne contient que le chiffre d'affaires : ces colonnes y affichent
  donc « non disponible » tant que des comptes complets ne sont pas chargés.
- **Données d'exemple.** Les chiffres Nvidia fournis sont ceux des communiqués,
  arrondis, avec des dates de période et de dépôt approximatives. La prévision
  du T4 exercice 2026 est reconstituée à partir d'un article. L'écran les
  signale comme telles.
- **Chiffre d'affaires annuel vide dans l'exemple.** Le mode Pro affiche le
  chiffre d'affaires par exercice et sa variation sur un an. Le jeu d'exemple
  Nvidia ne contient que des trimestres : ce tableau y est donc vide.
- **Collecte SEC à fiabiliser.** Le lecteur a été essayé à la main sur un
  vrai fichier de la SEC : les chiffres annuels obtenus sont justes, mais la
  date « connu depuis » est celle du dernier rapport qui rappelle le chiffre,
  pas celle de sa première publication, et les libellés de trimestre peuvent
  être faux (tâches 3.14 et 3.15). La commande `ingest-sec` elle-même reste
  à durcir (tâche 3.1).
- **Pas encore d'IA.** La barre de question n'existe pas ; il faut une clé
  d'accès à un modèle de langage.
- **Pas de cours de bourse ni de temps réel.** Seuls les comptes publiés sont
  gérés.
- **Les prévisions sont saisies à la main.** Leur extraction automatique des
  communiqués reste à écrire.
- **Pas de comptes utilisateurs, pas de portefeuille, pas d'alertes.**
- **Serveur de développement.** Il convient pour essayer en local, pas pour
  une mise en ligne.

## Étapes suivantes proposées

1. Lancer `ingest-sec` sur une machine connectée et contrôler les chiffres
   obtenus contre les documents d'origine.
2. Extraire les prévisions des communiqués pour une centaine de sociétés.
3. Brancher un modèle de langage qui ne répond qu'à partir de la fiche
   produite par `views.py`, avec un jeu de questions à réponse connue.
4. Ajouter les cours différés, puis le portefeuille et les alertes.
