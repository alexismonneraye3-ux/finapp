"""Collecte des comptes publiés auprès du régulateur américain (SEC EDGAR).

L'interface « companyfacts » de la SEC est publique et gratuite. Elle exige
un en-tête User-Agent identifiant l'appelant (nom et adresse de contact) et
limite le débit à dix requêtes par seconde.
"""

import json
import urllib.request

from . import facts

COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK%s.json"

# Indicateur interne -> étiquettes comptables possibles, par ordre de préférence.
TAGS = {
    "revenue": [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
    ],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss"],
    "equity": ["StockholdersEquity"],
    "eps_diluted": ["EarningsPerShareDiluted"],
}


def pad_cik(cik):
    return str(int(cik)).zfill(10)


def fetch_companyfacts(cik, user_agent):
    """Télécharge le fichier companyfacts d'une société."""
    if not user_agent or "@" not in user_agent:
        raise ValueError(
            "La SEC exige un User-Agent avec une adresse de contact, "
            "par exemple « MonAppli contact@exemple.com »."
        )
    req = urllib.request.Request(
        COMPANYFACTS_URL % pad_cik(cik), headers={"User-Agent": user_agent}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def filing_url(cik, accession):
    return "https://www.sec.gov/Archives/edgar/data/%d/%s/" % (
        int(cik), accession.replace("-", ""))


def parse_companyfacts(doc):
    """Transforme un fichier companyfacts en lignes prêtes à stocker."""
    cik = doc.get("cik")
    gaap = doc.get("facts", {}).get("us-gaap", {})
    rows = []
    for metric, tags in TAGS.items():
        for tag in tags:
            for unit, entries in gaap.get(tag, {}).get("units", {}).items():
                for e in entries:
                    if "end" not in e or "val" not in e or "filed" not in e:
                        continue
                    accn = e.get("accn", "")
                    if not e.get("_url") and (cik is None or not accn):
                        continue  # sans document d'origine, pas de fait
                    rows.append({
                        "metric": metric,
                        "period_start": e.get("start", ""),
                        "period_end": e["end"],
                        "value": e["val"],
                        "unit": unit,
                        "fiscal_year": e.get("fy"),
                        "fiscal_period": e.get("fp"),
                        "known_at": e["filed"],
                        "form": e.get("form", ""),
                        "source_url": e.get("_url") or filing_url(cik, accn),
                    })
    return rows


def ingest(conn, doc, ticker, is_sample=False):
    """Charge un fichier companyfacts dans la base. Renvoie le nombre de faits ajoutés.

    Les étiquettes sont parcourues par ordre de préférence : si deux
    étiquettes donnent la même période à la même date, la première gagne.
    """
    company_id = facts.upsert_company(
        conn, ticker, doc.get("entityName", ticker), facts_cik(doc),
        is_fictional=bool(doc.get("_fictional")))
    added = 0
    for r in parse_companyfacts(doc):
        source_id = facts.add_source(
            conn, "sec_filing", r["source_url"],
            "%s déposé le %s" % (r["form"] or "Dépôt", r["known_at"]),
            r["known_at"])
        if facts.add_fact(
                conn, company_id, r["metric"], r["period_start"], r["period_end"],
                r["value"], r["unit"], source_id, r["known_at"],
                r["fiscal_year"], r["fiscal_period"], is_sample):
            added += 1
    conn.commit()
    return added


def facts_cik(doc):
    return pad_cik(doc["cik"]) if doc.get("cik") is not None else None
