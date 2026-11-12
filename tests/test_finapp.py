import json
import os
import tempfile
import unittest

from finapp import api, calc, db, facts, promises, sec, seed, views
from finapp.__main__ import export_demo


def fresh():
    return db.init(db.connect())


class PointInTime(unittest.TestCase):
    """Un chiffre révisé ne remplace pas l'ancien : on sait ce qui était connu quand."""

    def setUp(self):
        self.conn = fresh()
        self.cid = facts.upsert_company(self.conn, "abc", "ABC SA")
        s1 = facts.add_source(self.conn, "sec_filing", "https://ex.test/1", "10-Q", "2026-05-01")
        s2 = facts.add_source(self.conn, "sec_filing", "https://ex.test/2", "10-Q/A", "2026-06-15")
        facts.add_fact(self.conn, self.cid, "revenue", "2026-01-01", "2026-03-31",
                       100, "USD", s1, "2026-05-01")
        facts.add_fact(self.conn, self.cid, "revenue", "2026-01-01", "2026-03-31",
                       90, "USD", s2, "2026-06-15")

    def get(self, as_of=None):
        return facts.get_fact(self.conn, self.cid, "revenue", "2026-03-31", as_of)

    def test_before_publication_nothing_is_known(self):
        self.assertIsNone(self.get("2026-04-30"))

    def test_original_value_before_restatement(self):
        self.assertEqual(self.get("2026-06-14")["value"], 100)

    def test_restated_value_afterwards(self):
        self.assertEqual(self.get("2026-06-15")["value"], 90)
        self.assertEqual(self.get()["value"], 90)

    def test_series_has_one_row_per_period(self):
        rows = facts.series(self.conn, self.cid, "revenue")
        self.assertEqual([r["value"] for r in rows], [90])

    def test_same_version_is_not_added_twice(self):
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/1", "10-Q")
        self.assertFalse(facts.add_fact(self.conn, self.cid, "revenue", "2026-01-01",
                                        "2026-03-31", 100, "USD", s, "2026-05-01"))

    def test_ticker_is_case_insensitive(self):
        self.assertEqual(facts.get_company(self.conn, "ABC")["id"], self.cid)

    def test_fact_always_carries_its_source(self):
        d = facts.fact_dict(self.get())
        self.assertEqual(d["source"]["url"], "https://ex.test/2")
        self.assertEqual(d["known_at"], "2026-06-15")


class PeriodType(unittest.TestCase):
    def test_classification(self):
        self.assertEqual(facts.period_type("2026-01-26", "2026-04-26"), "quarter")
        self.assertEqual(facts.period_type("2025-01-27", "2026-01-25"), "year")
        self.assertEqual(facts.period_type("", "2026-01-25"), "instant")
        self.assertEqual(facts.period_type("2026-01-01", "2026-06-30"), "other")


