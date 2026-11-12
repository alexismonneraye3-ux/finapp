# Liste des tâches

L'agent prend la première tâche non cochée, dans l'ordre, une par passage.
Pour changer les priorités, déplace les lignes. Pour ajouter une tâche,
ajoute une ligne `- [ ] ...`.

Chaque tâche renvoie au fichier de `docs/specifications/` qui la détaille.
La vision d'ensemble est dans `docs/vision.md`. Une tâche est terminée
quand elle respecte la « définition de terminé » de
`docs/specifications/08-langues-conformite-securite.md`, section 9.

Si une tâche est trop grosse pour une seule proposition, l'agent la
découpe : il fait la première partie et ajoute les suivantes juste en
dessous.

## Ordre de passage : jalon 1 d'abord

La stratégie (`docs/strategie.md`) fixe un premier jalon : un site public
de 100 sociétés réelles avec leurs comptes sourcés et leur mémoire des
promesses. **L'agent suit d'abord cette liste, dans cet ordre**, en
prenant la première tâche non cochée. Quand toute la liste est cochée, il
reprend les phases dans l'ordre du fichier.

1. Fiche lisible : 1.1, 1.2, 1.3, 1.12, 1.14, 1.15
2. Plusieurs sociétés : 2.1, 2.2, 2.3, 2.4, 2.5
3. Données réelles : 3.14, 3.15, 3.1, 3.2, 3.3, 3.4, 3.8, 3.9, 3.12
4. Promesses à grande échelle : 4.1, 4.2, 4.5, 4.6, 4.7, 4.8, 4.9
5. Deux langues : 10.1, 10.2, 10.3
6. Site public : 12.1, 12.2, 12.3, 12.4, 12.7, 12.8, 12.9
7. Présentable : 2.6, 13.1

## Décisions du propriétaire

L'agent ne traite pas ces lignes. Il les rappelle dans ses résumés quand
une tâche en dépend.

- [ ] D1 — Choisir le nom de l'appli et vérifier la marque.
- [ ] D2 — Fournir une clé d'accès à un modèle de langage (bloque la phase 9).
- [ ] D3 — Choisir un fournisseur de cours avec droits d'affichage (bloque les cours réels ; les tâches utilisent un faux fournisseur en attendant).
- [x] D4 — Accès réseau à `sec.gov`, `www.sec.gov` et `data.sec.gov` : ouvert le 12 novembre 2026 dans l'environnement cloud « finapp » (à choisir à chaque nouvelle session). La SEC exige une adresse de contact à chaque requête : elle se passe à la commande, elle ne s'écrit jamais dans le dépôt.
- [ ] D5 — Choisir l'hébergement et le nom de domaine (bloque la phase 14).
- [ ] D6 — Faire relire par un avocat les formulations de l'IA, les classements et les partenariats courtiers avant tout lancement public.
- [ ] D7 — Fixer le seuil d'erreur maximal du jeu de questions (valeur de départ proposée : 2 %).
- [ ] D8 — Pays de création de la société, financement, associé technique (voir `docs/plan-de-creation.md`).

## Phase 1 — Fiche société complète

Référence : `02-calculs.md`, `03-ecrans.md` section 3.3.

