"""Connexion et schéma de la base de faits (SQLite)."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
    id      INTEGER PRIMARY KEY,
    ticker  TEXT NOT NULL UNIQUE,
    name    TEXT NOT NULL,
    cik     TEXT
);

-- Un document d'origine : dépôt réglementaire, communiqué, article.
CREATE TABLE IF NOT EXISTS sources (
    id            INTEGER PRIMARY KEY,
    kind          TEXT NOT NULL,          -- 'sec_filing', 'press_release', 'article'
    url           TEXT NOT NULL UNIQUE,
    title         TEXT NOT NULL,
    published_at  TEXT                    -- AAAA-MM-JJ
);

-- Un chiffre publié. Une même période peut avoir plusieurs versions
-- (chiffre révisé plus tard) : on ne remplace jamais, on ajoute, et
-- known_at dit à partir de quand cette version était connue.
CREATE TABLE IF NOT EXISTS facts (
    id             INTEGER PRIMARY KEY,
    company_id     INTEGER NOT NULL REFERENCES companies(id),
    metric         TEXT NOT NULL,         -- 'revenue', 'net_income', ...
    period_start   TEXT NOT NULL DEFAULT '',  -- '' pour une valeur à une date
    period_end     TEXT NOT NULL,
    period_type    TEXT NOT NULL,         -- 'quarter', 'year', 'instant', 'other'
    fiscal_year    INTEGER,
    fiscal_period  TEXT,                  -- 'Q1'..'Q4', 'FY'
    value          REAL NOT NULL,
    unit           TEXT NOT NULL,
    source_id      INTEGER NOT NULL REFERENCES sources(id),
    known_at       TEXT NOT NULL,         -- date de publication de cette version
    is_sample      INTEGER NOT NULL DEFAULT 0,  -- 1 = donnée d'exemple arrondie
    UNIQUE (company_id, metric, period_start, period_end, known_at)
);
CREATE INDEX IF NOT EXISTS facts_lookup
    ON facts (company_id, metric, period_end, known_at);

-- Un engagement chiffré de la direction pour une période à venir.
CREATE TABLE IF NOT EXISTS promises (
    id             INTEGER PRIMARY KEY,
    company_id     INTEGER NOT NULL REFERENCES companies(id),
    metric         TEXT NOT NULL,
    period_end     TEXT NOT NULL,         -- fin de la période visée
    fiscal_label   TEXT NOT NULL,
    low            REAL,                  -- bas de fourchette, si donné
    mid            REAL NOT NULL,         -- valeur centrale annoncée
    high           REAL,                  -- haut de fourchette, si donné
    unit           TEXT NOT NULL,
    source_id      INTEGER NOT NULL REFERENCES sources(id),
    stated_at      TEXT NOT NULL,         -- date de l'annonce
    is_deduced     INTEGER NOT NULL DEFAULT 0,  -- 1 = reconstituée, pas lue à la source
    UNIQUE (company_id, metric, period_end, stated_at)
);

-- Un lecteur signale qu'un chiffre lui paraît faux. Rien n'est corrigé
-- automatiquement : une personne traite le signalement.
CREATE TABLE IF NOT EXISTS error_reports (
    id          INTEGER PRIMARY KEY,
    fact_id     INTEGER NOT NULL REFERENCES facts(id),
    about       TEXT NOT NULL DEFAULT '',   -- ce que l'écran affichait
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL,              -- AAAA-MM-JJTHH:MM:SSZ (UTC)
    status      TEXT NOT NULL DEFAULT 'ouvert'
);
"""


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init(conn):
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
