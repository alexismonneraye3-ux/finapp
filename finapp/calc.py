"""Calculs déterministes. Chaque résultat garde sa formule et ses entrées."""

from datetime import date


def _result(name, value, unit, formula, inputs):
    return {"name": name, "value": value, "unit": unit,
            "formula": formula, "input_fact_ids": inputs}


def consecutive(prev, cur, tolerance_days=7):
    """Vrai si la période cur suit immédiatement la période prev."""
    if not cur["period_start"]:
        return False
    gap = (date.fromisoformat(cur["period_start"])
           - date.fromisoformat(prev["period_end"])).days
    return 0 <= gap <= tolerance_days


def growth(cur, prev):
    """Variation en % entre deux faits de même indicateur, ou None."""
    if prev is None or prev["value"] == 0 or cur["unit"] != prev["unit"]:
        return None
    value = (cur["value"] - prev["value"]) / abs(prev["value"]) * 100
    return _result(
        "variation", value, "%",
        "(%s − %s) ÷ %s × 100" % (_n(cur["value"]), _n(prev["value"]), _n(abs(prev["value"]))),
        [cur["id"], prev["id"]])


def same_period_last_year(rows, cur, tolerance_days=10):
    """Le fait de `rows` qui couvre la même période un an avant `cur`, ou None.

    Les exercices de 52 ou 53 semaines décalent les dates de quelques jours :
    on accepte une fin de période située un an plus tôt à `tolerance_days`
    près, et une durée de période voisine. S'il manque, None : on ne
    compare jamais avec un autre trimestre.
    """
    if not cur["period_start"]:
        return None
    cur_end = date.fromisoformat(cur["period_end"])
    cur_len = (cur_end - date.fromisoformat(cur["period_start"])).days
    best, best_gap = None, None
    for r in rows:
        if not r["period_start"]:
            continue
        end = date.fromisoformat(r["period_end"])
        length = (end - date.fromisoformat(r["period_start"])).days
        gap = abs((cur_end - end).days - 365)
        if gap <= tolerance_days and abs(length - cur_len) <= tolerance_days:
            if best is None or gap < best_gap:
                best, best_gap = r, gap
    return best


def year_over_year(cur, year_ago):
    """Variation sur un an en % : (T − T₋₄) ÷ |T₋₄| × 100, ou None."""
    result = growth(cur, year_ago)
    if result is not None:
        result["name"] = "variation sur un an"
    return result


def cagr(end, start, years):
    """Croissance annuelle moyenne en % entre deux faits séparés de `years` ans.

    ((fin ÷ début)^(1/n) − 1) × 100, seulement si début et fin sont
    strictement positifs, de même unité, et n ≥ 1. Sinon None.
    """
    if (end is None or start is None or not years or years < 1
            or end["unit"] != start["unit"]
            or end["value"] <= 0 or start["value"] <= 0):
        return None
    value = ((end["value"] / start["value"]) ** (1.0 / years) - 1) * 100
    return _result(
        "croissance annuelle moyenne", value, "%",
        "((%s ÷ %s)^(1/%s) − 1) × 100" % (_n(end["value"]), _n(start["value"]), _n(years)),
        [end["id"], start["id"]])


def margin_reason(numerator, denominator):
    """Pourquoi une marge ne peut pas être calculée, ou None si elle peut l'être.

    « non disponible » : une entrée manque, le dénominateur est nul ou les
    unités diffèrent. « non significatif » : le dénominateur est négatif.
    """
    if (numerator is None or denominator is None or denominator["value"] == 0
            or numerator["unit"] != denominator["unit"]):
        return "non disponible"
    if denominator["value"] < 0:
        return "non significatif"
    return None


def margin(numerator, denominator, name="marge"):
    """Marge en % (par exemple résultat net ÷ chiffre d'affaires), ou None."""
    if margin_reason(numerator, denominator) is not None:
        return None
    value = numerator["value"] / denominator["value"] * 100
    return _result(
        name, value, "%",
        "%s ÷ %s × 100" % (_n(numerator["value"]), _n(denominator["value"])),
        [numerator["id"], denominator["id"]])


def gap_pct(actual, target):
    """Écart en % d'une valeur réalisée par rapport à une cible."""
    if not target:
        return None
    return (actual - target) / abs(target) * 100


def _n(x):
    return ("%.0f" % x) if float(x).is_integer() else ("%s" % x)
