# Plan de création de A à Z — Appli d'information financière

11 novembre 2026

## Synthèse

L'objectif : la plus précise des applis d'information financière accessibles à tous, gratuite et sans limite pour les particuliers, financée par les courtiers puis par les professionnels.

- **Le produit.** Une IA qui répond à toute question financière avec la source de chaque chiffre, dans deux interfaces (Essentiel et Pro), plus des créations propres : mémoire des promesses, thèse vivante, ondes de choc.
- **La preuve de précision.** Les chiffres viennent d'une base vérifiée, jamais de la mémoire de l'IA, et le taux d'erreur est mesuré et publié.
- **Le démarrage.** Actions américaines et cryptomonnaies d'abord, parce que leurs données sont publiques ou bon marché ; les autres marchés suivent un par un.
- **L'argent.** Partenariats courtiers dès le lancement, offre Équipes ensuite, licences de données quand l'audience est là.
- **Les moyens.** Une équipe d'environ huit personnes et un financement de l'ordre de 1,5 à 2 M€ pour 18 mois, hypothèse de travail à confirmer par des devis.
- **Le calendrier.** Prototype à 3 mois, version bêta à 6 mois, lancement public à 9 mois, offre Équipes à 12 mois.

Ce document est le plan. Le produit fini demandera une équipe, des licences de données et une validation juridique que je ne peux pas remplacer ; je peux en revanche produire les maquettes, un prototype, le modèle financier et le dossier investisseurs. L'étude de marché détaillée se trouve dans le document « Analyse de marché ».

## Hypothèses de départ

J'ai retenu les hypothèses ci-dessous pour avancer ; chacune change le plan si elle est fausse.

| Sujet | Hypothèse retenue | À confirmer par toi |
| --- | --- | --- |
| Fondateurs | Tu portes la vision et le financement ; il faut un associé technique | As-tu déjà un associé technique ? |
| Financement | Levée d'amorçage de 1,5 à 2 M€ | Quel apport personnel, quels investisseurs possibles ? |
| Pays de la société | Union européenne, France par défaut | Où veux-tu créer la société ? |
| Premier marché | Actions américaines et cryptos, interface en anglais et en français | D'accord pour ne pas ouvrir tous les pays le premier jour ? |
| Activité | Information financière uniquement, aucun passage d'ordres | Confirmé dans nos échanges |
| Modèle | Gratuit sans limite pour les particuliers, payant pour les équipes | Confirmé dans nos échanges |
| Nom et marque | Non choisis | À définir avant toute communication |

## Le produit, version par version

La version 1 doit prouver une seule chose : des réponses justes et sourcées, mieux que tout ce qui est gratuit aujourd'hui.

| | Version 1 (lancement) | Version 2 (12 à 18 mois) | Version 3 (18 à 24 mois et après) |
| --- | --- | --- | --- |
| Marchés | Actions et ETF américains, cryptos | Europe, puis Asie, un marché à la fois | Couverture mondiale |
| Données | Différées pour les actions, temps réel pour les cryptos | Temps réel pour l'offre Équipes | Données alternatives |
| IA | Questions-réponses sourcées, brief quotidien | Thèse vivante complète, contradicteur, scénarios | Agents, accès ouvert pour IA externes |
| Écrans | Fiche d'actif en modes Essentiel et Pro, portefeuille, alertes | Screener, graphiques avancés, espaces d'équipe | Place de marché, pages des sociétés cotées |
| Créations propres | Mémoire des promesses, suivi des grands investisseurs | Ondes de choc, écart récit-réalité | Indice d'attention mondial, miroir de l'investisseur |
| Langues | IA dans toutes les langues ; interface en anglais et français | Six langues de plus | Lecture des sources étrangères en langue locale |
| Revenus | Partenariats courtiers | Offre Équipes | Licences de données, API commerciale |

**Ce qui reste hors de la version 1, volontairement.** Le temps réel sur les actions, les graphiques avancés et l'ouverture simultanée de tous les pays. Ce sont les trois postes qui coûtent le plus cher et qui retarderaient le lancement sans prouver la promesse de précision.

