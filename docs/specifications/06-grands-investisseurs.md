# 06 — Suivre les grands investisseurs

Référence du genre : Dataroma, qui suit environ 80 gérants américains à
partir de leurs déclarations trimestrielles. Notre version ajoute l'âge de
l'information, tous les signaux réunis, le recoupement entre gérants et
l'explication.

## 1. Sources

| Signal | Document | Délai légal | Ce qu'on y lit |
| --- | --- | --- | --- |
| Portefeuille d'un gérant | formulaire 13F-HR | 45 jours après la fin du trimestre | titres cotés aux États-Unis détenus à l'achat : émetteur, identifiant CUSIP, nombre de titres, valeur |
| Opération d'un dirigeant | formulaire 4 | 2 jours ouvrés | personne, fonction, achat ou vente, quantité, prix, date |
| Prise de participation de plus de 5 % | formulaires 13D (actif) et 13G (passif) | variable | détenteur, part du capital, intention |
| Lettres aux actionnaires | sites des gérants | — | le raisonnement, à citer avec lien |

Les transactions des élus et les déclarations des autres pays viennent
après la version 1.

## 2. Limites à afficher partout

- Une position 13F a entre 45 et 135 jours quand on la découvre ; le
  gérant a pu vendre depuis.
- On ne voit que les achats de titres cotés aux États-Unis : ni ventes à
  découvert, ni liquidités, ni obligations, ni actions étrangères.
- Les options apparaissent à part et ne doivent pas être confondues avec
  des actions.
- Ce sont des idées à étudier, pas des ordres à reproduire.

## 3. Données

- **Investisseur** : nom, société de gestion, CIK, style (valeur,
  croissance, activiste), courte présentation avec source.
- **Position** : investisseur, titre, trimestre, quantité, valeur
  déclarée, type (action, option d'achat, option de vente), source,
  `known_at` = date du dépôt.
- **Correspondance CUSIP → symbole** : table tenue à part, avec source ;
  un CUSIP inconnu reste affiché sous le nom de l'émetteur.
- Une déclaration corrigée (13F-HR/A) est une nouvelle version.
- Particularités à gérer : valeur déclarée en milliers de dollars avant
  2023 et en dollars depuis ; plusieurs lignes pour un même titre à
  additionner ; divisions d'actions entre deux trimestres.

## 4. Calculs

| Indicateur | Formule |
| --- | --- |
| Poids d'une ligne | valeur de la ligne ÷ valeur totale déclarée |
| Mouvement du trimestre | nouvelle, renforcée, allégée, vendue, inchangée, selon la variation du nombre de titres ajustée des divisions |
| Variation en % | (titres T − titres T₋₁) ÷ titres T₋₁ |
| Concentration | poids des dix premières lignes |
| Rotation | part du portefeuille renouvelée d'un trimestre à l'autre |
| Durée de détention | nombre de trimestres consécutifs |
| Prix d'achat estimé | fourchette des cours du trimestre d'achat, présentée comme une estimation |
| Âge de l'information | jours écoulés depuis la fin du trimestre déclaré |
| Consensus | titres achetés ou renforcés par plusieurs investisseurs suivis le même trimestre |
| Détenteurs d'un titre | investisseurs suivis qui le détiennent, avec poids |
| Achats groupés de dirigeants | au moins trois dirigeants acheteurs sur 30 jours |

## 5. Écran

| Bloc | Essentiel | Pro |
| --- | --- | --- |
| Liste des investisseurs | « les portefeuilles des maîtres » : nom, style, trois premières lignes | tableau triable : valeur, concentration, rotation, date du dernier dépôt |
| Fiche d'un investisseur | lignes principales, une phrase par mouvement, âge de l'information en clair | portefeuille complet, historique par trimestre, mouvements, export |
| Sur la fiche d'une société | « X grands investisseurs en détiennent » | détenteurs, mouvements, opérations de dirigeants |
| Consensus | « les titres que plusieurs achètent » | recoupements, filtres par style |
| Test historique (version 2) | — | « si j'avais suivi ce gérant depuis dix ans, délai de publication compris » |

Chaque ligne ouvre sa source : le dépôt d'origine.

## 6. Alertes

Le jour d'un nouveau dépôt d'un investisseur suivi, ou d'un mouvement sur
un titre de sa liste. Voir `07-portefeuille-alertes-brief.md`.

## 7. Le pourquoi (version 2)

L'IA relie un mouvement aux lettres et entretiens publics du gérant, en
citant le passage. Sans passage, elle écrit « raison non publiée » et ne
suppose rien.

## 8. Garde-fous

Pas de copie automatique d'ordres : c'est une activité réglementée. Les
performances passées d'un gérant ne sont jamais présentées comme une
promesse.
