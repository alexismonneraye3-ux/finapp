"""Signalements d'erreur : un lecteur dit qu'un chiffre lui paraît faux.

Un signalement ne corrige rien tout seul. Il stocke le fait visé, le
message et la date (01-donnees.md, section 8), pour qu'une personne le
traite.
"""

from datetime import datetime, timezone

MAX_MESSAGE = 1000
MAX_ABOUT = 200
OPEN = "ouvert"


class ReportError(ValueError):
    """Signalement refusé ; le message est destiné à l'utilisateur."""


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def add_report(conn, fact_id, message, about=None, now=None):
    """Enregistre un signalement et renvoie sa forme publique."""
    if isinstance(fact_id, bool) or not isinstance(fact_id, int):
        raise ReportError("Le chiffre visé est mal désigné.")
    if not isinstance(message, str) or not message.strip():
        raise ReportError("Le message est vide.")
    message = message.strip()
    if len(message) > MAX_MESSAGE:
        raise ReportError("Le message dépasse %d caractères." % MAX_MESSAGE)
    if about is not None and not isinstance(about, str):
        raise ReportError("La description du chiffre est mal formée.")
    about = (about or "").strip()[:MAX_ABOUT]
    if conn.execute("SELECT 1 FROM facts WHERE id = ?", (fact_id,)).fetchone() is None:
        raise KeyError("Chiffre inconnu : %s" % fact_id)
    created_at = now or _now()
    cur = conn.execute(
        "INSERT INTO error_reports (fact_id, about, message, created_at, status) "
        "VALUES (?, ?, ?, ?, ?)",
        (fact_id, about, message, created_at, OPEN))
    conn.commit()
    return {"id": cur.lastrowid, "fact_id": fact_id, "created_at": created_at,
            "status": OPEN}


def list_reports(conn, status=None):
    """Signalements, du plus récent au plus ancien, avec le chiffre visé."""
    sql = ("SELECT r.*, c.ticker, f.metric, f.period_end, f.value, f.unit, "
           "s.url AS source_url "
           "FROM error_reports r JOIN facts f ON f.id = r.fact_id "
           "JOIN companies c ON c.id = f.company_id "
           "JOIN sources s ON s.id = f.source_id ")
    args = ()
    if status is not None:
        sql += "WHERE r.status = ? "
        args = (status,)
    return [dict(r) for r in conn.execute(sql + "ORDER BY r.created_at DESC, r.id DESC", args)]