**Les écrans de la version 1.**

1. Accueil : le brief du jour et la barre de question.
2. Réponse de l'IA : texte, chiffres cliquables jusqu'à la source, graphique.
3. Fiche d'un actif, en mode Essentiel et en mode Pro.
4. Portefeuille et liste de suivi.
5. Mémoire des promesses d'une entreprise.
6. Grands investisseurs : portefeuilles et mouvements.
7. Alertes.
8. Compte, réglages, choix du mode et de la langue.

## Architecture technique et exactitude

Le système est construit autour d'une base de faits vérifiés : l'IA la lit et l'explique, elle ne l'alimente pas et n'invente aucun chiffre.

| Couche | Rôle | Choix pour la version 1 |
| --- | --- | --- |
| Sources | Cours, comptes, communiqués, actualités | Dépôts du régulateur américain (gratuits), un fournisseur de cours à licence d'affichage, flux crypto publics |
| Collecte | Récupérer chaque donnée dès sa publication | Surveillance continue des sources, file d'attente de traitement |
| Base de faits | Stocker chaque chiffre avec sa source, sa date et son heure | Base historisée : on sait ce qui était connu à chaque date |
| Calcul | Ratios, écarts, comparaisons | Code classique et testé, jamais l'IA |
| IA | Comprendre la question, chercher les faits, rédiger la réponse | Modèle de langage du marché, branché sur la base ; second passage de vérification |
| Applis | Montrer et alerter | Téléphone et web à partir d'un même code |
| Supervision | Détecter retards, pannes et erreurs | Tableaux de bord, alertes internes, bascule sur un second fournisseur |

**Pourquoi cette architecture.** Les modèles de langage seuls se trompent trop sur les chiffres. Sur le banc d'essai FinanceBench, un modèle de pointe avec recherche documentaire a mal répondu ou refusé de répondre à 81 % d'un échantillon de 150 questions. Les systèmes qui décomposent chaque affirmation et la vérifient descendent autour de 4 % d'erreurs. La règle retenue par les praticiens : tout chiffre est recalculé hors du modèle.

**Le plan qualité.**

1. Un jeu de 500 questions à réponse connue, rejoué avant chaque mise en ligne.
2. Aucune mise en ligne si le taux d'erreur dépasse le seuil fixé.
3. Chaque réponse affiche ses sources et l'heure des données.
4. Un bouton « signaler une erreur » sur chaque chiffre, traité sous 24 heures.
5. Le taux d'erreur est publié chaque mois.

**Sécurité et fiabilité.** Chiffrement des données, connexion à double facteur, hébergement dans l'Union européenne, tests d'intrusion avant le lancement, et capacité prévue pour les pics d'activité, puisque les pannes aux heures de pointe sont le premier reproche fait aux applis concurrentes.

**Construire ou acheter.** Acheter : modèle de langage, hébergement, flux de données, authentification, paiement. Construire : la base de faits, la vérification, les créations propres, les interfaces. C'est là que se trouve notre avantage.

## Équipe et organisation

Huit personnes suffisent pour la version 1 ; le recrutement le plus urgent est un associé technique.

| Rôle | Mission | Arrivée |
| --- | --- | --- |
| Fondateur dirigeant | Vision, financement, partenariats courtiers | Mois 0 |
| Associé technique | Architecture, recrutement technique, qualité | Mois 0 |
| Ingénieur données | Collecte, base de faits, fraîcheur | Mois 1 |
| Ingénieur IA | Recherche des faits, vérification, jeu de tests | Mois 1 |
| Développeur applis | Téléphone et web | Mois 2 |
| Designer produit | Les deux interfaces, lisibilité | Mois 2 |
| Analyste financier | Contrôle des données, jeu de questions, contenus pédagogiques | Mois 3 |
| Responsable croissance | Communauté, contenus, lancement | Mois 6 |

**En appui externe.** Un avocat spécialisé en droit financier dès le mois 1, un expert-comptable, et un prestataire de tests de sécurité avant le lancement.

