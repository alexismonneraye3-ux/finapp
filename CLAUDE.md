# Règles de travail sur ce dépôt

Appli d'information financière (pas un courtier, jamais de conseil
d'achat ou de vente). Le propriétaire n'est pas développeur : tout ce qui
lui est destiné (résumés, descriptions de propositions, TACHES.md) s'écrit
en français simple, sans jargon.

## À lire avant de coder

1. `docs/strategie.md` (l'ordre et le pourquoi) et `docs/vision.md` : ce
   qu'on construit et les règles qui ne se
   négocient pas.
2. `TACHES.md` : quoi faire, dans quel ordre.
3. Le fichier de `docs/specifications/` cité par la tâche. Il fait foi :
   formules, règles, cas limites, contenu des écrans.

Les études de fond sont dans `docs/analyse-de-marche.md` et
`docs/plan-de-creation.md` ; inutile de les relire à chaque passage.

Si la spécification est muette ou contradictoire sur un point qui change
le résultat pour l'utilisateur, ne pas deviner : choisir l'option la plus
prudente, l'écrire dans la description de la proposition, et proposer la
correction de la spécification dans la même proposition.

## Règles du produit, à ne jamais enfreindre

1. Un chiffre ne voyage jamais sans sa source (adresse du document et date).
2. On ne remplace jamais un fait, on ajoute une version (`known_at`).
3. Tout nombre affiché vient d'un fait ou d'un calcul fait par du code
   testé, avec sa formule et ses entrées. Aucun nombre inventé ou estimé.
4. Les données d'exemple sont marquées `is_sample` et signalées à l'écran.
   Ne jamais écrire de chiffres réels de mémoire dans un jeu d'exemple en
   les présentant comme vérifiés.
5. Aucune formulation de conseil : ni « achète », ni « vends », ni
   objectif de cours, ni jugement de valeur sans règle écrite.
6. Toute information affiche son âge.

## Règles techniques

- Python, bibliothèque standard uniquement : aucune dépendance à installer.
- Écran : dossier `web/`, JavaScript ES5 sans bibliothèque (il doit
  marcher sur d'anciens Safari), téléphone et ordinateur. La commande
  `export-demo` doit continuer à produire une page autonome.
- Tests : `python3 -m unittest discover tests` doit passer en entier avant
  toute proposition. Tout nouveau comportement a ses tests.
- Les tests ne font aucun appel réseau réel. Le réseau se teste avec un
  faux serveur local ou des fichiers de `fixtures/`.
- Aucune clé ni secret dans le dépôt.
- Requêtes SQL toujours paramétrées.
- Ne pas casser l'API existante sans le dire dans la proposition.

## Façon de travailler

- Ne jamais pousser sur `main`. Travailler sur une branche `claude/...` et
  ouvrir une proposition de modification (pull request).
- Une tâche de TACHES.md par proposition, petite et relisible. Une tâche
  trop grosse se découpe : faire la première partie, ajouter les suivantes
  dans TACHES.md.
- Dans la même proposition, cocher la tâche et la déplacer sous « Fait ».
- Ne pas traiter les lignes « Décisions du propriétaire » ; les rappeler
  quand une tâche en dépend.
- Si une tâche est ambiguë ou demande une décision du propriétaire, ne pas
  deviner : l'écrire dans la description et passer à la tâche suivante.
- Mettre `README.md` à jour quand une commande ou un fichier change.
