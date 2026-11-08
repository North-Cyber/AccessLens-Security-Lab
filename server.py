
"""AccessLens practice server.

Local-only security learning application.
Uses fictional data and demo-only bearer tokens.
Python 3.10+; no third-party packages required.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import json

BASE_DIR = Path(__file__).resolve().parent

# Demo-only tokens, NOT secure authentication for a real product.
DEMO_TOKENS = {
    "practice-alex": "alex",
    "practice-jordan": "jordan",
}

NOTES = {
    "1001": {"id": "1001", "owner": "alex", "title": "Networking study plan", "content": "Review DNS, HTTP, and TLS."},
    "1002": {"id": "1002", "owner": "alex", "title": "Interview notes", "content": "Describe a security finding with evidence."},
    "2001": {"id": "2001", "owner": "jordan", "title": "Private project notes", "content": "My mock project concept and draft feedback."},
    "2002": {"id": "2002", "owner": "jordan", "title": "Scholarship brainstorm", "content": "Practice example only; not a real student's data."},
}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, value):
        payload = json.dumps(value, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def demo_user(self):
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        return DEMO_TOKENS.get(header[len("Bearer "):])

    def do_GET(self):
        path = urlsplit(self.path).path

        if path == "/":
            content = (BASE_DIR / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/health":
            self.send_json(200, {"service": "AccessLens", "scope": "local practice only"})
            return

        user = self.demo_user()

        if user is None:
            self.send_json(401, {"error": "Demo bearer token required"})
            return

        if path == "/api/my-notes":
            own_notes = [
                note for note in NOTES.values()
                if note["owner"] == user
            ]
            self.send_json(200, {"user": user, "notes": own_notes})
            return

        if path.startswith("/api/notes/"):
            note_id = path[len("/api/notes/"):]
            note = NOTES.get(note_id)

            if note is None:
                self.send_json(404, {"error": "Note not found"})
                return

            # SECURITY FIX:
            # Verify that the authenticated user owns the note.
            if note["owner"] != user:
                self.send_json(403, {"error": "Forbidden"})
                return

            # Only authorized users can reach this line.
            self.send_json(200, note)
            return

        self.send_json(404, {"error": "Unknown endpoint"})


def main():
    parser = argparse.ArgumentParser(
        description="Local AccessLens security practice server"
    )
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer(
        ("127.0.0.1", args.port),
        Handler
    )

    print(f"AccessLens running locally at http://127.0.0.1:{args.port}")
    print("This is a local practice application. Do not expose it publicly.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping practice server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