**Plus tard.** Un commercial pour l'offre Équipes vers le mois 12, puis un responsable conformité quand l'activité s'étend à plusieurs pays.

**Faire appel à une agence ?** Une agence peut livrer une première appli en trois à six mois. Je la déconseille pour le cœur du produit : la base de faits et la vérification sont notre avantage et doivent rester en interne.

## Budget et financement

L'ordre de grandeur est de 1,5 à 2 M€ pour tenir 18 mois, ce qui correspond à une levée d'amorçage européenne médiane.

**Repères du marché.**

| Poste | Repère trouvé |
| --- | --- |
| Première version d'une appli financière par une agence | 50 000 à 150 000 $, en 3 à 6 mois |
| Version complète avec conformité | 150 000 à 300 000 $, en 6 à 12 mois |
| Supplément pour une appli riche en IA | 20 à 40 % de plus |
| Entretien annuel | 15 à 25 % du coût de construction |
| Données de marché pour une jeune société | D'environ 333 à 1 499 $ par mois chez un fournisseur avec droits d'affichage |
| Temps réel consolidé redistribué | Couramment plus de 10 000 $ par mois |
| Levée d'amorçage médiane en Europe | Environ 2,0 M€, pour une valorisation avant levée d'environ 6 M€ |

**Répartition indicative sur 18 mois.** Ce sont des proportions de travail, pas des devis.

| Poste | Part du budget |
| --- | --- |
| Salaires de l'équipe | Environ 70 % |
| Données de marché et licences | Environ 8 % |
| IA et hébergement | Environ 8 % |
| Juridique, conformité, sécurité | Environ 6 % |
| Lancement et acquisition | Environ 8 % |

**Parcours de financement.**

1. **Mois 0 à 3 : apport des fondateurs et proches**, pour le prototype et les premiers tests de précision.
2. **Mois 3 à 6 : levée d'amorçage**, appuyée sur le prototype et une liste d'attente.
3. **Mois 18 à 24 : tour suivant**, appuyé sur l'audience et les premiers revenus de l'offre Équipes.

À étudier en complément : aides publiques à l'innovation et crédits offerts par les fournisseurs d'hébergement et d'IA aux jeunes sociétés.

**Ce que je n'ai pas chiffré.** Les salaires dépendent du pays, et le coût de l'IA par question dépend du modèle choisi et de l'usage réel. Ces deux postes décident du budget final et doivent être établis avec l'associé technique.

## Juridique et conformité

La ligne à ne pas franchir : informer et expliquer, sans jamais recommander un placement à une personne donnée. Tout ce qui suit est à valider par un avocat ; je ne suis pas juriste.

| Sujet | Ce qu'il faut savoir | Action |
| --- | --- | --- |
| Information ou conseil | En France, une recommandation personnalisée est un conseil en investissement, activité réservée à des statuts encadrés ; l'exercer sans agrément expose à des sanctions pénales | Faire relire par un avocat les réponses types de l'IA et les formulations interdites |
| Scores et indicateurs | Un score sur une entreprise peut être traité comme une recommandation d'investissement, avec des obligations de présentation objective et de transparence sur les conflits d'intérêts | Méthode publiée, conflits affichés, avis juridique avant lancement |
| IA | Le règlement européen sur l'IA impose transparence et supervision humaine pour les usages à risque ; le régulateur européen des marchés rappelle que la direction reste responsable de ce que fait l'IA | Qualifier notre niveau de risque, documenter les contrôles |
| Partenariats courtiers | La rémunération pour apport de clients est encadrée selon les pays | Vérifier le statut requis dans chaque pays avant de signer |
| Données personnelles | Portefeuilles et questions sont des données sensibles au sens du règlement européen | Consentement, minimisation, hébergement en Europe, registre des traitements |
| Licences de données | Afficher ou redistribuer des cours exige des droits précis, différents de l'usage personnel | Lire chaque contrat : affichage, redistribution, usage par l'IA |
| Cryptomonnaies | Le règlement européen sur les crypto-actifs encadre les services ; l'information seule en est en principe distincte | Confirmer que nous restons hors du champ |
| Marque et propriété | Nom, logo, code et bases de données | Dépôt de marque, cession des droits par chaque salarié et prestataire |
| Boutiques d'applis | Règles propres aux applis financières | Lire les conditions avant de développer |

