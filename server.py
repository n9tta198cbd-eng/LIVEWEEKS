from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import sys

BASE_DIR = os.path.dirname(__file__)
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
API_DIR = os.path.join(BASE_DIR, "api")

sys.path.append(API_DIR)

PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split("?", 1)[0]

        if path == "/" or path == "":
            path = "/index.html"

        path = path.lstrip("/")
        return os.path.join(PUBLIC_DIR, path)

    def do_GET(self):
        parsed = urlparse(self.path)

        # ===== API =====
        if parsed.path == "/api/generate":
            try:
                from generate import generate_image

                params = parse_qs(parsed.query)
                result = generate_image(params)

                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                self.wfile.write(result)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(str(e).encode())
            return

        # ===== STATIC =====
        return super().do_GET()


if __name__ == "__main__":
    os.chdir(PUBLIC_DIR)
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Server running → http://localhost:{PORT}")
    server.serve_forever()
