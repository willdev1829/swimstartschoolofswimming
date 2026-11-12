#!/usr/bin/env python3
"""
Swim Start — local website server.

Serves the static site so you can look at it on this machine before putting it
online. Standard library only: no pip install, no accounts, no running costs.

    python server.py            start the site on http://127.0.0.1:8777
    python server.py --port 80  serve on a different port

There is no booking system: enquiries come in by phone and email.
"""

import argparse
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SERVABLE_SUFFIXES = {
    ".html", ".css", ".js", ".ico", ".txt", ".webmanifest",
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif",
    ".woff", ".woff2",
}

CSP = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data:",
    "frame-src https://maps.google.com https://www.google.com",
    "connect-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
])


class Handler(SimpleHTTPRequestHandler):
    server_version = "SwimStart"
    sys_version = ""  # don't advertise the Python version to the world

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, fmt, *args):
        # Control characters in a URL could otherwise forge lines in the log.
        line = (fmt % args).replace("\r", "\\r").replace("\n", "\\n")
        sys.stderr.write("%s - %s\n" % (self.log_date_time_string(), line))

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=(), payment=()")
        self.send_header("Content-Security-Policy", CSP)

        # Pages, styles and scripts must be re-checked every visit, or a
        # browser will happily keep showing last month's copy and never see a
        # fix. Images rarely change, so they can sit in the cache.
        suffix = Path(urllib.parse.urlsplit(self.path).path).suffix.lower()
        if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
                      ".avif", ".ico", ".woff", ".woff2"}:
            self.send_header("Cache-Control", "public, max-age=604800")
        else:
            self.send_header("Cache-Control", "no-cache")

        super().end_headers()

    def list_directory(self, path):
        """Never publish a listing of what is in a folder."""
        self.send_error(404, "Not found")
        return None

    def _servable(self):
        """Is the requested URL one of the file types we publish?"""
        path = urllib.parse.urlsplit(self.path).path
        parts = [part for part in path.split("/") if part]

        # Hidden files and folders (.claude, .git, .env) are never served.
        if any(part.startswith(".") for part in parts):
            return False

        # Anything tucked away for reference stays off the website.
        if parts and parts[0] in {"_archived-booking-system", "__pycache__", "docs"}:
            return False

        # "/" and "/folder/" resolve to an index.html, or to a 404 above.
        if not parts or path.endswith("/"):
            return True

        return Path(parts[-1]).suffix.lower() in SERVABLE_SUFFIXES

    def do_GET(self):
        if not self._servable():
            self.send_error(404, "Not found")
            return
        super().do_GET()

    def do_HEAD(self):
        if not self._servable():
            self.send_error(404, "Not found")
            return
        super().do_HEAD()


def main():
    parser = argparse.ArgumentParser(description="Swim Start website server")
    parser.add_argument("--port", type=int, default=8777, help="port to serve on (default 8777)")
    parser.add_argument("--host", default="127.0.0.1", help="host to bind (use 0.0.0.0 to allow other devices)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Swim Start running at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