**Garde-fous intégrés au produit.**

- L'IA ne dit jamais « achète » ou « vends » ; elle expose des faits, des scénarios et des risques.
- Chaque écran rappelle qu'il s'agit d'information, pas de conseil.
- Chaque lien rémunéré est affiché comme tel.
- Un journal conserve ce que l'IA a répondu, pour pouvoir le justifier.

**Ordre d'ouverture des pays.** Chaque pays ajoute ses règles ; l'ouverture se fait donc un pays à la fois, après avis local.

## Mise sur le marché

Le produit doit se faire connaître par ce qu'il produit : des réponses et des pages que les gens partagent, plutôt que de la publicité achetée.

**Le message.** « La réponse juste, avec la preuve. » Une phrase pour les débutants : comprendre avant d'investir. Une phrase pour les avancés : une question au lieu de quarante recherches.

| Canal | Ce qu'on fait | Pourquoi |
| --- | --- | --- |
| Pages publiques | Une page gratuite par entreprise : promesses tenues ou non, positions des grands investisseurs | Attire par les moteurs de recherche et les IA, sans budget publicitaire |
| Réponses partageables | Chaque réponse de l'IA peut être partagée avec ses sources | Chaque partage est une démonstration du produit |
| Communautés | Présence sur les forums et réseaux où les investisseurs discutent | C'est là que se trouvent les utilisateurs avancés |
| Créateurs de contenu | Partenariats affichés avec des créateurs sérieux | YouTube et Instagram sont les premières sources d'information dans plusieurs pays |
| Étudiants et clubs d'investissement | Accès et ateliers | Forme les futurs professionnels, clients de l'offre Équipes |
| Courtiers partenaires | L'appli proposée à leurs clients | Distribution et revenu en même temps |
| Clients pilotes | Dix conseillers indépendants ou petits fonds accompagnés de près | Construit l'offre Équipes avec ceux qui la paieront |

**Le déroulé.**

1. **Avant le lancement :** liste d'attente, publication régulière de nos mesures de précision, pages publiques en ligne.
2. **Bêta fermée :** quelques centaines d'utilisateurs choisis, moitié débutants, moitié avancés.
3. **Lancement public :** un pays et deux langues, avec un événement autour d'un test comparatif de précision.
4. **Extension :** un nouveau marché tous les trois à quatre mois.

**Ce qu'on ne fait pas.** Pas de promesse de gains, pas de publicité agressive, pas d'incitation à trader : c'est contraire au positionnement et risqué juridiquement.

## Modèle financier

Dans ce scénario de travail, l'activité devient bénéficiaire au cours de la troisième année, portée par l'offre Équipes. Tous les chiffres de cette section sont des hypothèses que j'ai posées pour structurer le raisonnement, pas des prévisions.

**Hypothèses.**

| Hypothèse | Année 1 | Année 2 | Année 3 |
| --- | --- | --- | --- |
| Utilisateurs actifs | 50 000 | 300 000 | 1 000 000 |
| Part qui ouvre un compte chez un courtier partenaire | 1 % | 1 % | 1 % |
| Commission par compte | 150 $ | 150 $ | 150 $ |
| Entreprises clientes de l'offre Équipes | 20 | 150 | 500 |
| Postes par entreprise | 5 | 5 | 5 |
| Prix par poste et par an | 3 000 $ | 3 000 $ | 3 000 $ |

**Résultat du scénario.**

| | Année 1 | Année 2 | Année 3 |
| --- | --- | --- | --- |
| Revenus courtiers | 75 000 $ | 450 000 $ | 1 500 000 $ |
| Revenus Équipes | 300 000 $ | 2 250 000 $ | 7 500 000 $ |
| Revenus totaux | 375 000 $ | 2 700 000 $ | 9 000 000 $ |
| Dépenses | 1 500 000 $ | 3 500 000 $ | 7 000 000 $ |
| Résultat | −1 125 000 $ | −800 000 $ | +2 000 000 $ |

