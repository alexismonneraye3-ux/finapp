"""Mémoire des promesses : ce que la direction a annoncé, puis ce qui a été publié."""

from statistics import mean

from . import calc, facts

PENDING = "en attente"
BEAT = "dépassée"        # au-dessus du haut de fourchette
MET = "tenue"            # dans la fourchette
MISSED = "manquée"       # sous le bas de fourchette


def add_promise(conn, company_id, metric, period_end, fiscal_label, mid, unit,
                source_id, stated_at, low=None, high=None, is_deduced=False):
    conn.execute(
        "INSERT OR IGNORE INTO promises (company_id, metric, period_end, fiscal_label, "
        "low, mid, high, unit, source_id, stated_at, is_deduced) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (company_id, metric, period_end, fiscal_label, low, mid, high, unit,
         source_id, stated_at, 1 if is_deduced else 0),
    )


def status(actual, low, mid, high):
    """Verdict d'une promesse. Sans fourchette, on compare à la valeur centrale."""
    if actual is None:
        return PENDING
    low = mid if low is None else low
    high = mid if high is None else high
    if actual > high:
        return BEAT
    if actual < low:
        return MISSED
    return MET


def evaluate(conn, company_id, metric="revenue", as_of=None):
    """Confronte chaque promesse connue à la date as_of au résultat connu à cette date."""
    as_of = as_of or facts.FAR_FUTURE
    rows = conn.execute(
        "SELECT p.*, s.url AS source_url, s.title AS source_title, s.kind AS source_kind "
        "FROM promises p JOIN sources s ON s.id = p.source_id "
        "WHERE p.company_id = ? AND p.metric = ? AND p.stated_at <= ? "
        "ORDER BY p.period_end",
        (company_id, metric, as_of),
    ).fetchall()
    out = []
    for p in rows:
        actual = facts.get_fact(conn, company_id, metric, p["period_end"], as_of)
        value = actual["value"] if actual is not None else None
        out.append({
            "fiscal_label": p["fiscal_label"],
            "period_end": p["period_end"],
            "low": p["low"], "mid": p["mid"], "high": p["high"],
            "unit": p["unit"],
            "stated_at": p["stated_at"],
            "is_deduced": bool(p["is_deduced"]),
            "source": {"url": p["source_url"], "title": p["source_title"],
                       "kind": p["source_kind"]},
            "actual": facts.fact_dict(actual) if actual is not None else None,
            "gap_pct": calc.gap_pct(value, p["mid"]) if value is not None else None,
            "status": status(value, p["low"], p["mid"], p["high"]),
        })
    return out


def profile(items):
    """Habitude de l'entreprise, calculée sur les promesses déjà dénouées."""
    done = [i for i in items if i["status"] != PENDING]
    if not done:
        return {"evaluated": 0, "pending": len(items), "kept": 0,
                "kept_rate": None, "mean_gap_pct": None}
    kept = [i for i in done if i["status"] in (MET, BEAT)]
    return {
        "evaluated": len(done),
        "pending": len(items) - len(done),
        "kept": len(kept),
        "kept_rate": len(kept) / len(done) * 100,
        "mean_gap_pct": mean(i["gap_pct"] for i in done),
    }


def unusual(items, threshold_points=3.0):
    """Signale les résultats qui s'écartent de l'habitude des trimestres précédents.

    Un dépassement habituel n'apprend rien ; ce qui compte est un écart qui
    change. Il faut au moins deux promesses dénouées avant pour juger.
    """
    flagged, history = [], []
    for i in items:
        if i["status"] == PENDING:
            continue
        if len(history) >= 2:
            habit = mean(history)
            if abs(i["gap_pct"] - habit) >= threshold_points:
                flagged.append({"fiscal_label": i["fiscal_label"],
                                "gap_pct": i["gap_pct"], "habit_pct": habit})
        history.append(i["gap_pct"])
    return flagged