class SecParsing(unittest.TestCase):
    DOC = {
        "cik": 1234, "entityName": "Test Corp",
        "facts": {"us-gaap": {
            "Revenues": {"units": {"USD": [
                {"start": "2026-01-01", "end": "2026-03-31", "val": 500, "fy": 2026,
                 "fp": "Q1", "form": "10-Q", "filed": "2026-05-01",
                 "accn": "0000001234-26-000001"},
                {"start": "2025-01-01", "end": "2025-12-31", "val": 1800, "fy": 2025,
                 "fp": "FY", "form": "10-K", "filed": "2026-02-20",
                 "accn": "0000001234-26-000000"},
            ]}},
            "SalesRevenueNet": {"units": {"USD": [
                {"start": "2026-01-01", "end": "2026-03-31", "val": 499, "fy": 2026,
                 "fp": "Q1", "form": "10-Q", "filed": "2026-05-01",
                 "accn": "0000001234-26-000001"},
            ]}},
            "NetIncomeLoss": {"units": {"USD": [
                {"start": "2026-01-01", "end": "2026-03-31", "val": 50, "fy": 2026,
                 "fp": "Q1", "form": "10-Q", "filed": "2026-05-01",
                 "accn": "0000001234-26-000001"},
                {"end": "2026-03-31", "val": 1},
            ]}},
        }},
    }

    def test_filing_url(self):
        self.assertEqual(
            sec.filing_url(1234, "0000001234-26-000001"),
            "https://www.sec.gov/Archives/edgar/data/1234/000000123426000001/")

    def test_incomplete_entries_are_skipped(self):
        rows = sec.parse_companyfacts(self.DOC)
        self.assertEqual(len([r for r in rows if r["metric"] == "net_income"]), 1)

    def test_ingest_prefers_first_tag_and_separates_quarter_from_year(self):
        conn = fresh()
        sec.ingest(conn, self.DOC, "TST")
        cid = facts.get_company(conn, "TST")["id"]
        quarters = facts.series(conn, cid, "revenue")
        self.assertEqual([r["value"] for r in quarters], [500])
        years = facts.series(conn, cid, "revenue", period_type="year")
        self.assertEqual([r["value"] for r in years], [1800])

    def test_ingest_twice_adds_nothing(self):
        conn = fresh()
        sec.ingest(conn, self.DOC, "TST")
        self.assertEqual(sec.ingest(conn, self.DOC, "TST"), 0)

    def test_margin_from_ingested_facts(self):
        conn = fresh()
        sec.ingest(conn, self.DOC, "TST")
        cid = facts.get_company(conn, "TST")["id"]
        ni = facts.get_fact(conn, cid, "net_income", "2026-03-31")
        rev = facts.get_fact(conn, cid, "revenue", "2026-03-31")
        m = calc.margin(ni, rev)
        self.assertAlmostEqual(m["value"], 10.0)
        self.assertEqual(m["input_fact_ids"], [ni["id"], rev["id"]])

    def test_user_agent_is_required(self):
        with self.assertRaises(ValueError):
            sec.fetch_companyfacts(1234, "")


class Calc(unittest.TestCase):
    def test_growth_handles_zero_and_missing(self):
        cur = {"id": 2, "value": 10, "unit": "USD"}
        self.assertIsNone(calc.growth(cur, None))
        self.assertIsNone(calc.growth(cur, {"id": 1, "value": 0, "unit": "USD"}))
        self.assertIsNone(calc.growth(cur, {"id": 1, "value": 5, "unit": "EUR"}))

    def test_growth_from_negative_base(self):
        g = calc.growth({"id": 2, "value": 50, "unit": "USD"},
                        {"id": 1, "value": -100, "unit": "USD"})
        self.assertAlmostEqual(g["value"], 150.0)

    def test_status(self):
        self.assertEqual(promises.status(None, 9, 10, 11), promises.PENDING)
        self.assertEqual(promises.status(12, 9, 10, 11), promises.BEAT)
        self.assertEqual(promises.status(11, 9, 10, 11), promises.MET)
        self.assertEqual(promises.status(8.9, 9, 10, 11), promises.MISSED)
        self.assertEqual(promises.status(10, None, 10, None), promises.MET)
        self.assertEqual(promises.status(9.9, None, 10, None), promises.MISSED)