- [ ] 1.4 — Étendre `sec.TAGS` au compte de résultat complet listé dans `01-donnees.md` section 3, avec jeu d'exemple au format SEC. Tests.
- [ ] 1.5 — Bilan : indicateurs à une date (`period_type` « instant »), lecture et affichage en mode Pro. Tests.
- [ ] 1.6 — Flux de trésorerie : gérer les cumuls depuis le début de l'exercice et calculer le trimestre isolé par différence, avec formule et entrées. Tests.
- [ ] 1.7 — Quatrième trimestre calculé (exercice moins trois trimestres), marqué « calculé ». Tests.
- [ ] 1.8 — « Douze derniers mois » : fonction de somme des quatre derniers trimestres consécutifs, `None` s'il en manque un. Tests.
- [ ] 1.9 — Rentabilité : rentabilité des capitaux propres et de l'actif, part de la recherche. Tests.
- [ ] 1.10 — Solidité : dette nette, liquidité générale, couverture des intérêts, endettement, avec la règle « non significatif ». Tests.
- [ ] 1.11 — Trésorerie : flux disponible, marge de flux disponible, conversion du bénéfice. Tests.
- [ ] 1.12 — Bloc « Santé » du mode Essentiel : cinq indicateurs (croissance, rentabilité, dette, trésorerie, promesses tenues), chacun avec une phrase modèle produite par du code. Tests des phrases.
- [ ] 1.13 — Tableaux complets du mode Pro : compte de résultat, bilan, flux, par trimestre et par exercice, dans un cadre qui défile, avec export CSV.
- [ ] 1.14 — Graphiques SVG maison : courbe et barres pour chiffre d'affaires et bénéfice, valeurs au toucher, tableau équivalent accessible (`03-ecrans.md` section 4).
- [ ] 1.15 — Fiche source enrichie : formule, entrées, contrôles de qualité, bouton « signaler une erreur » (stockage du signalement, route d'API, tests).
- [ ] 1.16 — Fiche société : informations d'en-tête (bourse, pays, devise, secteur, fin d'exercice) dans le schéma et à l'écran.
- [ ] 1.17 — Comparaison de jusqu'à cinq sociétés côte à côte en mode Pro, sur un indicateur et une période. Tests.
- [ ] 1.18 — Afficher la croissance annuelle moyenne du chiffre d'affaires sur 3 et 5 ans en mode Pro, à partir de `calc.cagr` (déjà écrit et testé), avec sa fiche source. Tests.

## Phase 2 — Plusieurs sociétés, recherche, navigation

Référence : `03-ecrans.md` sections 2 et 3, `07` section 6.

- [ ] 2.1 — Deuxième et troisième jeux d'exemple (marqués exemple), avec des cas différents : société en perte, capitaux propres négatifs, exercice décalé.
- [ ] 2.2 — Navigation par adresse (`#/societe/NVDA`), barre du bas sur téléphone et barre latérale sur ordinateur, retour arrière fonctionnel.
- [ ] 2.3 — Recherche par nom ou symbole tolérante aux accents, à la casse et aux fautes légères ; route d'API et champ de recherche. Tests.
- [ ] 2.4 — Écran d'accueil : barre de recherche, liste des sociétés, sociétés récemment consultées.
- [ ] 2.5 — États de chaque bloc : chargement, vide, erreur, donnée ancienne.
- [ ] 2.6 — Thème sombre, contrastes vérifiés, zones tactiles de 44 px, navigation au clavier.
- [ ] 2.7 — Découper `web/index.html` en fichiers séparés (styles, scripts par écran) en gardant l'export de la page de démonstration autonome. Tests de l'export.

## Phase 3 — Collecte réelle et qualité des données

Référence : `01-donnees.md` sections 4 à 8.

