#!/usr/bin/env python3
"""
AI Stock Factory 로컬 서버.
실행: python server.py
접속: http://localhost:8080
"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8080
ROOT        = Path(__file__).parent
MARKET_JSON = ROOT.parent.parent / "data" / "market" / "latest.json"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/api/market":
            self._serve_market()
        else:
            super().do_GET()

    def _serve_market(self):
        if not MARKET_JSON.exists():
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b'{"error":"market data not found"}')
            return
        data = MARKET_JSON.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(data)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        path = args[0] if args else ""
        if "data.json" not in path and "/api/market" not in path:
            super().log_message(format, *args)


if __name__ == "__main__":
    print(f"AI Stock Factory 서버 시작: http://localhost:{PORT}")
    print("종료: Ctrl+C\n")
    with HTTPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