**Comment lire ce tableau.**

- L'offre Équipes fait au moins 80 % des revenus dès la première année : c'est elle qu'il faut réussir.
- Les revenus courtiers restent modestes, mais ils existent dès le premier jour et ne demandent pas de commerciaux.
- Les licences de données ne sont pas comptées ; elles viendraient s'ajouter à partir de la troisième année.
- Le besoin de financement cumulé atteint environ 1,9 M$ sur les deux premières années, cohérent avec la levée envisagée.

**Les trois chiffres qui font tout basculer.**

1. Le nombre d'entreprises clientes : à 250 au lieu de 500 en année 3, le résultat tombe à −1 750 000 $.
2. Le coût de l'IA par utilisateur gratuit : il grandit avec l'audience et n'est pas encore mesuré.
3. Le prix par poste : à tester auprès des clients pilotes avant toute projection sérieuse.

Une fois le coût par question et les devis de données connus, ce scénario doit être refait dans un tableur avec plusieurs variantes.

## Feuille de route sur 24 mois

Sept étapes, chacune avec un critère de passage : on n'avance pas tant que le critère n'est pas atteint.

| Période | Étape | Ce qui est livré | Critère de passage |
| --- | --- | --- | --- |
| Mois 0 à 1 | Fondations | Société créée, associé technique, avocat choisi, maquettes des écrans, entretiens avec 20 utilisateurs cibles | Les entretiens confirment le besoin |
| Mois 1 à 3 | Prototype | IA sourcée sur 100 sociétés américaines, mémoire des promesses, jeu de 500 questions | Taux d'erreur sous le seuil fixé |
| Mois 3 à 6 | Bêta fermée | Applis téléphone et web, brief quotidien, portefeuille, alertes ; levée d'amorçage | Les testeurs reviennent chaque semaine |
| Mois 6 à 9 | Lancement public | Toutes les sociétés américaines, cryptos, pages publiques, premiers courtiers partenaires | Fiabilité tenue pendant une journée de marché agitée |
| Mois 9 à 12 | Offre Équipes | Espaces partagés, piste d'audit, paiement en ligne, dix clients pilotes | Des pilotes deviennent payants |
| Mois 12 à 18 | Extension | Temps réel, Europe, ondes de choc, six langues de plus | Un deuxième marché atteint l'usage du premier |
| Mois 18 à 24 | Échelle | Asie, licences de données, accès pour IA externes, tour de financement suivant | Revenus récurrents en ligne avec le scénario |

**Les 30 premiers jours.**

- ☐ Choisir le pays et créer la société.
- ☐ Trouver l'associé technique.
- ☐ Mener 20 entretiens : débutants, investisseurs avancés, traders, conseillers.
- ☐ Valider les maquettes des huit écrans.
- ☐ Demander des devis à trois fournisseurs de données.
- ☐ Prendre un premier rendez-vous avec un avocat en droit financier.
- ☐ Choisir le nom et vérifier la disponibilité de la marque.

## Pilotage, risques et décisions

La précision se pilote comme un chiffre d'affaires : mesurée chaque semaine, avec un responsable.

**Indicateurs.**

| Famille | Indicateur |
| --- | --- |
| Précision | Taux d'erreur sur le jeu de questions ; part des réponses avec source ; délai entre publication d'une donnée et sa présence dans l'appli |
| Fiabilité | Disponibilité aux heures de marché ; temps de réponse |
| Usage | Utilisateurs actifs par semaine ; part qui revient après quatre semaines ; questions par utilisateur |
| Revenus | Comptes ouverts chez les partenaires ; entreprises clientes ; revenu récurrent |
| Coûts | Coût par question ; coût des données par utilisateur |
| Confiance | Erreurs signalées et délai de correction ; recommandation par les utilisateurs |

**Risques principaux.**