class YearOverYearCalc(unittest.TestCase):
    """Variation sur un an et croissance annuelle moyenne (02-calculs.md, sections 2 et 10)."""

    @staticmethod
    def f(fid, value, start="", end="2026-03-31", unit="USD"):
        return {"id": fid, "value": value, "unit": unit,
                "period_start": start, "period_end": end}

    def q(self, fid, value, start, end):
        return self.f(fid, value, start, end)

    def test_normal_case_checked_by_hand(self):
        g = calc.year_over_year(self.f(1, 150), self.f(2, 120))
        self.assertAlmostEqual(g["value"], 25.0)
        self.assertEqual((g["unit"], g["name"]), ("%", "variation sur un an"))

    def test_formula_and_inputs_are_returned(self):
        g = calc.year_over_year(self.f(1, 150), self.f(2, 120))
        self.assertEqual(g["formula"], "(150 − 120) ÷ 120 × 100")
        self.assertEqual(g["input_fact_ids"], [1, 2])

    def test_missing_input(self):
        self.assertIsNone(calc.year_over_year(self.f(1, 150), None))

    def test_division_by_zero(self):
        self.assertIsNone(calc.year_over_year(self.f(1, 150), self.f(2, 0)))

    def test_negative_base_uses_absolute_value(self):
        """De −100 à 50 : (50 − (−100)) ÷ |−100| × 100 = +150 %."""
        g = calc.year_over_year(self.f(1, 50), self.f(2, -100))
        self.assertAlmostEqual(g["value"], 150.0)

    def test_different_units(self):
        self.assertIsNone(calc.year_over_year(self.f(1, 150), self.f(2, 120, unit="EUR")))

    def test_finds_same_quarter_a_year_earlier(self):
        rows = [self.q(1, 100, "2025-01-01", "2025-03-31"),
                self.q(2, 110, "2025-04-01", "2025-06-30"),
                self.q(3, 120, "2025-10-01", "2025-12-31"),
                self.q(4, 130, "2026-01-01", "2026-03-31")]
        self.assertEqual(calc.same_period_last_year(rows, rows[3])["id"], 1)

    def test_no_match_when_that_quarter_is_missing(self):
        """Jamais de comparaison avec un autre trimestre que celui d'il y a un an."""
        rows = [self.q(2, 110, "2025-04-01", "2025-06-30"),
                self.q(4, 130, "2026-01-01", "2026-03-31")]
        self.assertIsNone(calc.same_period_last_year(rows, rows[1]))
        self.assertIsNone(calc.same_period_last_year(rows, rows[0]))

    def test_tolerates_52_and_53_week_years(self):
        """Fins de trimestre décalées de quelques jours d'une année à l'autre."""
        rows = [self.q(1, 100, "2025-01-27", "2025-04-27"),
                self.q(2, 130, "2026-01-26", "2026-04-26")]
        self.assertEqual(calc.same_period_last_year(rows, rows[1])["id"], 1)

    def test_a_full_year_is_not_matched_with_a_quarter(self):
        rows = [self.q(1, 400, "2024-04-01", "2025-03-31"),
                self.q(2, 130, "2026-01-01", "2026-03-31")]
        self.assertIsNone(calc.same_period_last_year(rows, rows[1]))

    def test_instant_value_has_no_year_ago_period(self):
        rows = [self.f(1, 100, "", "2025-03-31"), self.f(2, 130, "", "2026-03-31")]
        self.assertIsNone(calc.same_period_last_year(rows, rows[1]))

    def test_cagr_normal_case_checked_by_hand(self):
        """De 100 à 121 en 2 ans : +10 % par an."""
        c = calc.cagr(self.f(1, 121), self.f(2, 100), 2)
        self.assertAlmostEqual(c["value"], 10.0)
        self.assertEqual((c["unit"], c["name"]), ("%", "croissance annuelle moyenne"))

    def test_cagr_formula_and_inputs_are_returned(self):
        c = calc.cagr(self.f(1, 121), self.f(2, 100), 2)
        self.assertEqual(c["formula"], "((121 ÷ 100)^(1/2) − 1) × 100")
        self.assertEqual(c["input_fact_ids"], [1, 2])

    def test_cagr_decline(self):
        """De 100 à 25 en 2 ans : −50 % par an."""
        self.assertAlmostEqual(calc.cagr(self.f(1, 25), self.f(2, 100), 2)["value"], -50.0)

    def test_cagr_over_one_year_equals_simple_growth(self):
        self.assertAlmostEqual(calc.cagr(self.f(1, 150), self.f(2, 120), 1)["value"], 25.0)

    def test_cagr_missing_input(self):
        self.assertIsNone(calc.cagr(None, self.f(2, 100), 2))
        self.assertIsNone(calc.cagr(self.f(1, 121), None, 2))

    def test_cagr_zero_or_negative_start_or_end(self):
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, 0), 2))
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, -100), 2))
        self.assertIsNone(calc.cagr(self.f(1, -5), self.f(2, 100), 2))
        self.assertIsNone(calc.cagr(self.f(1, 0), self.f(2, 100), 2))

    def test_cagr_needs_at_least_one_year(self):
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, 100), 0))
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, 100), -3))
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, 100), None))

    def test_cagr_different_units(self):
        self.assertIsNone(calc.cagr(self.f(1, 121), self.f(2, 100, unit="EUR"), 2))


