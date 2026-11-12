"""Données des graphiques : séries, axe et graduations calculés par du code testé.

L'écran ne fait que dessiner. Chaque point garde le fait publié qu'il
représente ; une période sans chiffre donne un point absent (None), jamais
un zéro.
"""

import math

from . import health

SHORT_MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
                "août", "sept.", "oct.", "nov.", "déc."]

# (diviseur, mot) du plus grand au plus petit.
SCALES = [(1e9, "Md"), (1e6, "M"), (1e3, "k"), (1, "")]

MAX_PERIODS = 12


def short_period(period_end):
    """« 2026-04-26 » devient « avr. 2026 » : le mois où la période finit."""
    year, month, _day = period_end[:10].split("-")
    return "%s %s" % (SHORT_MONTHS[int(month) - 1], year)


def scale_for(max_abs):
    """Échelle d'affichage : milliards, millions, milliers ou unités."""
    for divisor, word in SCALES:
        if max_abs >= divisor:
            return divisor, word
    return 1, ""


def nice_step(span, target=4):
    """Pas « rond » (1, 2 ou 5 fois une puissance de dix) pour environ `target` intervalles."""
    if span <= 0:
        return 1.0
    raw = span / float(target)
    power = 10 ** math.floor(math.log10(raw))
    for mult in (1, 2, 5, 10):
        if raw <= mult * power:
            return mult * power
    return 10 * power


def axis(values, unit):
    """Axe vertical : toujours zéro inclus, bornes rondes qui couvrent toutes les valeurs."""
    low = min([0.0] + list(values))
    high = max([0.0] + list(values))
    if low == high:
        high = 1.0
    step = nice_step(high - low)
    lo = math.floor(low / step) * step
    hi = math.ceil(high / step) * step
    divisor, word = scale_for(max(abs(lo), abs(hi)))
    suffix = (" " + word if word else "") + health.currency(unit)
    if word == "" and not suffix.startswith(" "):
        suffix = " " + suffix
    ticks, n = [], int(round((hi - lo) / step))
    for i in range(n + 1):
        value = lo + i * step
        ticks.append({"value": value,
                      "label": health.number(value / divisor, 2) + suffix})
    return {"min": lo, "max": hi, "ticks": ticks, "unit": unit}


def revenue_and_profit(margin_lines):
    """Chiffre d'affaires (barres) et résultat net (courbe) par trimestre.

    Part des lignes de marges de la fiche : une ligne par trimestre de
    chiffre d'affaires, avec le résultat net de la même période s'il est
    publié. Garde les MAX_PERIODS derniers trimestres. Renvoie None s'il
    n'y a rien à tracer ou si les unités diffèrent.
    """
    lines = margin_lines[-MAX_PERIODS:]
    if not lines:
        return None
    revenue = [line["revenue"] for line in lines]
    profit = [line["net"]["numerator"] for line in lines]
    units = set(f["unit"] for f in revenue + profit if f is not None)
    if len(units) != 1:
        return None
    unit = units.pop()
    values = [f["value"] for f in revenue + profit if f is not None]
    series = [{"key": "revenue", "name": "Chiffre d'affaires", "kind": "bars",
               "points": revenue}]
    if any(f is not None for f in profit):
        series.append({"key": "net_income", "name": "Résultat net", "kind": "line",
                       "points": profit})
    return {
        "title": "Chiffre d'affaires et résultat net par trimestre",
        "periods": [{"period_end": line["period_end"],
                     "label": short_period(line["period_end"]),
                     "fiscal_label": line["fiscal_label"]} for line in lines],
        "series": series,
        "axis": axis(values, unit),
        "is_sample": any(f["is_sample"] for f in revenue + profit if f is not None),
    }
