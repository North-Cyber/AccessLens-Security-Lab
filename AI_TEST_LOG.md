# AccessLens 2.0 — AI-assisted security investigation log

**Status:** Investigation planned; results not yet recorded.

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

**Result:** Not yet verified locally by the project owner.

**Evidence to record:** Actual terminal output, number of passed/failed checks, any unexpected response bodies, and any code changes required.

**Interpretation reminder:** If the checks pass, the hypothesis was **not supported** by these scenarios. Do not report it as a vulnerability.

## Human verification

The project owner will execute the code, review the output, and update this log with observed outcomes before claiming a new verified finding or adding a CI requirement.

## Safety and limits

Run only against `127.0.0.1` with the fictional AccessLens users and demo tokens. Never point practice scripts at public systems without explicit authorization.