class YearOverYearInView(unittest.TestCase):
    """Variation sur un an par trimestre dans la fiche. Chiffres inventés pour le test."""

    QUARTERS = [("2025-01-01", "2025-03-31", 100, "2025-05-01"),
                ("2025-04-01", "2025-06-30", 110, "2025-08-01"),
                ("2025-07-01", "2025-09-30", 120, "2025-11-01"),
                ("2025-10-01", "2025-12-31", 125, "2026-02-01"),
                ("2026-01-01", "2026-03-31", 130, "2026-05-01")]

    def setUp(self):
        self.conn = fresh()
        self.cid = facts.upsert_company(self.conn, "tst", "Test SA")
        for start, end, value, known in self.QUARTERS:
            s = facts.add_source(self.conn, "sec_filing", "https://ex.test/" + end, "10-Q " + end, known)
            facts.add_fact(self.conn, self.cid, "revenue", start, end, value, "USD", s, known)

    def revenue(self, as_of=None):
        return views.company_view(self.conn, "TST", as_of)["revenue"]

    def test_only_the_fifth_quarter_has_a_year_ago(self):
        rev = self.revenue()
        self.assertEqual([r["growth_year"] is None for r in rev], [True] * 4 + [False])
        self.assertAlmostEqual(rev[4]["growth_year"]["value"], 30.0)

    def test_quarter_on_quarter_growth_is_unchanged(self):
        self.assertAlmostEqual(self.revenue()[4]["growth"]["value"], 4.0)

    def test_carries_both_facts_and_sources(self):
        last = self.revenue()[4]
        self.assertEqual(last["growth_year"]["input_fact_ids"], [last["id"], last["year_ago"]["id"]])
        self.assertEqual(last["year_ago"]["source"]["url"], "https://ex.test/2025-03-31")
        self.assertEqual(last["year_ago"]["known_at"], "2025-05-01")
        self.assertIsNone(self.revenue()[0]["year_ago"])

    def test_as_of_uses_the_version_known_then(self):
        """Le trimestre d'il y a un an est révisé après coup : la variation suit la date choisie."""
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/rev", "10-Q/A")
        facts.add_fact(self.conn, self.cid, "revenue", "2025-01-01", "2025-03-31",
                       104, "USD", s, "2026-06-01")
        self.assertAlmostEqual(self.revenue("2026-05-15")[4]["growth_year"]["value"], 30.0)
        self.assertAlmostEqual(self.revenue()[4]["growth_year"]["value"], 25.0)

    def test_api_and_demo_page_include_it(self):
        body = api.route(self.conn, "/api/company/tst", {})[1]
        self.assertAlmostEqual(body["revenue"][4]["growth_year"]["value"], 30.0)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "demo.html")
            export_demo(self.conn, out)
            with open(out, encoding="utf-8") as fh:
                html = fh.read()
        self.assertIn("Var. sur un an", html)
        self.assertIn('"growth_year"', html)


class MarginCalc(unittest.TestCase):
    """Cas attendus par docs/specifications/02-calculs.md, section 10."""

    @staticmethod
    def f(fid, value, unit="USD"):
        return {"id": fid, "value": value, "unit": unit}

    def test_normal_case_checked_by_hand(self):
        m = calc.margin(self.f(1, 45), self.f(2, 200), "marge nette")
        self.assertAlmostEqual(m["value"], 22.5)
        self.assertEqual(m["unit"], "%")
        self.assertEqual(m["name"], "marge nette")

    def test_formula_and_inputs_are_returned(self):
        m = calc.margin(self.f(1, 45), self.f(2, 200))
        self.assertEqual(m["formula"], "45 ÷ 200 × 100")
        self.assertEqual(m["input_fact_ids"], [1, 2])
        self.assertEqual(m["name"], "marge")

    def test_missing_input(self):
        self.assertIsNone(calc.margin(None, self.f(2, 200)))
        self.assertIsNone(calc.margin(self.f(1, 45), None))
        self.assertEqual(calc.margin_reason(None, self.f(2, 200)), "non disponible")

    def test_division_by_zero(self):
        self.assertIsNone(calc.margin(self.f(1, 45), self.f(2, 0)))
        self.assertEqual(calc.margin_reason(self.f(1, 45), self.f(2, 0)), "non disponible")

    def test_negative_numerator_gives_negative_margin(self):
        m = calc.margin(self.f(1, -30), self.f(2, 200))
        self.assertAlmostEqual(m["value"], -15.0)

    def test_negative_denominator_is_not_meaningful(self):
        self.assertIsNone(calc.margin(self.f(1, 45), self.f(2, -200)))
        self.assertEqual(calc.margin_reason(self.f(1, 45), self.f(2, -200)), "non significatif")

    def test_different_units(self):
        self.assertIsNone(calc.margin(self.f(1, 45, "EUR"), self.f(2, 200)))
        self.assertEqual(calc.margin_reason(self.f(1, 45, "EUR"), self.f(2, 200)), "non disponible")

    def test_reason_is_none_when_computable(self):
        self.assertIsNone(calc.margin_reason(self.f(1, 45), self.f(2, 200)))


