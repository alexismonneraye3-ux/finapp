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
