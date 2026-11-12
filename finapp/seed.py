"""Charge le jeu d'exemple fourni avec le projet."""

import json
import os

from . import facts, promises, sec

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def load_json(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


def seed(conn):
    """Charge l'exemple Nvidia : chiffres d'affaires publiés et prévisions annoncées."""
    doc = load_json("nvda_companyfacts_sample.json")
    added = sec.ingest(conn, doc, "NVDA", is_sample=True)

    company_id = facts.get_company(conn, "NVDA")["id"]
    for g in load_json("nvda_guidance_sample.json")["guidance"]:
        source_id = facts.add_source(
            conn, g["source_kind"], g["source_url"], g["source_title"], g["stated_at"])
        promises.add_promise(
            conn, company_id, g["metric"], g["period_end"], g["fiscal_label"],
            g["mid"], g["unit"], source_id, g["stated_at"],
            g.get("low"), g.get("high"), g.get("is_deduced", False))
    conn.commit()
    return added