class MarginsInView(unittest.TestCase):
    """Marges par trimestre dans la fiche. Société et chiffres inventés pour le test."""

    Q1 = ("2026-01-01", "2026-03-31")
    Q2 = ("2026-04-01", "2026-06-30")

    def setUp(self):
        self.conn = fresh()
        self.cid = facts.upsert_company(self.conn, "tst", "Test SA")
        self.s1 = facts.add_source(self.conn, "sec_filing", "https://ex.test/q1", "10-Q T1", "2026-05-01")
        self.s2 = facts.add_source(self.conn, "sec_filing", "https://ex.test/q2", "10-Q T2", "2026-08-01")
        self.add("revenue", self.Q1, 200, self.s1, "2026-05-01")
        self.add("gross_profit", self.Q1, 120, self.s1, "2026-05-01")
        self.add("operating_income", self.Q1, 50, self.s1, "2026-05-01")
        self.add("net_income", self.Q1, -30, self.s1, "2026-05-01")
        self.add("revenue", self.Q2, 250, self.s2, "2026-08-01")
        self.add("gross_profit", self.Q2, 150, self.s2, "2026-08-01")

    def add(self, metric, period, value, source, known_at, **kw):
        facts.add_fact(self.conn, self.cid, metric, period[0], period[1], value,
                       "USD", source, known_at, **kw)

    def view(self, as_of=None):
        return views.company_view(self.conn, "TST", as_of)

    def test_three_margins_per_quarter(self):
        q1, q2 = self.view()["margins"]
        self.assertAlmostEqual(q1["gross"]["result"]["value"], 60.0)
        self.assertAlmostEqual(q1["operating"]["result"]["value"], 25.0)
        self.assertAlmostEqual(q1["net"]["result"]["value"], -15.0)
        self.assertAlmostEqual(q2["gross"]["result"]["value"], 60.0)
        self.assertEqual(q1["gross"]["result"]["name"], "marge brute")
        self.assertEqual(q1["net"]["result"]["formula"], "-30 ÷ 200 × 100")

    def test_missing_fact_is_not_available_never_zero(self):
        q2 = self.view()["margins"][1]
        for key in ("operating", "net"):
            self.assertIsNone(q2[key]["result"])
            self.assertEqual(q2[key]["reason"], "non disponible")
            self.assertIsNone(q2[key]["numerator"])

    def test_each_margin_carries_both_sources(self):
        q1 = self.view()["margins"][0]
        m = q1["gross"]
        self.assertEqual(m["numerator"]["source"]["url"], "https://ex.test/q1")
        self.assertEqual(q1["revenue"]["source"]["url"], "https://ex.test/q1")
        self.assertEqual(m["result"]["input_fact_ids"],
                         [m["numerator"]["id"], q1["revenue"]["id"]])
        self.assertIsNone(m["reason"])

    def test_as_of_uses_only_what_was_known(self):
        lines = self.view("2026-06-01")["margins"]
        self.assertEqual(len(lines), 1)
        s3 = facts.add_source(self.conn, "sec_filing", "https://ex.test/q1a", "10-Q/A", "2026-09-01")
        self.add("gross_profit", self.Q1, 100, s3, "2026-09-01")
        self.assertAlmostEqual(self.view("2026-08-15")["margins"][0]["gross"]["result"]["value"], 60.0)
        latest = self.view()["margins"][0]["gross"]
        self.assertAlmostEqual(latest["result"]["value"], 50.0)
        self.assertEqual(latest["numerator"]["source"]["url"], "https://ex.test/q1a")

    def test_negative_revenue_is_not_meaningful(self):
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/q3", "10-Q T3", "2026-11-01")
        q3 = ("2026-07-01", "2026-09-30")
        self.add("revenue", q3, -10, s, "2026-11-01")
        self.add("net_income", q3, 5, s, "2026-11-01")
        net = self.view()["margins"][2]["net"]
        self.assertIsNone(net["result"])
        self.assertEqual(net["reason"], "non significatif")

    def test_period_must_match_exactly(self):
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/q3", "10-Q T3", "2026-11-01")
        self.add("revenue", ("2026-07-01", "2026-09-30"), 300, s, "2026-11-01")
        self.add("net_income", ("2026-06-25", "2026-09-30"), 60, s, "2026-11-01")
        net = self.view()["margins"][2]["net"]
        self.assertIsNone(net["result"])
        self.assertEqual(net["reason"], "non disponible")

    def test_sample_numerator_flags_the_view(self):
        self.assertFalse(self.view()["has_sample_data"])
        self.add("operating_income", self.Q2, 70, self.s2, "2026-08-01", is_sample=True)
        self.assertTrue(self.view()["has_sample_data"])

    def test_api_and_demo_page_include_margins(self):
        code, body = api.route(self.conn, "/api/company/TST", {})
        self.assertEqual(code, 200)
        self.assertEqual(len(body["margins"]), 2)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "demo.html")
            export_demo(self.conn, out)
            with open(out, encoding="utf-8") as fh:
                html = fh.read()
        self.assertIn('"margins"', html)
        self.assertIn("Marges par trimestre", html)
        self.assertIn("marginInfo", html)


