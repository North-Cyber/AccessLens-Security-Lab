# AccessLens — AI-Assisted API Security Investigation

**Status:** Initial investigation completed. BOLA vulnerability reproduced and remediated, six automated API tests passing, and security finding report documented. AI-assisted test generation is planned.

AccessLens is a **local, intentionally vulnerable practice app**. It uses fake student notes to teach broken object-level authorization (BOLA), a major API security risk. The purpose is to demonstrate how a product security engineer discovers a defect, proves impact, fixes it, and verifies the fix.

## Quick start on Windows

1. Install Python 3.10+ if it is not already installed. Confirm in PowerShell with `py --version`.
2. Unzip the starter and open PowerShell in the unzipped `accesslens-starter` folder.
3. Start the practice API: `py server.py`
4. In a browser, visit **http://127.0.0.1:8000**.
5. Keep the server running. Open a **second** PowerShell window in the same folder and run `py audit_starter.py`.
6. Stop the server with **Ctrl+C** when done.

On macOS or Linux replace `py` with `python3`.

## Your first investigation (30–45 minutes)

1. In the web app choose **Alex**, request note **1001**. Record the HTTP status.
2. Still as **Alex**, request note **2001**. Read the returned `owner` field.
3. Ask: Should Alex read Jordan's private note? What did the application fail to check?
4. Open `server.py`, find the `INTENTIONALLY INSECURE CODE` comment, and identify the missing authorization check.
5. In `audit_starter.py`, implement the four TODOs **yourself**, using AI to explain concepts or debug syntax as needed.
6. After writing the failing test, correct the server code; confirm Alex's note returns **200**, Jordan's note returns **403** when requested by Alex, and Jordan can still read Jordan's note.
7. Record your finding using `FINDING_TEMPLATE.md`.

**Why 403?** The server recognizes the demo user, but the user is not permitted to access that record. An absent/invalid bearer token should return **401**.

## Turn this into an internship portfolio project

- **Milestone 1 — HTTP/API fundamentals:** Explain requests, headers, IDs, 200/401/403/404 codes; demonstrate two demo accounts.
- **Milestone 2 — Reproduce the defect:** Capture evidence of an unauthorized response using fictional data.
- **Milestone 3 — Automated regression testing:** Test your own note, someone else's note, nonexistent IDs, and unauthenticated requests. Distinguish test expectations from real responses.
- **Milestone 4 — Fix and retest:** Make a server-side record ownership check, run the test suite, document your remediation and limitations.
- **Milestone 5 — Add AI-assisted investigation:** Ask an AI assistant for additional test cases; verify suggestions rather than assuming they're correct. Keep an `AI_NOTES.md` describing prompts, what you checked, and any incorrect suggestions.
- **Milestone 6 — Publish responsibly:** Add screenshots, a simple architecture diagram, a 2-page security review, and a 60–90 second demo video; publish code to GitHub with a prominent warning that it is intentionally vulnerable practice software.

## Scope and limitations

- **Only your own local server** is authorized for testing.
- Uses fictional information only; do not enter real personal/medical/student data.
- Demo tokens are hard-coded for teaching and **are not production-ready authentication**. Fixing the object ownership check does **not** turn this into a secure real-world service.
- The server binds to `127.0.0.1` so it does not listen on other machines. Do not deploy it on a public IP.
- The starter was generated to help you learn. When showcasing the project, be transparent about starter code/AI assistance, and highlight the tests, decisions, fixes, and analysis **you** performed.

## Ideas for your next version

After the first fix, build a privacy risk checklist (what sensitive data exists, who should access it, and what should be logged), then add a second demo weakness and demonstrate a second fix. Don't race to add a complex AI agent before your basic tests are trustworthy.

## References

- [OWASP: API1 Broken Object Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)
- [PortSwigger: Access control labs](https://portswigger.net/web-security/access-control)

