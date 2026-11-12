"""Assemble la fiche d'une société à partir des faits, sans rien inventer."""

from . import calc, facts, promises


def fiscal_label(row):
    fp, fy = row["fiscal_period"], row["fiscal_year"]
    if fp and fy:
        return ("T%s exercice %s" % (fp[1:], fy)) if fp.startswith("Q") else "Exercice %s" % fy
    return row["period_end"]


def timeline(conn, company_id):
    """Dates auxquelles une information nouvelle est devenue connue."""
    rows = conn.execute(
        "SELECT known_at AS d FROM facts WHERE company_id = ? "
        "UNION SELECT stated_at FROM promises WHERE company_id = ? ORDER BY d",
        (company_id, company_id),
    ).fetchall()
    return [r["d"] for r in rows]


# Marges du mode Pro : (clé, nom affiché, indicateur au numérateur).
# Le dénominateur est toujours le chiffre d'affaires du même trimestre.
MARGINS = [
    ("gross", "marge brute", "gross_profit"),
    ("operating", "marge opérationnelle", "operating_income"),
    ("net", "marge nette", "net_income"),
]


def margins(conn, company_id, revenue_rows, as_of=None):
    """Marges par trimestre, une ligne par trimestre de chiffre d'affaires.

    Tous les faits sont lus à la même date as_of. Une marge impossible à
    calculer a `result` à None et une raison (« non disponible » ou « non
    significatif ») : jamais de zéro à la place d'une donnée absente.
    """
    by_period = {}
    for key, _name, metric in MARGINS:
        by_period[key] = {
            (r["period_start"], r["period_end"]): r
            for r in facts.series(conn, company_id, metric, as_of)}
    out = []
    for rev in revenue_rows:
        line = {"period_end": rev["period_end"], "fiscal_label": fiscal_label(rev),
                "revenue": facts.fact_dict(rev)}
        for key, name, _metric in MARGINS:
            num = by_period[key].get((rev["period_start"], rev["period_end"]))
            line[key] = {
                "name": name,
                "result": calc.margin(num, rev, name),
                "reason": calc.margin_reason(num, rev),
                "numerator": facts.fact_dict(num) if num is not None else None,
            }
        out.append(line)
    return out


def company_view(conn, ticker, as_of=None):
    company = facts.get_company(conn, ticker)
    cid = company["id"]

    revenue, prev = [], None
    revenue_rows = facts.series(conn, cid, "revenue", as_of)
    for row in revenue_rows:
        item = facts.fact_dict(row)
        item["fiscal_label"] = fiscal_label(row)
        item["growth"] = (calc.growth(row, prev)
                          if prev is not None and calc.consecutive(prev, row) else None)
        revenue.append(item)
        prev = row

    margin_lines = margins(conn, cid, revenue_rows, as_of)
    margin_sample = any(
        line[key]["numerator"] is not None and line[key]["numerator"]["is_sample"]
        for line in margin_lines for key, _n, _m in MARGINS)

    items = promises.evaluate(conn, cid, "revenue", as_of)
    return {
        "company": {"ticker": company["ticker"], "name": company["name"],
                    "cik": company["cik"]},
        "as_of": as_of,
        "timeline": timeline(conn, cid),
        "revenue": revenue,
        "margins": margin_lines,
        "promises": {
            "items": items,
            "profile": promises.profile(items),
            "unusual": promises.unusual(items),
        },
        "has_sample_data": any(f["is_sample"] for f in revenue) or margin_sample,
    }