class AnnualRevenue(unittest.TestCase):
    """Chiffre d'affaires par exercice. Société et chiffres inventés pour le test."""

    Y1 = ("2023-01-01", "2023-12-31")
    Y2 = ("2024-01-01", "2024-12-31")
    Y3 = ("2025-01-01", "2025-12-31")

    def setUp(self):
        self.conn = fresh()
        self.cid = facts.upsert_company(self.conn, "tst", "Test SA")
        self.s1 = facts.add_source(self.conn, "sec_filing", "https://ex.test/k23", "10-K 2023", "2024-02-15")
        self.s2 = facts.add_source(self.conn, "sec_filing", "https://ex.test/k24", "10-K 2024", "2025-02-15")
        self.add(self.Y1, 400, self.s1, "2024-02-15")
        self.add(self.Y2, 500, self.s2, "2025-02-15")

    def add(self, period, value, source, known_at, **kw):
        facts.add_fact(self.conn, self.cid, "revenue", period[0], period[1], value,
                       "USD", source, known_at, **kw)

    def annual(self, as_of=None):
        return views.company_view(self.conn, "TST", as_of)["revenue_annual"]

    def test_one_line_per_year_with_growth(self):
        y1, y2 = self.annual()
        self.assertEqual((y1["value"], y2["value"]), (400, 500))
        self.assertIsNone(y1["growth"])
        self.assertAlmostEqual(y2["growth"]["value"], 25.0)
        self.assertEqual(y2["growth"]["formula"], "(500 − 400) ÷ 400 × 100")

    def test_growth_carries_both_facts_and_sources(self):
        y2 = self.annual()[1]
        self.assertEqual(y2["growth"]["input_fact_ids"], [y2["id"], y2["previous"]["id"]])
        self.assertEqual(y2["source"]["url"], "https://ex.test/k24")
        self.assertEqual(y2["previous"]["source"]["url"], "https://ex.test/k23")
        self.assertEqual(y2["previous"]["known_at"], "2024-02-15")

    def test_first_year_has_no_previous(self):
        self.assertIsNone(self.annual()[0]["previous"])

    def test_label_comes_from_closing_date(self):
        self.assertEqual(self.annual()[1]["fiscal_label"],
                         "Exercice clos le 31 décembre 2024")

    def test_missing_year_gives_no_growth(self):
        """Un trou dans la série : pas de comparaison avec un exercice plus ancien."""
        conn = fresh()
        cid = facts.upsert_company(conn, "tst", "Test SA")
        s = facts.add_source(conn, "sec_filing", "https://ex.test/k", "10-K")
        facts.add_fact(conn, cid, "revenue", *self.Y1, 400, "USD", s, "2024-02-15")
        facts.add_fact(conn, cid, "revenue", *self.Y3, 700, "USD", s, "2026-02-15")
        y1, y3 = views.company_view(conn, "TST")["revenue_annual"]
        self.assertIsNone(y3["growth"])
        self.assertIsNone(y3["previous"])

    def test_zero_previous_year_gives_no_growth(self):
        self.add(self.Y3, 700, self.s2, "2026-02-15")
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/k24a", "10-K/A")
        self.add(self.Y2, 0, s, "2026-02-15")
        self.assertIsNone(self.annual()[2]["growth"])

    def test_decline_is_negative(self):
        self.add(self.Y3, 450, self.s2, "2026-02-15")
        self.assertAlmostEqual(self.annual()[2]["growth"]["value"], -10.0)

    def test_as_of_uses_only_what_was_known(self):
        """Exercice 2023 révisé plus tard : avant la révision, on voit l'ancien chiffre."""
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/k23a", "10-K/A 2023")
        self.add(self.Y1, 320, s, "2025-06-01")
        self.assertEqual(len(self.annual("2024-12-31")), 1)
        self.assertAlmostEqual(self.annual("2025-03-01")[1]["growth"]["value"], 25.0)
        after = self.annual()[1]
        self.assertAlmostEqual(after["growth"]["value"], 56.25)
        self.assertEqual(after["previous"]["source"]["url"], "https://ex.test/k23a")

    def test_quarters_and_years_do_not_mix(self):
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/q", "10-Q")
        facts.add_fact(self.conn, self.cid, "revenue", "2025-01-01", "2025-03-31",
                       130, "USD", s, "2025-05-01")
        view = views.company_view(self.conn, "TST")
        self.assertEqual([f["value"] for f in view["revenue_annual"]], [400, 500])
        self.assertEqual([f["value"] for f in view["revenue"]], [130])

    def test_sample_year_flags_the_view(self):
        self.assertFalse(views.company_view(self.conn, "TST")["has_sample_data"])
        self.add(self.Y3, 700, self.s2, "2026-02-15", is_sample=True)
        self.assertTrue(views.company_view(self.conn, "TST")["has_sample_data"])

    def test_sec_fiscal_year_of_the_filing_does_not_mislabel(self):
        """Format SEC : un rapport annuel rappelle l'exercice précédent avec son
        propre millésime (fy). Le libellé doit suivre la date de clôture."""
        doc = {"cik": 999, "entityName": "Inventée SA", "facts": {"us-gaap": {"Revenues": {"units": {"USD": [
            {"start": "2023-01-01", "end": "2023-12-31", "val": 400, "fy": 2023,
             "fp": "FY", "form": "10-K", "filed": "2024-02-15", "accn": "0000000999-24-000001"},
            {"start": "2023-01-01", "end": "2023-12-31", "val": 400, "fy": 2024,
             "fp": "FY", "form": "10-K", "filed": "2025-02-15", "accn": "0000000999-25-000001"},
            {"start": "2024-01-01", "end": "2024-12-31", "val": 500, "fy": 2024,
             "fp": "FY", "form": "10-K", "filed": "2025-02-15", "accn": "0000000999-25-000001"},
        ]}}}}}
        conn = fresh()
        sec.ingest(conn, doc, "INV")
        y1, y2 = views.company_view(conn, "INV")["revenue_annual"]
        self.assertEqual(y1["fiscal_label"], "Exercice clos le 31 décembre 2023")
        self.assertEqual(y2["fiscal_label"], "Exercice clos le 31 décembre 2024")
        self.assertAlmostEqual(y2["growth"]["value"], 25.0)

    def test_api_and_demo_page_include_annual_revenue(self):
        code, body = api.route(self.conn, "/api/company/tst", {})
        self.assertEqual(code, 200)
        self.assertAlmostEqual(body["revenue_annual"][1]["growth"]["value"], 25.0)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "demo.html")
            export_demo(self.conn, out)
            html = open(out, encoding="utf-8").read()
        self.assertIn("Chiffre d\\'affaires annuel", html)
        self.assertIn('"revenue_annual"', html)


