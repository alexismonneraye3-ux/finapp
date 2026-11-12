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
