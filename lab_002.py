"""AccessLens Lab 002 — API response privacy review.

INTENTIONALLY INSECURE TRAINING EXERCISE.
All profiles and tokens are fictional. Local-only, never deploy publicly.
Python 3.10+, standard library only.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

PORT = 8001

DEMO_TOKENS = {
    "practice-alex": "alex",
    "practice-jordan": "jordan",
}

PROFILES = {
    "alex": {
        "username": "alex",
        "display_name": "Alex",
        "program": "Cybersecurity",
        "bio": "Interested in securing useful technology.",
        "internal_support_note": "Fictional internal review: account ticket 104",
        "demo_recovery_token": "fake-reset-alex-001-not-a-real-secret",
    },
    "jordan": {
        "username": "jordan",
        "display_name": "Jordan",
        "program": "Computer Science",
        "bio": "Enjoys learning how software works.",
        "internal_support_note": "Fictional internal review: account ticket 205",
        "demo_recovery_token": "fake-reset-jordan-002-not-a-real-secret",
    },
}

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AccessLens — Lab 002</title>
<style>
:root { color-scheme: dark; font-family: system-ui, sans-serif; }
body { margin: 0; background: #0c1220; color: #f1f5ff; }
main { max-width: 680px; padding: 30px 22px; margin: 42px auto; }
h1 { font-size: 2.4rem; margin: 8px 0; }
p { color: #bfcae0; line-height: 1.6; }
.panel { background: #19233b; border: 1px solid #35466a; padding: 24px; border-radius: 16px; }
select, button { font-size: 1rem; padding: 12px 15px; border-radius: 8px; }
select { background: #111b30; color: white; border: 1px solid #60759d; }
button { background: #a9c2ff; color: #0c1220; border: none; font-weight: bold; cursor: pointer; }
label { display: block; margin-bottom: 9px; }
#card { margin-top: 24px; padding: 18px; background: #0f1729; border-radius: 10px; min-height: 80px; }
.warning { font-size: .9rem; color: #ffd69c; }
</style>
</head>
<body><main>
<p style="font-size:.78rem;letter-spacing:.16em;text-transform:uppercase">Security research · isolated local lab</p>
<h1>AccessLens: Profile Review</h1>
<p>This page displays a simple user profile. Your job is to compare what the page <strong>shows</strong> with what the API actually <strong>sends</strong>.</p>
<div class="panel">
<label for="user">Demo account</label>
<select id="user">
<option value="practice-alex">Alex</option>
<option value="practice-jordan">Jordan</option>
</select>
<button id="load">Load profile</button>
<div id="card" aria-live="polite">No profile loaded yet.</div>
<p class="warning">All names, tokens, notes and account details are fictional. This practice server contains an intentional privacy flaw. Keep it local.</p>
</div>
<p>Investigation hint: Open Chrome DevTools → Network → Fetch/XHR, click Load profile, then inspect the <strong>Response</strong> of the <code>profile</code> request.</p>
<script>
const card = document.querySelector("#card");
document.querySelector("#load").addEventListener("click", async () => {
  card.textContent = "Loading…";
  try {
    const token = document.querySelector("#user").value;
    const response = await fetch("/api/profile", {
      headers: { Authorization: "Bearer " + token }
    });
    const data = await response.json();
    if (!response.ok) {
      card.textContent = "HTTP " + response.status + ": " + (data.error || "Request failed");
      return;
    }
    // The page deliberately displays only a couple of the fields it receives.
    const name = document.createElement("h2");
    name.textContent = data.display_name;
    const program = document.createElement("p");
    program.textContent = "Program: " + data.program;
    card.replaceChildren(name, program);
  } catch (err) {
    card.textContent = "Request error: " + String(err);
  }
});
</script>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = urlsplit(self.path).path

        if path == "/":
            raw = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)
            return

        if path == "/api/health":
            self.send_json(200, {"service": "AccessLens Lab 002", "local_only": True})
            return

        if path == "/api/profile":
            auth = self.headers.get("Authorization", "")
            token = auth[len("Bearer "):] if auth.startswith("Bearer ") else ""
            username = DEMO_TOKENS.get(token)
            if username is None:
                self.send_json(401, {"error": "Demo token required"})
                return

            # INTENTIONAL TRAINING FLAW:
            # The response may contain fields that the client should never receive.
            # Investigate first; do not fix until you understand the evidence.
            self.send_json(200, PROFILES[username])
            return

        self.send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"AccessLens Lab 002 is running at http://127.0.0.1:{PORT}")
    print("Intentionally insecure fictional-data exercise. Keep it local.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Lab 002...")
    finally:
        server.server_close()