class NvidiaExample(unittest.TestCase):
    """Le jeu d'exemple doit redonner les écarts calculés à la main dans l'étude."""

    def setUp(self):
        self.conn = fresh()
        seed.seed(self.conn)

    def view(self, as_of=None):
        return views.company_view(self.conn, "NVDA", as_of)

    def test_gaps_match_hand_calculation(self):
        items = {i["fiscal_label"]: i for i in self.view()["promises"]["items"]}
        self.assertAlmostEqual(items["T4 exercice 2026"]["gap_pct"], 4.8, places=1)
        self.assertAlmostEqual(items["T1 exercice 2027"]["gap_pct"], 4.6, places=1)
        self.assertAlmostEqual(items["T2 exercice 2027"]["gap_pct"], 5.7, places=1)
        self.assertEqual(items["T2 exercice 2027"]["status"], promises.BEAT)
        self.assertEqual(items["T3 exercice 2027"]["status"], promises.PENDING)
        self.assertTrue(items["T4 exercice 2026"]["is_deduced"])

    def test_profile(self):
        p = self.view()["promises"]["profile"]
        self.assertEqual((p["evaluated"], p["pending"], p["kept"]), (3, 1, 3))
        self.assertAlmostEqual(p["mean_gap_pct"], 5.0, places=1)
        self.assertEqual(self.view()["promises"]["unusual"], [])

    def test_growth_between_consecutive_quarters(self):
        rev = self.view()["revenue"]
        self.assertIsNone(rev[0]["growth"])
        self.assertAlmostEqual(rev[1]["growth"]["value"], 19.8, places=1)
        self.assertAlmostEqual(rev[2]["growth"]["value"], 17.9, places=1)

    def test_view_as_of_a_past_date(self):
        v = self.view("2026-06-01")
        self.assertEqual(len(v["revenue"]), 2)
        labels = {i["fiscal_label"]: i["status"] for i in v["promises"]["items"]}
        self.assertEqual(labels["T2 exercice 2027"], promises.PENDING)
        self.assertNotIn("T3 exercice 2027", labels)

    def test_sample_data_is_flagged(self):
        self.assertTrue(self.view()["has_sample_data"])

    def test_unusual_flags_a_break_in_habit(self):
        cid = facts.get_company(self.conn, "NVDA")["id"]
        s = facts.add_source(self.conn, "sec_filing", "https://ex.test/q3", "8-K")
        facts.add_fact(self.conn, cid, "revenue", "2026-07-27", "2026-10-25",
                       109.0e9, "USD", s, "2026-11-19", 2027, "Q3")
        flagged = self.view()["promises"]["unusual"]
        self.assertEqual([f["fiscal_label"] for f in flagged], ["T3 exercice 2027"])

    def test_no_year_over_year_with_three_quarters(self):
        """Le jeu d'exemple n'a que trois trimestres : aucune variation sur un an."""
        for item in self.view()["revenue"]:
            self.assertIsNone(item["growth_year"])

    def test_no_annual_revenue_without_published_year(self):
        """Le jeu d'exemple n'a que des trimestres : aucun chiffre annuel inventé."""
        self.assertEqual(self.view()["revenue_annual"], [])

    def test_margins_not_available_without_published_inputs(self):
        """Le jeu d'exemple n'a que le chiffre d'affaires : aucune marge inventée."""
        lines = views.company_view(self.conn, "NVDA")["margins"]
        self.assertTrue(lines)
        for line in lines:
            for key in ("gross", "operating", "net"):
                self.assertIsNone(line[key]["result"])
                self.assertEqual(line[key]["reason"], "non disponible")


class Api(unittest.TestCase):
    def setUp(self):
        self.conn = fresh()
        seed.seed(self.conn)

    def test_routes(self):
        self.assertEqual(api.route(self.conn, "/api/companies", {})[1],
                         [{"ticker": "NVDA", "name": "NVIDIA Corporation"}])
        code, body = api.route(self.conn, "/api/company/nvda", {})
        self.assertEqual((code, body["company"]["ticker"]), (200, "NVDA"))
        self.assertEqual(api.route(self.conn, "/api/company/ZZZ", {})[0], 404)
        self.assertEqual(api.route(self.conn, "/api/company/NVDA",
                                   {"as_of": ["hier"]})[0], 400)
        self.assertEqual(api.route(self.conn, "/api/rien", {})[0], 404)

    def test_export_demo_embeds_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "demo.html")
            export_demo(self.conn, out)
            html = open(out, encoding="utf-8").read()
        self.assertNotIn("/*__DATA__*/null", html)
        start = html.index("window.__DATA__ = ") + len("window.__DATA__ = ")
        data = json.loads(html[start:html.index(";\n", start)])
        self.assertIn("2026-05-27", data["NVDA"])


if __name__ == "__main__":
    unittest.main()
