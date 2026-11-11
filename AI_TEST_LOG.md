# AccessLens 2.0 — AI-assisted security investigation log

**Status:** Locally verified by project owner; the specific data-leak hypothesis was not supported by these three tests.

## Purpose

Use AI to propose a **specific security hypothesis**, run a reproducible test against **only the local AccessLens practice server**, and record whether evidence supports or rejects the hypothesis. An AI suggestion is **not** a confirmed vulnerability.

## Hypothesis H-002: Private note-list leakage

**AI-assisted suggestion:** Even if `GET /api/notes/{id}` enforces ownership, the separate `GET /api/my-notes` endpoint might return notes belonging to someone else.

**Security rule:** An authenticated user's note list must contain only notes whose `owner` matches that user.

**Test plan:**
1. Start `py server.py` locally.
2. Run `py privacy_audit.py` in a second terminal.
3. Verify Alex sees only `1001` and `1002`, owned by Alex.
4. Verify Jordan sees only `2001` and `2002`, owned by Jordan.
5. Verify a request without a bearer token returns `401` without a `notes` field.

**Result (observed locally):** 3 of 3 checks passed. Alex received note IDs `1001` and `1002`, Jordan received `2001` and `2002`, and the request without an authentication token was rejected with no notes returned. No note-list privacy leak was found in these tested scenarios.

**Evidence:** PowerShell screenshot shared after running `py privacy_audit.py` on the owner's Windows computer. The output states `RESULT: 3 checks passed. No list-level privacy leak found in these scenarios.` No unexpected responses or code changes were reported.

**Interpretation reminder:** If the checks pass, the hypothesis was **not supported** by these scenarios. Do not report it as a vulnerability.

## Human verification

The project owner executed the script and reviewed the output on their local computer. These passing tests **refute the proposed weakness in the tested cases**; they are not a new confirmed vulnerability. CI can now repeat these checks alongside the original regression suite.

## Safety and limits

Run only against `127.0.0.1` with the fictional AccessLens users and demo tokens. Never point practice scripts at public systems without explicit authorization.
