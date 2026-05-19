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
ROOT = Path(__file__).parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # fetch API가 로컬에서 data.json을 읽을 수 있도록 CORS 허용
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        # /data.json 폴링 로그는 생략 (30초마다 찍혀서 노이즈)
        if "data.json" not in (args[0] if args else ""):
            super().log_message(format, *args)


if __name__ == "__main__":
    print(f"AI Stock Factory 서버 시작: http://localhost:{PORT}")
    print("종료: Ctrl+C\n")
    with HTTPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
