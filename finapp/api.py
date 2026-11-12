"""API JSON et service de l'écran web. Bibliothèque standard uniquement."""

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import db, facts, views

WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def route(conn, path, query):
    """Renvoie (code HTTP, objet JSON) pour une route de l'API."""
    as_of = (query.get("as_of") or [None])[0]
    if as_of is not None and not DATE.match(as_of):
        return 400, {"error": "as_of doit être au format AAAA-MM-JJ"}

    if path == "/api/companies":
        return 200, [{"ticker": c["ticker"], "name": c["name"]}
                     for c in facts.list_companies(conn)]

    m = re.match(r"^/api/company/([A-Za-z0-9.\-]{1,12})$", path)
    if m:
        try:
            return 200, views.company_view(conn, m.group(1), as_of)
        except KeyError as exc:
            return 404, {"error": str(exc.args[0])}

    return 404, {"error": "Route inconnue"}


def make_handler(db_path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse(self.path)
            if url.path.startswith("/api/"):
                conn = db.connect(db_path)
                try:
                    code, body = route(conn, url.path, parse_qs(url.query))
                finally:
                    conn.close()
                self._send(code, json.dumps(body, ensure_ascii=False).encode("utf-8"),
                           "application/json; charset=utf-8")
            elif url.path in ("/", "/index.html"):
                with open(os.path.join(WEB_DIR, "index.html"), "rb") as fh:
                    self._send(200, fh.read(), "text/html; charset=utf-8")
            else:
                self._send(404, b"Introuvable", "text/plain; charset=utf-8")

        def _send(self, code, payload, content_type):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass

    return Handler


def serve(db_path, port=8000, host="127.0.0.1"):
    server = ThreadingHTTPServer((host, port), make_handler(db_path))
    print("Appli disponible sur http://%s:%d" % (host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
