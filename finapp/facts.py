"""Écriture et lecture des faits, avec lecture « tel que connu à une date »."""

from datetime import date

FAR_FUTURE = "9999-12-31"


def period_type(period_start, period_end):
    """Classe une période d'après sa durée."""
    if not period_start:
        return "instant"
    days = (date.fromisoformat(period_end) - date.fromisoformat(period_start)).days
    if 80 <= days <= 100:
        return "quarter"
    if 350 <= days <= 380:
        return "year"
    return "other"


def upsert_company(conn, ticker, name, cik=None):
    conn.execute(
        "INSERT INTO companies (ticker, name, cik) VALUES (?, ?, ?) "
        "ON CONFLICT(ticker) DO UPDATE SET name = excluded.name, "
        "cik = COALESCE(excluded.cik, companies.cik)",
        (ticker.upper(), name, cik),
    )
    return get_company(conn, ticker)["id"]


def get_company(conn, ticker):
    row = conn.execute(
        "SELECT * FROM companies WHERE ticker = ?", (ticker.upper(),)
    ).fetchone()
    if row is None:
        raise KeyError("Société inconnue : %s" % ticker)
    return row


def list_companies(conn):
    return conn.execute("SELECT * FROM companies ORDER BY ticker").fetchall()


def add_source(conn, kind, url, title, published_at=None):
    conn.execute(
        "INSERT OR IGNORE INTO sources (kind, url, title, published_at) "
        "VALUES (?, ?, ?, ?)",
        (kind, url, title, published_at),
    )
    return conn.execute("SELECT id FROM sources WHERE url = ?", (url,)).fetchone()["id"]


def add_fact(conn, company_id, metric, period_start, period_end, value, unit,
             source_id, known_at, fiscal_year=None, fiscal_period=None,
             is_sample=False):
    """Ajoute une version d'un chiffre. Renvoie True si elle est nouvelle."""
    period_start = period_start or ""
    cur = conn.execute(
        "INSERT OR IGNORE INTO facts (company_id, metric, period_start, period_end, "
        "period_type, fiscal_year, fiscal_period, value, unit, source_id, known_at, "
        "is_sample) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (company_id, metric, period_start, period_end,
         period_type(period_start, period_end), fiscal_year, fiscal_period,
         float(value), unit, source_id, known_at, 1 if is_sample else 0),
    )
    return cur.rowcount == 1


_SELECT = """
SELECT f.*, s.url AS source_url, s.title AS source_title, s.kind AS source_kind,
       s.published_at AS source_published_at
FROM facts f JOIN sources s ON s.id = f.source_id
"""

# Pour chaque période, ne garder que la dernière version connue à la date as_of.
_LATEST = """
AND f.known_at = (
    SELECT MAX(g.known_at) FROM facts g
    WHERE g.company_id = f.company_id AND g.metric = f.metric
      AND g.period_start = f.period_start AND g.period_end = f.period_end
      AND g.known_at <= ?)
"""


def series(conn, company_id, metric, as_of=None, period_type="quarter"):
    """Série d'un indicateur, telle qu'elle était connue à la date as_of."""
    as_of = as_of or FAR_FUTURE
    return conn.execute(
        _SELECT + "WHERE f.company_id = ? AND f.metric = ? AND f.period_type = ? "
        "AND f.known_at <= ? " + _LATEST + "ORDER BY f.period_end",
        (company_id, metric, period_type, as_of, as_of),
    ).fetchall()


def get_fact(conn, company_id, metric, period_end, as_of=None, period_type="quarter"):
    """Dernière version connue d'un chiffre pour une période, ou None."""
    as_of = as_of or FAR_FUTURE
    return conn.execute(
        _SELECT + "WHERE f.company_id = ? AND f.metric = ? AND f.period_end = ? "
        "AND f.period_type = ? AND f.known_at <= ? " + _LATEST,
        (company_id, metric, period_end, period_type, as_of, as_of),
    ).fetchone()


def fact_dict(row):
    """Forme publique d'un fait : la valeur ne voyage jamais sans sa source."""
    return {
        "id": row["id"],
        "metric": row["metric"],
        "period_start": row["period_start"] or None,
        "period_end": row["period_end"],
        "fiscal_year": row["fiscal_year"],
        "fiscal_period": row["fiscal_period"],
        "value": row["value"],
        "unit": row["unit"],
        "known_at": row["known_at"],
        "is_sample": bool(row["is_sample"]),
        "source": {
            "url": row["source_url"],
            "title": row["source_title"],
            "kind": row["source_kind"],
            "published_at": row["source_published_at"],
        },
    }