- [ ] 3.1 — `sec.fetch_companyfacts` robuste : délai maximal, trois essais avec attente sur 429 et 5xx, message clair. Tests avec faux serveur local.
- [ ] 3.2 — Lecture de `company_tickers.json` : remplir la table des sociétés (symbole, CIK, nom) à partir d'un fichier d'exemple. Tests.
- [ ] 3.3 — Commande `ingest-sec-batch` : fichier CSV `ticker,cik`, au plus 5 requêtes par seconde, résumé des réussites et échecs. Tests avec faux serveur.
- [ ] 3.4 — Journal de collecte (source, heure, lignes ajoutées, erreurs) et commande pour l'afficher.
- [ ] 3.5 — File d'attente de collecte en SQLite, reprise après arrêt. Tests.
- [ ] 3.6 — Lecture de l'API `submissions` : liste des dépôts d'une société, détection d'un nouveau dépôt. Tests sur fichier d'exemple.
- [ ] 3.7 — Table des événements (dépôts, communiqués) reliée aux sociétés ; affichage de la liste dans la fiche.
- [ ] 3.8 — Heures de connaissance précises : accepter date et heure UTC dans `known_at` sans casser les dates seules. Tests de non-régression.
- [ ] 3.9 — Table des contrôles de qualité et contrôles 1 à 3 (égalité comptable, marge brute, somme des trimestres). Tests.
- [ ] 3.10 — Contrôles 4, 5 et 7 (variation extrême, changement d'unité apparent, trou dans une série). Tests.
- [ ] 3.11 — Affichage des contrôles dans la fiche source et page « Qualité des données » en mode Pro.
- [ ] 3.12 — Âge des données : calcul et affichage par bloc, seuils « donnée ancienne ». Tests.
- [ ] 3.13 — Commande de vérification complète de la base (tous les contrôles) avec rapport lisible.
- [ ] 3.14 — Chiffre republié à l'identique : quand un rapport plus récent rappelle un chiffre déjà connu sans le changer, ne pas en faire une nouvelle version, pour que « connu depuis » reste la date de première publication. Constaté sur les vrais comptes de la SEC pendant la tâche 1.2. Tests.
- [ ] 3.15 — Libellés de trimestre fiables : le champ « exercice » de la SEC est celui du document déposé, pas celui de la période ; déduire le libellé des dates de la période (comme pour les exercices depuis la tâche 1.2). Tests sur fichier au format SEC.

## Phase 4 — Mémoire des promesses étendue

Référence : `05-creations.md` section 1.

- [ ] 4.1 — Plusieurs indicateurs dans `promises.evaluate` (marge brute, bénéfice par action) et à l'écran. Tests.
- [ ] 4.2 — Types d'engagement : borne (« au moins », « au plus ») et sens (« en hausse »), avec verdict adapté. Tests.
- [ ] 4.3 — Révisions de prévision : versions successives, évaluation de la dernière connue avant publication, mention « revue ». Tests.
- [ ] 4.4 — Prévisions annuelles en plus des trimestrielles. Tests.
- [ ] 4.5 — Profil enrichi : écart type, tendance, prudence de la direction, mention « peu de recul » sous quatre évaluations. Tests.
- [ ] 4.6 — Extraction par règles des perspectives dans un communiqué de résultats en texte (formulations courantes en anglais), avec passage d'origine et niveau de confiance. Jeu de dix communiqués d'exemple inventés et marqués exemple. Tests.
- [ ] 4.7 — File de validation : les extractions peu sûres attendent une validation ; commande pour les lister et les accepter ou refuser.
- [ ] 4.8 — Écran « Mémoire des promesses » dédié : vue par société et vue d'ensemble classée par régularité, avec les limites affichées.
- [ ] 4.9 — Phrases du mode Essentiel pour chaque verdict et pour le profil. Tests.

## Phase 5 — Cours

Référence : `07-portefeuille-alertes-brief.md` section 1, `02-calculs.md` sections 6 et 7.

- [ ] 5.1 — Table des cours journaliers et des opérations sur titres ; interface `finapp/prices.py` avec faux fournisseur et import CSV. Tests.
- [ ] 5.2 — Cours ajustés des divisions et dividendes, calculés à la demande. Tests.
- [ ] 5.3 — Calendrier des séances (jours ouvrés, fériés) pour la bourse américaine. Tests.
- [ ] 5.4 — Calculs de performance, volatilité, plus forte baisse. Tests.
- [ ] 5.5 — Corrélation et bêta, minimum 60 séances. Tests.
- [ ] 5.6 — Valorisation : capitalisation, PER, cours sur chiffre d'affaires, valeur d'entreprise et ses ratios, rendements ; la formule affiche les deux dates. Tests.
- [ ] 5.7 — Courbe de cours dans la fiche, événements marqués dessus, mention « différé ».
- [ ] 5.8 — Cryptomonnaies : même table, cotation continue, fiche simplifiée sans comptes. Tests.
- [ ] 5.9 — Bloc « Marchés » de l'accueil à partir des cours disponibles.

## Phase 6 — Grands investisseurs

Référence : `06-grands-investisseurs.md`.

- [ ] 6.1 — Schéma investisseurs et positions ; lecteur de la table d'information d'un 13F au format XML sur fichier d'exemple ; valeur en milliers avant 2023, en dollars depuis. Tests.
- [ ] 6.2 — Table de correspondance CUSIP → symbole avec source ; CUSIP inconnu affiché sous le nom de l'émetteur. Tests.
- [ ] 6.3 — Addition des lignes multiples, séparation actions et options, déclarations corrigées comme nouvelles versions. Tests.
- [ ] 6.4 — Calculs : poids, mouvement du trimestre, variation, concentration, rotation, durée de détention, âge de l'information. Tests.
- [ ] 6.5 — Écran liste des investisseurs et fiche d'un investisseur, deux modes, limites affichées.
- [ ] 6.6 — Bloc « Qui détient » sur la fiche d'une société.
- [ ] 6.7 — Consensus : titres achetés ou renforcés par plusieurs investisseurs le même trimestre. Tests et écran.
- [ ] 6.8 — Lecteur du formulaire 4 (opérations de dirigeants) sur fichier d'exemple ; table et affichage. Tests.
- [ ] 6.9 — Achats groupés de dirigeants. Tests.
- [ ] 6.10 — Lecteur des formulaires 13D et 13G (prises de participation) sur fichiers d'exemple. Tests.
- [ ] 6.11 — Liste de départ de 30 investisseurs suivis avec leur CIK, à faire valider par le propriétaire avant collecte réelle.
- [ ] 6.12 — Prix d'achat estimé (fourchette des cours du trimestre), présenté comme estimation. Tests.

## Phase 7 — Portefeuille, alertes, brief

Référence : `07-portefeuille-alertes-brief.md`.

- [ ] 7.1 — Listes de suivi stockées dans le navigateur : ajouter, retirer, plusieurs listes.
- [ ] 7.2 — Portefeuille dans le navigateur : saisie à la main, import CSV avec erreurs expliquées. Tests du lecteur.
- [ ] 7.3 — Calculs de portefeuille : valeur, poids, plus-values, répartitions, concentration. Tests.
- [ ] 7.4 — Écran portefeuille, deux modes, phrases de constat du mode Essentiel.
- [ ] 7.5 — Corrélations et volatilité du portefeuille en mode Pro. Tests.
- [ ] 7.6 — Moteur d'alertes : modèle (cible, conditions ET / OU), déclenchement une fois par franchissement, délai de repos. Tests.
- [ ] 7.7 — Conditions sur cours et volume. Tests.
- [ ] 7.8 — Conditions sur publications, comptes, promesses. Tests.
- [ ] 7.9 — Conditions sur grands investisseurs et dirigeants. Tests.
- [ ] 7.10 — Écran des alertes : réglage unique du mode Essentiel, composition en mode Pro, historique des déclenchements, centre de notifications.
- [ ] 7.11 — Brief du jour : collecte des nouveautés depuis le dernier brief, filtrage par portefeuille, règles d'importance. Tests.
- [ ] 7.12 — Brief à l'écran : trois phrases en Essentiel, liste groupée en Pro, historique des briefs.
- [ ] 7.13 — Calendrier : dates de résultats avec source, dates limites des 13F.

## Phase 8 — Thèse vivante

Référence : `05-creations.md` section 2.

- [ ] 8.1 — Modèle de thèse et de conditions vérifiables ; évaluation tenue, fragile, rompue, non évaluable. Tests.
- [ ] 8.2 — Historique des changements d'état avec le fait en cause. Tests.
- [ ] 8.3 — Écran : créer une thèse, choisir des conditions dans une liste, voir l'état de santé.
- [ ] 8.4 — Alerte quand une condition change d'état.

## Phase 9 — Questions et IA

Référence : `04-ia.md`.

- [ ] 9.1 — Outils de lecture (`chercher_societe`, `serie`, `calculer`, `comparer`, `promesses`, `detenteurs`, `cours`, `evenements`) sous forme de fonctions testées qui renvoient des faits avec identifiants.
- [ ] 9.2 — Demande structurée : format, validation. Tests.
- [ ] 9.3 — Analyseur à règles en français et en anglais pour les formes courantes de questions. Tests sur 60 formulations.
- [ ] 9.4 — Assemblage de la réponse : repères remplacés par valeurs et liens sources ; rejet de tout nombre hors repère. Tests.
- [ ] 9.5 — Lexique : 80 termes en français, deux niveaux, et l'outil `lexique`.
- [ ] 9.6 — Écran de réponse et barre de question branchés sur l'analyseur à règles ; suggestions quand la question n'est pas reconnue.
- [ ] 9.7 — Liste de formulations interdites et test qui les refuse ; réponse type aux questions de conseil.
- [ ] 9.8 — Jeu de questions `evals/questions.jsonl` : format, 100 premières questions tirées de la base de test, commande d'évaluation avec rapport. Tests.
- [ ] 9.9 — Porter le jeu à 500 questions avec la répartition prévue.
- [ ] 9.10 — Interface `finapp/llm.py` avec faux modèle pour les tests ; clé lue dans une variable d'environnement. Dépend de D2 pour l'usage réel.
- [ ] 9.11 — Étapes comprendre et planifier par le modèle, limitées aux outils. Tests avec faux modèle.
- [ ] 9.12 — Étape rédiger avec repères, puis vérification par second passage. Tests avec faux modèle.
- [ ] 9.13 — Journal des réponses, coût par question, cache des réponses. Tests.
- [ ] 9.14 — Adaptation au mode et à la langue de la question.
- [ ] 9.15 — Page publique « Bulletin de notes de l'IA » alimentée par la commande d'évaluation et par les signalements.

## Phase 10 — Langues

Référence : `08` section 1.

- [ ] 10.1 — Dictionnaires de textes, français par défaut ; plus aucun texte en dur dans l'écran ; test des clés manquantes.
- [ ] 10.2 — Anglais complet et sélecteur de langue.
- [ ] 10.3 — Formats par langue : nombres, dates, devises, pluriels. Tests.
- [ ] 10.4 — Phrases modèles du mode Essentiel en anglais. Tests.
- [ ] 10.5 — Lexique en anglais.
- [ ] 10.6 — Espagnol, allemand, portugais, italien.
- [ ] 10.7 — Japonais et chinois simplifié ; vérification de la mise en page.
- [ ] 10.8 — Préparation de l'écriture de droite à gauche.

## Phase 11 — Graphe de liens et ondes de choc

Référence : `05-creations.md` section 3.

- [ ] 11.1 — Schéma des entités et des liens typés, datés et sourcés. Tests.
- [ ] 11.2 — Jeu d'exemple de liens (marqué exemple) et import CSV.
- [ ] 11.3 — Propagation à un et deux liens, avec chemins et sources. Tests.
- [ ] 11.4 — Bloc « touche aussi » sur un événement, croisé avec le portefeuille.
- [ ] 11.5 — Carte des liens en mode Pro, en SVG, avec tableau équivalent.

## Phase 12 — Pages publiques, partage, confiance

Référence : `03-ecrans.md` section 5, `08` section 2.

- [ ] 12.1 — Page publique par société, lisible sans script, avec titre, description et données structurées.
- [ ] 12.2 — Liens partageables pour une fiche à une date donnée ; version imprimable.
- [ ] 12.3 — Pages « Méthode et sources » et « Comment nous gagnons de l'argent ».
- [ ] 12.4 — Mention « Information, pas conseil » sur chaque écran ; test qui vérifie sa présence.
- [ ] 12.5 — Emplacements de liens partenaires, marqués « partenaire rémunéré », désactivés par défaut.
- [ ] 12.6 — Page d'état : fraîcheur de chaque source, dernier passage de collecte.
- [ ] 12.7 — Page d'accueil publique : la promesse en une phrase, trois exemples de fiches, formulaire de liste d'attente (adresse stockée en base, route d'API, validation, aucune autre donnée). Tests.
- [ ] 12.8 — Commande de contrôle par tirage : tirer 200 chiffres au hasard et produire une feuille de vérification (valeur, période, lien du document) à contrôler à la main ; enregistrer le résultat du contrôle. Tests.
- [ ] 12.9 — Guide d'entretien utilisateurs dans `docs/` : dix questions pour débutants et dix pour investisseurs avancés, grille de notes, en français simple.

## Phase 13 — Comptes et sécurité

Référence : `08` sections 3 à 5.

- [ ] 13.1 — En-têtes de sécurité, politique de contenu stricte, validation des entrées revue sur toutes les routes. Tests.
- [ ] 13.2 — Limite de débit par adresse sur l'API. Tests.
- [ ] 13.3 — Comptes : création par lien de connexion (envoi simulé en développement), sessions. Tests.
- [ ] 13.4 — Synchronisation du portefeuille et des listes pour un compte ; export et suppression de ses données. Tests.
- [ ] 13.5 — Registre des traitements de données dans `docs/`.

## Phase 14 — Préparer la mise en ligne

Référence : `08` sections 6 et 7. Dépend de D5.

- [ ] 14.1 — Couche d'accès aux données compatible PostgreSQL et SQLite, mêmes tests sur les deux quand PostgreSQL est disponible.
- [ ] 14.2 — Séparation des tâches de collecte et du service web ; commande de planification.
- [ ] 14.3 — Fichier de lancement automatique des tests à chaque proposition (GitHub Actions).
- [ ] 14.4 — Appli web installable sur l'écran d'accueil du téléphone, lecture hors connexion des dernières fiches consultées.
- [ ] 14.5 — Guide de mise en ligne pas à pas dans `docs/`, en français simple.

## Phase 15 — Version 2 et suivantes

Référence : `05-creations.md` sections 4, 5 et 7, `04-ia.md` section 10.

- [ ] 15.1 — Jumeaux historiques : recherche de cas ressemblants dans les données telles que connues, fréquences, seuil de 20 cas. Tests.
- [ ] 15.2 — Écart récit-réalité : tableau des désaccords entre prévisions, faits et opérations de dirigeants.
- [ ] 15.3 — Screener multi-critères sur les indicateurs du catalogue ; idées par thème en mode Essentiel.
- [ ] 15.4 — Test historique « si j'avais suivi ce gérant », délai de publication compris.
- [ ] 15.5 — Contradicteur et scénarios (dépend de D2).
- [ ] 15.6 — Offre Équipes : espaces partagés, rôles, piste d'audit.
- [ ] 15.7 — Journal de décisions et miroir de l'investisseur.
- [ ] 15.8 — Sources hors États-Unis, un marché à la fois, en commençant par l'Europe.

## Fait

- [x] Socle : base de faits datés, calculs, mémoire des promesses, API, écran Essentiel/Pro, 25 tests.
- [x] Vision, spécifications détaillées et plan de tâches complet dans `docs/`.
- [x] 1.1 — Marges : ajouter au mode Pro la marge brute, la marge opérationnelle et la marge nette par trimestre, calculées par `calc.margin` ; chaque valeur ouvre sa fiche source. Tests.
- [x] 1.2 — Vue annuelle : série annuelle du chiffre d'affaires dans `views.company_view` avec variation sur un an ; affichage en mode Pro. Tests.
- [x] 1.3 — Variation sur un an par trimestre (même trimestre de l'exercice précédent) et croissance annuelle moyenne sur n ans dans `calc.py`. Tests des cas limites.
