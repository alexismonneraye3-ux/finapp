"""Bloc « Santé » du mode Essentiel : cinq indicateurs, une phrase chacun.

Les phrases sont des modèles remplis par du code (02-calculs.md, section 9).
Elles décrivent et ne jugent pas : ni « bon », ni « inquiétant ». Chaque
nombre d'une phrase vient d'un calcul déjà présent dans la fiche ; la
phrase est donnée en morceaux pour que l'écran rende ce nombre cliquable.
"""

SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£"}


def number(x, decimals=1):
    """Nombre à la française : virgule, signe moins typographique, pas de « ,0 »."""
    text = ("%.*f" % (decimals, abs(x)))
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if float(text) == 0:
        return "0"
    return ("−" if x < 0 else "") + text.replace(".", ",")


def currency(unit):
    return SYMBOLS.get(unit, unit)


def _item(key, title, parts, available, **details):
    sentence = "".join(p if isinstance(p, str) else p["text"] for p in parts)
    out = {"key": key, "title": title, "available": available,
           "sentence": sentence, "parts": parts}
    out.update(details)
    return out


def _num(text):
    """Morceau de phrase qui porte un nombre : l'écran en fait un bouton source."""
    return {"text": text}


def growth(revenue):
    """Croissance du dernier trimestre : sur un an si possible, sinon sur un trimestre."""
    title = "Croissance"
    last = revenue[-1] if revenue else None
    if last is not None and last.get("growth_year") is not None:
        result, basis = last["growth_year"], "year"
        versus, other = "au même trimestre un an plus tôt", last["year_ago"]
    elif last is not None and last.get("growth") is not None:
        result, basis = last["growth"], "quarter"
        versus, other = "au trimestre précédent", None
    else:
        return _item("growth", title, [
            "Pas assez de trimestres publiés dans nos données pour mesurer la croissance."],
            False)
    rounded = round(result["value"], 1)
    if rounded == 0:
        parts = ["Le chiffre d'affaires est resté stable (",
                 _num(number(0) + " %"), ") par rapport " + versus + "."]
    else:
        verb = "augmenté" if rounded > 0 else "baissé"
        parts = ["Le chiffre d'affaires a %s de " % verb,
                 _num(number(abs(rounded)) + " %"), " par rapport " + versus + "."]
    return _item("growth", title, parts, True, result=result, basis=basis,
                 current=last, compared_to=other)


def profitability(margins):
    """Marge nette du dernier trimestre, dite en monnaie pour 100 de ventes."""
    title = "Rentabilité"
    line = margins[-1] if margins else None
    if line is None:
        return _item("profitability", title, [
            "Aucun trimestre publié dans nos données pour mesurer la rentabilité."], False)
    net = line["net"]
    if net["result"] is None:
        if net["reason"] == "non significatif":
            text = ("Le chiffre d'affaires du dernier trimestre est négatif : "
                    "la rentabilité n'est pas significative.")
        else:
            text = "Le bénéfice du dernier trimestre n'est pas dans nos données."
        return _item("profitability", title, [text], False, reason=net["reason"])
    sym = currency(line["revenue"]["unit"])
    rounded = round(net["result"]["value"], 1)
    start = "Au dernier trimestre publié, sur 100 %s de ventes, l'entreprise " % sym
    if rounded > 0:
        parts = [start + "garde ", _num("%s %s" % (number(rounded), sym)), " de bénéfice."]
    elif rounded < 0:
        parts = [start + "perd ", _num("%s %s" % (number(abs(rounded)), sym)), "."]
    else:
        parts = [start + "ne gagne ni ne perd rien (", _num("0 %s" % sym), ")."]
    return _item("profitability", title, parts, True, result=net["result"], line=line)


def debt():
    """Dette nette : attend le bilan (tâches 1.5 et 1.10)."""
    return _item("debt", "Dette", [
        "Le bilan de l'entreprise n'est pas encore dans nos données : "
        "la dette ne peut pas être mesurée."], False)


def cash():
    """Flux de trésorerie disponible : attend le tableau des flux (tâches 1.6 et 1.11)."""
    return _item("cash", "Trésorerie", [
        "Les flux de trésorerie de l'entreprise ne sont pas encore dans nos "
        "données : la trésorerie dégagée ne peut pas être mesurée."], False)


def promises_kept(items, profile):
    """Prévisions de ventes atteintes ou dépassées, parmi celles déjà dénouées."""
    title = "Promesses tenues"
    n = profile["evaluated"]
    if n == 0:
        return _item("promises", title, [
            "Aucune prévision de la direction n'est encore vérifiable dans nos données."],
            False)
    kept = profile["kept"]
    done = [i for i in items if i["status"] != "en attente"]
    if n == 1:
        parts = ["La direction a %s sa seule prévision de ventes vérifiable ("
                 % ("atteint ou dépassé" if kept else "manqué"),
                 _num("%d sur 1" % kept), ")."]
    else:
        parts = ["La direction a atteint ou dépassé ", _num("%d" % kept),
                 " de ses ", _num("%d" % n), " prévisions de ventes vérifiables."]
    return _item("promises", title, parts, True, kept=kept, evaluated=n,
                 periods=[{"fiscal_label": i["fiscal_label"], "status": i["status"]}
                          for i in done])


def health(revenue, margins, promise_items, promise_profile):
    """Les cinq indicateurs, toujours dans le même ordre."""
    return [growth(revenue), profitability(margins), debt(), cash(),
            promises_kept(promise_items, promise_profile)]
