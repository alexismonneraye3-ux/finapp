# 07 — Portefeuille, alertes, brief du jour, cours

## 1. Cours

- Table des cours journaliers : actif, date, ouverture, plus haut, plus
  bas, clôture, volume, fournisseur, `known_at`, indication « différé ».
- Opérations sur titres (divisions, dividendes) stockées à part ; les
  cours ajustés sont calculés, jamais stockés à la place des cours bruts.
- L'accès au fournisseur passe par une interface unique
  (`finapp/prices.py`) avec un faux fournisseur pour les tests et un import
  CSV. Le vrai fournisseur sera branché quand le propriétaire aura choisi
  un contrat avec droits d'affichage.
- Tout cours affiché porte son heure et la mention « différé de 15
  minutes » quand c'est le cas.
- Cryptomonnaies : même table, cotation continue, pas de jours fériés.
- Calendrier des séances : jours ouvrés et jours fériés par bourse.

## 2. Portefeuille

**Données.** Portefeuille (nom, devise), lignes (actif, quantité, prix de
revient, date), opérations (achat, vente, dividende). Listes de suivi
nommées.

**Entrée.** À la main ou import CSV (modèle fourni, erreurs expliquées
ligne par ligne). Pas de connexion à un courtier en version 1.

**Calculs.** Valeur, poids, plus-value latente, répartition par secteur,
pays et devise, concentration (poids des trois premières lignes),
corrélations entre lignes, volatilité, performance comparée à un indice.

**Lecture en mode Essentiel.** Une phrase par constat, produite par des
règles écrites : « Ta première ligne pèse 42 % du portefeuille. » Aucun
conseil d'arbitrage.

**Vie privée.** Sans compte, le portefeuille reste dans le navigateur.
Avec compte, il est stocké chiffré et exportable ou supprimable à tout
moment.

## 3. Alertes

**Modèle.** Une alerte = une cible (titre, liste, portefeuille,
investisseur) + une ou plusieurs conditions reliées par ET / OU + un canal.

| Type de condition | Exemple |
| --- | --- |
| Cours | franchit un seuil, varie de plus de x % sur la séance |
| Volume | supérieur à x fois la moyenne de 20 séances |
| Publication | nouveau dépôt, nouveaux résultats, date de résultats annoncée |
| Comptes | un indicateur passe un seuil (marge brute sous 60 %) |
| Promesse | nouvelle prévision, verdict rendu, rupture d'habitude |
| Thèse | une condition change d'état |
| Grand investisseur | nouveau dépôt, achat ou vente d'un titre suivi |
| Dirigeants | achat ou vente d'un dirigeant, achats groupés |
| Qualité | une donnée de mes titres a été corrigée |

**Règles.**

- Une alerte se déclenche une fois par franchissement, pas à chaque
  passage du moteur ; un délai de repos évite les rafales.
- Chaque déclenchement garde le fait qui l'a causé, avec sa source.
- Mode Essentiel : un seul réglage, « préviens-moi si quelque chose
  d'important arrive sur mes titres », qui active un jeu d'alertes par
  défaut (résultats, verdict de promesse, mouvement d'un grand
  investisseur, variation de plus de 5 % sur la séance).
- Mode Pro : composition libre des conditions ; plus tard, création en
  langage naturel par l'IA, qui montre la règle obtenue avant de
  l'enregistrer.
- Canaux : centre de notifications dans l'appli d'abord ; courriel et
  notifications du téléphone quand l'hébergement existera.
- Historique des déclenchements consultable.

## 4. Brief du jour

**Idée.** Ce qui a changé depuis hier pour les titres de l'utilisateur,
plutôt qu'un fil à relire.

**Construction, par du code.**

1. Lister tout ce qui est nouveau depuis le dernier brief : faits,
   dépôts, verdicts de promesse, mouvements de grands investisseurs,
   opérations de dirigeants, changements d'état d'une thèse, corrections
   de données, variations de cours notables.
2. Garder ce qui concerne le portefeuille et les listes de suivi.
3. Classer par importance selon des règles écrites et testées (résultats
   publiés avant un simple dépôt administratif, ligne lourde avant ligne
   légère).
4. Mode Essentiel : les trois premiers éléments, une phrase chacun. Mode
   Pro : la liste complète, groupée par titre.
5. Chaque élément renvoie à sa source.

L'IA pourra ensuite rédiger l'introduction du brief à partir de cette
liste, sans y ajouter de nombre.

**Sans portefeuille.** Brief général sur les sociétés les plus suivies.

**Historique.** Les briefs passés restent consultables : c'est aussi la
preuve de ce que l'appli savait chaque jour.

## 5. Calendrier

Dates de résultats (annoncées par les sociétés, avec source), dates
limites de dépôt des 13F, puis indicateurs économiques en version 2.

## 6. Recherche

Recherche d'une société par nom ou symbole, tolérante aux accents, à la
casse et aux fautes légères ; résultats classés ; accessible depuis tous
les écrans.