| Risque | Gravité | Parade |
| --- | --- | --- |
| Une erreur de l'IA devient publique | Élevée | Vérification systématique, taux d'erreur publié, correction rapide et visible |
| Requalification en conseil en investissement | Élevée | Avis juridique avant lancement, formulations encadrées, journal des réponses |
| Les coûts d'IA dépassent les revenus | Élevée | Mesure dès le prototype, garde contre les abus, modèles moins chers pour les questions simples |
| Un géant sort un produit proche | Moyenne | Indépendance, précision prouvée, données propres qui s'accumulent |
| L'offre Équipes ne se vend pas | Élevée | Clients pilotes dès le mois 9, prix testé tôt |
| Pas d'associé technique | Bloquant | Priorité des 30 premiers jours |
| Dépendance à un fournisseur de données ou d'IA | Moyenne | Deux fournisseurs pour chaque brique critique |

**Décisions qui t'appartiennent.**

- ☐ Pays de création de la société.
- ☐ Apport personnel et stratégie de levée.
- ☐ Associé technique : qui, et quelle part du capital.
- ☐ Premier marché et langues de lancement.
- ☐ Nom de l'appli.

**Ce que je peux produire ensuite.** Les maquettes des huit écrans dans les deux modes, un prototype cliquable, le modèle financier en tableur avec variantes, le dossier de présentation aux investisseurs, le guide d'entretien utilisateurs et le cahier des charges technique détaillé.

## Sources

Repères issus de recherches web du 11 novembre 2026, à confirmer par des devis et des avis professionnels.

- [Coût d'une appli financière en 2026 – Acquaint Softtech](https://acquaintsoft.com/blog/fintech-app-development-cost)
- [Coût d'une appli financière – SPD Technology](https://spd.tech/industries/fintech/)
- [Coût d'une appli financière – 8ration](https://www.8ration.com/blogs/fintech-app-development-cost/)
- [Tarifs Intrinio et alternatives – Multiples](https://multiples.vc/compare/intrinio-api-alternatives/md)
- [Guide des licences de données pour fintechs – Intrinio](https://intrinio.com/blog/market-data-licensing-guide-for-fintechs)
- [Licences d'affichage des cours – MarketData.app](https://www.marketdata.app/?p=10587)
- [Valorisations du capital-risque européen début 2026 – Crowdfund Insider](https://www.crowdfundinsider.com/2026/05/280281-european-vc-valuations-surge-in-early-2026-driven-by-later-stage-deals-and-ai-adoption-research/)
- [Contrôles d'exactitude de l'IA en finance, résultats FinanceBench – Rework](https://resources.rework.com/libraries/ai-for-finance/ai-accuracy-controls-in-finance)
- [FinGround, vérification des affirmations financières – Emergent Mind](https://api.emergentmind.com/papers/2604.23588)
- [Statuts de conseiller en investissements financiers – AMF et ACPR](https://www.amf-france.org/sites/institutionnel/files/pdf/69893/fr/L%27ACPR_et_l%27AMF_publient_un_guide_d%27information_sur_les_statuts_de_conseiller_en_investissements_financiers_et_d%27entreprise_d%27investissement.pdf?1771276953)
- [Régime des conseillers en investissements financiers – AMF](https://www.amf-france.org/fr/reglementation/doctrine/doc-2006-23)
- [Déclaration de l'ESMA sur l'IA – CMS](https://cms.law/en/bel/legal-updates/esma-issues-first-formal-guidance-on-use-of-ai-in-retail-financial-services)
- [AlphaSense – Sacra](https://sacra.com/research/alphasense)
- [Affiliation Interactive Brokers – UpPromote](https://uppromote.com/affiliate-program-directory/interactive-brokers)
- [Enquête coréenne sur les applis de courtage – SBS Biz](https://biz.sbs.co.kr/amp/article/20000254842)
- [Sources d'information au Brésil – Acionista](https://acionista.com.br/canal-de-negocios-vai-do-youtube-a-tv-e-alcanca-30-milhoes-de-brasileiros/)
