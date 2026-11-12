# 05 — Ce que l'appli crée de nouveau

Chaque création relie des données existantes pour produire une
information qui n'est affichée nulle part ailleurs sous cette forme.
Toutes sont des constats ou des estimations, jamais des recommandations.
Chacune affiche sa méthode, ses limites et son historique.

## 1. Mémoire des promesses (version 1)

**Idée.** Relever chaque engagement chiffré de la direction, puis vérifier
s'il a été tenu.

**État.** Faite pour le chiffre d'affaires, saisie à la main.

**À construire.**

- Autres indicateurs : marge brute, marge opérationnelle, bénéfice par
  action, investissements, et prévisions annuelles.
- Types d'engagement : valeur avec fourchette (« 91 milliards ± 2 % »),
  borne (« au moins », « au plus »), sens (« en hausse »). Les
  engagements non chiffrés (« d'ici fin d'année ») sont notés avec une
  échéance et un verdict saisi avec source.
- Révisions : une prévision revue en cours de trimestre est une nouvelle
  version ; on garde l'historique et on évalue la dernière connue avant la
  publication, en affichant qu'elle a été revue.
- Extraction automatique des communiqués de résultats (pièce 99.1 du
  formulaire 8-K) : repérer la section des perspectives, extraire
  indicateur, période, valeur, fourchette. D'abord par règles sur les
  formulations courantes ; l'IA aidera ensuite. Toute extraction garde le
  passage d'origine et un niveau de confiance ; en dessous du seuil, elle
  attend une validation humaine.
- Profil par société : taux tenu, écart moyen, écart type, tendance,
  ruptures d'habitude, prudence (direction qui annonce systématiquement en
  dessous de ce qu'elle réalise).
- Vue marché : sociétés classées par régularité, par secteur.

**Limites à afficher.** Une direction prudente « dépasse » facilement ses
prévisions : le taux tenu ne mesure pas la qualité de l'entreprise. Avec
moins de quatre prévisions évaluées, le profil est marqué « peu de recul ».

## 2. Thèse vivante (version 1 simple, version 2 complète)

**Idée.** L'utilisateur écrit pourquoi il détient un titre ; l'appli suit
si ses raisons tiennent encore.

**Version 1.**

- L'utilisateur crée une thèse sur un titre et y ajoute des conditions
  vérifiables choisies dans une liste : indicateur, comparaison, seuil,
  période. Exemples : « croissance du chiffre d'affaires sur un an
  supérieure à 20 % », « marge brute supérieure à 60 % », « dette nette
  négative », « la direction tient ses prévisions ».
- À chaque nouvelle donnée, chaque condition passe à : tenue, fragile (à
  moins de 10 % du seuil), rompue, non évaluable.
- État de santé de la thèse : nombre de conditions tenues, fragiles,
  rompues. Pas de note unique.
- Historique : quand chaque condition a changé d'état, et à cause de quel
  fait.
- Une alerte part quand une condition change d'état.

**Version 2.** L'utilisateur écrit en texte libre ; l'IA propose le
découpage en conditions, qu'il valide. L'appli relie aussi les actualités
et les passages de documents qui confirment ou contredisent la thèse.

## 3. Ondes de choc (version 2, fondations en version 1)

**Idée.** Un événement touche une société : qui est touché ensuite ?

**Le graphe.**

- Nœuds : sociétés, matières premières, pays, secteurs.
- Liens typés : fournisseur, client, concurrent, filiale, dépendance à une
  matière, exposition à un pays. Chaque lien a un sens, un poids quand il
  est connu (part du chiffre d'affaires), une source et une période de
  validité.
- Sources des liens : clients importants cités dans les rapports annuels,
  répartition géographique des ventes, listes de fournisseurs publiées.
  Aucun lien sans source.

**La propagation.**

- Entrée : un événement (société, type, sens).
- Sortie : les entités à un et deux liens de distance, le chemin, le sens
  probable de l'effet, la source de chaque lien, et la présence ou non
  dans le portefeuille de l'utilisateur.
- L'effet n'est pas chiffré tant qu'une méthode validée n'existe pas : on
  montre le lien et sa force connue, pas une variation de cours.

**Écran.** Essentiel : « cette nouvelle touche aussi ces trois sociétés,
dont une que tu détiens ». Pro : carte des liens, filtres par type, poids,
chemins.

## 4. Écart récit-réalité (version 2)

Comparer trois choses sur une même période : ce que dit la direction
(ton et prévisions), ce que disent les médias, ce que montrent les faits
(comptes, embauches, achats de dirigeants). L'appli affiche les trois côte
à côte et signale les désaccords. Pas de score unique en première
version : un tableau des désaccords, chacun avec ses sources.

## 5. Jumeaux historiques (version 2)

Pour une situation décrite par des critères mesurables (par exemple
« croissance supérieure à 50 % et marge en baisse »), retrouver les cas
passés qui y ressemblent, dans les données telles qu'elles étaient connues
à l'époque, et montrer ce qui a suivi : fréquences, médiane, étendue,
nombre de cas. Moins de 20 cas : affiché comme « trop peu de cas pour
conclure ». Toujours avec la mention que le passé ne prédit pas l'avenir.

## 6. Bulletin de notes de l'IA (version 1)

Page publique : résultats mensuels du jeu de questions, nombre d'erreurs
signalées par les utilisateurs, délai moyen de correction, liste des
corrections. Voir `04-ia.md`.

## 7. Version 3

- **Avance par la langue** : informations publiées dans une langue locale
  et pas encore reprises en anglais, avec le passage d'origine.
- **Indice d'attention mondial** : ce que chaque pays regarde. Demande un
  accord explicite, des données agrégées, un seuil minimal d'utilisateurs
  par groupe pour qu'aucune personne ne soit identifiable.
- **Miroir de l'investisseur** : journal de décisions, puis constats sur
  les habitudes (vendre tôt, acheter après une hausse). Visible par
  l'utilisateur seul.

## 8. Ordre de construction

1. Mémoire des promesses étendue.
2. Thèse vivante simple.
3. Bulletin de notes.
4. Graphe de liens, puis ondes de choc.
5. Le reste, version par version.
