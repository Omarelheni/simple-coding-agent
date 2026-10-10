#!/usr/bin/env python3
"""A simple HTTP server that serves static files from the current directory.

Running this script will start a server on http://localhost:8000/ and
serve files such as index.html. It uses the built‑in `http.server` module
for simplicity.
"""

import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that can be extended in the future.

    For now it simply inherits from ``SimpleHTTPRequestHandler`` which
    already serves files from the current working directory.
    """

    pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT} (http://localhost:{PORT}/) ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            httpd.server_close()
