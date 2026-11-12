# Liste des tâches

L'agent prend la première tâche non cochée, dans l'ordre. Pour changer les
priorités, déplace les lignes. Pour ajouter une tâche, ajoute une ligne
`- [ ] ...` avec assez de détails pour qu'elle se comprenne seule.

## À faire

- [ ] Fiche société : ajouter au tableau « Pro » la marge brute, la marge opérationnelle et la marge nette par trimestre, calculées par `calc.margin` à partir des faits `gross_profit`, `operating_income`, `net_income` ; chaque valeur doit ouvrir sa fiche source comme les autres chiffres. Ajouter les tests.
- [ ] Vue annuelle : exposer dans `views.company_view` la série annuelle du chiffre d'affaires (period_type "year") avec la variation d'une année sur l'autre, et l'afficher dans le mode Pro. Ajouter les tests.
- [ ] Page d'accueil : quand plusieurs sociétés sont en base, afficher une liste des sociétés avec recherche par nom ou symbole, puis ouvrir la fiche choisie. Ajouter un deuxième jeu d'exemple (clairement marqué exemple) pour le tester.
- [ ] Collecte SEC : rendre `sec.fetch_companyfacts` robuste (délai maximal, nouvel essai en cas d'erreur 429 ou 5xx avec attente, message clair en cas d'échec) et tester avec un faux serveur local, sans accès réseau réel.
- [ ] Commande `ingest-sec-batch` : lire un fichier CSV `ticker,cik` et collecter chaque société en respectant au plus 5 requêtes par seconde ; résumé final des réussites et échecs. Tests avec faux serveur.
- [ ] Promesses : gérer plusieurs indicateurs (marge brute, bénéfice par action) en plus du chiffre d'affaires dans `promises.evaluate` et dans l'écran. Ajouter les tests.
- [ ] Mode Essentiel : pour chaque chiffre, une phrase d'explication en français simple produite par du code à partir des calculs (pas d'IA), par exemple « Le chiffre d'affaires a augmenté de 19,8 % par rapport au trimestre précédent ». Ajouter les tests.
- [ ] Langues : sortir tous les textes de `web/index.html` dans un dictionnaire, ajouter l'anglais, et un sélecteur de langue. Le français reste la langue par défaut.
- [ ] Accessibilité et petit écran : vérifier contrastes, tailles de zones tactiles (44 px au moins), navigation au clavier ; corriger ce qui manque.
- [ ] Grands investisseurs : schéma et lecteur pour les déclarations 13F de la SEC (positions par fonds et par trimestre, avec source et date de connaissance), sur fichiers d'exemple. Pas encore d'écran.

## Fait

- [x] Socle : base de faits datés, calculs, mémoire des promesses, API, écran Essentiel/Pro, 25 tests.
