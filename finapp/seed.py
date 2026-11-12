"""Charge le jeu d'exemple fourni avec le projet."""

import json
import os

from . import facts, promises, sec

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def load_json(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


# (symbole, fichier des comptes, fichier des prévisions ou None).
# NVDA : chiffres arrondis tirés de communiqués. ZBOR et ZQUE : sociétés
# entièrement inventées, pour montrer une perte, des capitaux propres
# négatifs et un exercice décalé.
SAMPLES = [
    ("NVDA", "nvda_companyfacts_sample.json", "nvda_guidance_sample.json"),
    ("ZBOR", "zbor_companyfacts_sample.json", "zbor_guidance_sample.json"),
    ("ZQUE", "zque_companyfacts_sample.json", None),
]


def seed(conn):
    """Charge les trois jeux d'exemple. Renvoie le nombre de faits ajoutés."""
    added = 0
    for ticker, facts_file, guidance_file in SAMPLES:
        added += sec.ingest(conn, load_json(facts_file), ticker, is_sample=True)
        if guidance_file:
            _seed_guidance(conn, ticker, guidance_file)
    conn.commit()
    return added


def _seed_guidance(conn, ticker, guidance_file):
    company_id = facts.get_company(conn, ticker)["id"]
    for g in load_json(guidance_file)["guidance"]:
        source_id = facts.add_source(
            conn, g["source_kind"], g["source_url"], g["source_title"], g["stated_at"])
        promises.add_promise(
            conn, company_id, g["metric"], g["period_end"], g["fiscal_label"],
            g["mid"], g["unit"], source_id, g["stated_at"],
            g.get("low"), g.get("high"), g.get("is_deduced", False))
