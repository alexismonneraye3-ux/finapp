# Règles de travail sur ce dépôt

Appli d'information financière (pas un courtier, jamais de conseil
d'achat ou de vente). Le propriétaire n'est pas développeur : tout ce qui
lui est destiné (résumés, descriptions de propositions, TACHES.md) s'écrit
en français simple, sans jargon.

## Règles du produit, à ne jamais enfreindre

1. Un chiffre ne voyage jamais sans sa source (adresse du document et date).
2. On ne remplace jamais un fait, on ajoute une version (`known_at`).
3. Tout nombre affiché vient d'un fait ou d'un calcul fait par du code
   testé, avec sa formule et ses entrées. Aucun nombre inventé ou estimé.
4. Les données d'exemple sont marquées `is_sample` et signalées à l'écran.

## Règles techniques

- Python, bibliothèque standard uniquement : aucune dépendance à installer.
- Écran : un seul fichier `web/index.html`, JavaScript ES5 sans bibliothèque
  (il doit marcher sur d'anciens Safari), téléphone et ordinateur.
- Tests : `python3 -m unittest discover tests` doit passer en entier avant
  toute proposition. Tout nouveau comportement a ses tests.
- Les tests ne font aucun appel réseau réel.

## Façon de travailler

- Ne jamais pousser sur `main`. Travailler sur une branche `claude/...` et
  ouvrir une proposition de modification (pull request).
- Une tâche de TACHES.md par proposition, petite et relisible.
- Dans la même proposition, cocher la tâche et la déplacer sous « Fait ».
- Si une tâche est ambiguë ou demande une décision du propriétaire, ne pas
  deviner : l'écrire dans la description et passer à la tâche suivante.
