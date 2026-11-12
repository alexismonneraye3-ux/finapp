# 02 — Calculs : catalogue des indicateurs

Tous les nombres dérivés sont produits par `finapp/calc.py` ou un module
voisin. Chaque résultat renvoie : nom, valeur, unité, formule lisible avec
les valeurs utilisées, identifiants des faits d'entrée.

## 1. Règles communes

- Si une entrée manque, le résultat est `None` ; l'écran affiche « non
  disponible » et jamais zéro.
- Division par zéro : `None`.
- Unités ou devises différentes : `None`.
- Dénominateur négatif (capitaux propres négatifs, bénéfice négatif) : le
  ratio est `None` avec la raison « non significatif ».
- Tous les faits d'entrée sont lus à la même date `as_of`.
- Arrondi : seulement à l'affichage. Pourcentages à une décimale, ratios à
  deux décimales, montants en milliers, millions ou milliards avec une
  décimale.
- « Douze derniers mois » = somme des quatre derniers trimestres
  consécutifs ; s'il en manque un, `None`.

## 2. Croissance

| Indicateur | Formule |
| --- | --- |
| Variation d'un trimestre sur l'autre | (T − T₋₁) ÷ \|T₋₁\| × 100 |
| Variation sur un an | (T − T₋₄) ÷ \|T₋₄\| × 100, même trimestre de l'exercice précédent |
| Croissance annuelle moyenne sur n ans | ((fin ÷ début)^(1/n) − 1) × 100, seulement si début et fin sont positifs |

## 3. Rentabilité

| Indicateur | Formule |
| --- | --- |
| Marge brute | marge brute ÷ chiffre d'affaires |
| Marge opérationnelle | résultat opérationnel ÷ chiffre d'affaires |
| Marge nette | résultat net ÷ chiffre d'affaires |
| Rentabilité des capitaux propres | résultat net 12 mois ÷ moyenne des capitaux propres début et fin |
| Rentabilité de l'actif | résultat net 12 mois ÷ moyenne de l'actif total |
| Part de la recherche | dépenses de recherche ÷ chiffre d'affaires |

## 4. Solidité financière

| Indicateur | Formule |
| --- | --- |
| Dette nette | dette court terme + dette long terme − trésorerie − placements court terme |
| Dette nette sur résultat opérationnel 12 mois | dette nette ÷ résultat opérationnel 12 mois |
| Liquidité générale | actif court terme ÷ passif court terme |
| Couverture des intérêts | résultat opérationnel ÷ charge d'intérêts |
| Endettement | total des dettes ÷ capitaux propres |

## 5. Trésorerie

| Indicateur | Formule |
| --- | --- |
| Flux de trésorerie disponible | flux d'exploitation − investissements |
| Marge de trésorerie disponible | flux disponible ÷ chiffre d'affaires |
| Conversion du bénéfice en trésorerie | flux disponible ÷ résultat net |
| Rémunération en actions rapportée au chiffre d'affaires | rémunération en actions ÷ chiffre d'affaires |

## 6. Valorisation (demande un cours)

| Indicateur | Formule |
| --- | --- |
| Capitalisation | cours × nombre d'actions |
| Cours sur bénéfice (PER) | cours ÷ bénéfice par action dilué 12 mois |
| Cours sur chiffre d'affaires | capitalisation ÷ chiffre d'affaires 12 mois |
| Valeur d'entreprise | capitalisation + dette nette |
| Valeur d'entreprise sur résultat opérationnel | valeur d'entreprise ÷ résultat opérationnel 12 mois |
| Rendement du flux disponible | flux disponible 12 mois ÷ capitalisation |
| Rendement du dividende | dividendes 12 mois par action ÷ cours |

Le cours et les comptes n'ont pas la même date : la formule affichée
indique les deux dates.

## 7. Cours et risque (demande un historique de cours)

| Indicateur | Formule |
| --- | --- |
| Performance sur une période | (cours fin ÷ cours début − 1) × 100, cours ajustés des divisions |
| Performance dividendes réinvestis | idem avec dividendes |
| Volatilité annualisée | écart type des variations journalières × √252 |
| Plus forte baisse | plus grand recul entre un sommet et le creux suivant |
| Corrélation entre deux titres | corrélation des variations journalières sur la période commune |
| Bêta | covariance avec l'indice ÷ variance de l'indice |

Minimum 60 séances pour la volatilité, la corrélation et le bêta ; en
dessous, `None`.

## 8. Mémoire des promesses

| Indicateur | Formule |
| --- | --- |
| Écart à la prévision | (réalisé − valeur centrale) ÷ \|valeur centrale\| × 100 |
| Verdict | dépassée si réalisé > haut ; manquée si réalisé < bas ; tenue sinon |
| Taux de promesses tenues | (tenues + dépassées) ÷ évaluées |
| Écart moyen | moyenne des écarts évalués |
| Rupture d'habitude | écart qui s'éloigne d'au moins 3 points de la moyenne des écarts précédents, avec au moins 2 précédents |

## 9. Phrases du mode Essentiel

Chaque calcul a un modèle de phrase, rempli par du code, dans chaque
langue. Exemples :

- Variation : « Le chiffre d'affaires a augmenté de 19,8 % par rapport au
  trimestre précédent. »
- Marge : « Sur 100 $ de ventes, l'entreprise garde 56 $ de bénéfice. »
- Promesse : « La direction avait annoncé environ 91 milliards ; elle a
  fait 96,2 milliards, soit 5,7 % de plus. »

Les phrases ne contiennent aucun jugement (« bon », « inquiétant ») sans
règle écrite ici. Elles décrivent.

## 10. Tests attendus pour chaque calcul

Un cas normal vérifié à la main, un cas avec entrée manquante, un cas de
division par zéro, un cas de valeur négative, un cas d'unités différentes,
et la vérification que la formule et les entrées sont renvoyées.
