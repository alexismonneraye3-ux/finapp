"""Ligne de commande : python -m finapp <commande>."""

import argparse
import json
import os

from . import api, db, reports, sec, seed, views

ROOT = os.path.dirname(os.path.dirname(__file__))


def calc_n(x):
    return ("%.0f" % x) if float(x).is_integer() else ("%s" % x)


def export_demo(conn, out_path):
    """Écrit une page autonome, données incluses, qui s'ouvre sans serveur."""
    data = {}
    for c in conn.execute("SELECT ticker FROM companies ORDER BY ticker"):
        ticker = c["ticker"]
        latest = views.company_view(conn, ticker)
        snapshots = {"": latest}
        for d in latest["timeline"]:
            snapshots[d] = views.company_view(conn, ticker, d)
        data[ticker] = snapshots
    with open(os.path.join(ROOT, "web", "index.html"), encoding="utf-8") as fh:
        html = fh.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*__DATA__*/null", payload)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)


def main(argv=None):
    p = argparse.ArgumentParser(prog="finapp", description=__doc__)
    p.add_argument("--db", default=os.path.join(ROOT, "finapp.db"),
                   help="chemin de la base SQLite")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="crée la base")
    sub.add_parser("seed", help="charge les jeux d'exemple")
    s = sub.add_parser("ingest-sec", help="collecte les comptes d'une société à la SEC")
    s.add_argument("--cik", required=True)
    s.add_argument("--ticker", required=True)
    s.add_argument("--user-agent", required=True,
                   help="nom et adresse de contact, exigés par la SEC")
    s = sub.add_parser("show", help="affiche la fiche d'une société en JSON")
    s.add_argument("ticker")
    s.add_argument("--as-of")
    s = sub.add_parser("serve", help="lance l'appli en local")
    s.add_argument("--port", type=int, default=8000)
    s = sub.add_parser("export-demo", help="écrit une page autonome")
    s.add_argument("--out", default=os.path.join(ROOT, "dist", "demo.html"))
    s = sub.add_parser("reports", help="liste les signalements d'erreur reçus")
    s.add_argument("--all", action="store_true",
                   help="inclure aussi les signalements déjà traités")
    args = p.parse_args(argv)

    if args.cmd == "serve":
        db.init(db.connect(args.db)).close()
        api.serve(args.db, args.port)
        return

    conn = db.init(db.connect(args.db))
    if args.cmd == "init":
        print("Base prête : %s" % args.db)
    elif args.cmd == "seed":
        print("%d faits ajoutés" % seed.seed(conn))
    elif args.cmd == "ingest-sec":
        doc = sec.fetch_companyfacts(args.cik, args.user_agent)
        print("%d faits ajoutés" % sec.ingest(conn, doc, args.ticker))
    elif args.cmd == "show":
        print(json.dumps(views.company_view(conn, args.ticker, args.as_of),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "reports":
        rows = reports.list_reports(conn, None if args.all else reports.OPEN)
        if not rows:
            print("Aucun signalement.")
        for r in rows:
            print("n° %d · %s · %s · %s %s, période finissant le %s, valeur %s %s" % (
                r["id"], r["created_at"], r["status"], r["ticker"], r["metric"],
                r["period_end"], calc_n(r["value"]), r["unit"]))
            if r["about"]:
                print("    Affiché : %s" % r["about"])
            print("    Message : %s" % r["message"])
            print("    Source  : %s" % r["source_url"])
    elif args.cmd == "export-demo":
        export_demo(conn, args.out)
        print("Page écrite : %s" % args.out)
    conn.close()


if __name__ == "__main__":
    main()
