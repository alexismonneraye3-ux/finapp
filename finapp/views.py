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


def company_view(conn, ticker, as_of=None):
    company = facts.get_company(conn, ticker)
    cid = company["id"]

    revenue, prev = [], None
    for row in facts.series(conn, cid, "revenue", as_of):
        item = facts.fact_dict(row)
        item["fiscal_label"] = fiscal_label(row)
        item["growth"] = (calc.growth(row, prev)
                          if prev is not None and calc.consecutive(prev, row) else None)
        revenue.append(item)
        prev = row

    items = promises.evaluate(conn, cid, "revenue", as_of)
    return {
        "company": {"ticker": company["ticker"], "name": company["name"],
                    "cik": company["cik"]},
        "as_of": as_of,
        "timeline": timeline(conn, cid),
        "revenue": revenue,
        "promises": {
            "items": items,
            "profile": promises.profile(items),
            "unusual": promises.unusual(items),
        },
        "has_sample_data": any(f["is_sample"] for f in revenue),
    }
