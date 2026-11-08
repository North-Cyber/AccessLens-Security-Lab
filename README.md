# AccessLens — API Authorization Security Lab

**Status:** First security investigation completed and remediated. Six API regression tests passed in local testing. **AI-assisted test generation is planned, not yet implemented.**

AccessLens is a **local-only** Python web application using fictional student notes. It demonstrates how a broken object-level authorization (BOLA/IDOR) weakness can expose another user's data, how to add a server-side ownership check, and how to retest that fix.

> **Practice environment only.** The application uses hard-coded demo tokens and is not suitable for production authentication. The Python server listens on `127.0.0.1`. Do not deploy this lab publicly or insert real personal information.

## Investigation and results

- **Original finding:** While acting as Alex, I retrieved Jordan's fictional note `2001` using `GET /api/notes/2001` (`HTTP 200`).
- **Root cause:** The original handler checked whether the requested note existed but did not verify ownership before sending the data.
- **Remediation:** An ownership check now returns `HTTP 403 Forbidden` when the requested note belongs to another authenticated demo user.
- **Verification:** The browser investigation and six automated API tests checked access for both users, invalid credentials, and a missing note.

Read the complete [Security Finding 001](FINDING-001.md) for evidence, impact, remediation, limitations, and the role AI played in the project.

## Run locally

Requirements: **Python 3.10+**, a browser, and no third-party packages.

1. Download or clone the repository and open a terminal in the folder containing `server.py`.
2. Start the server:
   ```powershell
   py server.py
   ```
3. Open **http://127.0.0.1:8000** in your browser.
4. Keep the server running. Open a **second** terminal in the same folder and run:
   ```powershell
   py audit_starter.py
   ```
5. Stop the server with **Ctrl+C**.

On macOS or Linux, use `python3` instead of `py`.

**Current behavior:** Alex can read note `1001` (`200`), but cannot read Jordan's note `2001` (`403`). Switching to Jordan reverses the ownership results. The published server **already includes the fix**; the vulnerable behavior is documented in the finding report.

## Test results

| Scenario | Expected | Locally observed |
| --- | ---: | ---: |
| Alex reads own note 1001 | 200 | 200 — PASS |
| Alex requests Jordan's note 2001 | 403 | 403 — PASS |
| Jordan reads own note 2001 | 200 | 200 — PASS |
| Jordan requests Alex's note 1001 | 403 | 403 — PASS |
| Invalid bearer token requests note 1001 | 401 | 401 — PASS |
| Alex requests nonexistent note 9999 | 404 | 404 — PASS |

The script also checks that two `403` responses omit a `content` field. These are **targeted checks**, not a comprehensive penetration test. Results were observed locally; do not interpret the passing tests as proof the entire application is secure.

## Files

- `server.py` — local Python API and server-side authorization check
- `index.html` — browser interface for exploring notes and HTTP responses
- `audit_starter.py` — six automated authorization and error-handling tests
- `FINDING-001.md` — completed security finding, remediation, and test results

## AI assistance and personal work

The initial application scaffold and portions of the remediation, automated tests, and documentation were created with ChatGPT assistance. I ran the local app, reproduced and inspected the vulnerability in Chrome DevTools, edited the Python files, debugged runtime and indentation issues, and executed the tests myself. I describe the AI assistance transparently and distinguish observed results from proposed improvements.

## Limitations and next steps

- Hard-coded demo bearer tokens are not secure production authentication.
- Only a small set of fictional users and API scenarios are covered.
- More edge cases, response-body checks, and privacy-focused tests are needed.
- Planned: repeatable CI testing, screenshots with sensitive UI cropped out, and human-validated AI-assisted test suggestions.

## Further reading

- [OWASP API Security Top 10 — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [PortSwigger Web Security Academy — Access control](https://portswigger.net/web-security/access-control)
