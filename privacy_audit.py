"""AccessLens: AI-suggested privacy test, verified against the local API.

Hypothesis: /api/my-notes might return notes from another user.
This script tests that hypothesis; it does not assume a vulnerability exists.
Uses only Python's standard library. Run with the local server active.
"""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:8000"


def request_my_notes(token=None):
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(f"{BASE_URL}/api/my-notes", headers=headers)
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


def check_owner(name, token, expected_ids):
    status, body = request_my_notes(token)
    assert status == 200, f"{name}: expected 200, got {status}: {body}"
    assert body.get("user") == name, f"{name}: wrong user in response: {body}"

    notes = body.get("notes")
    assert isinstance(notes, list), f"{name}: missing notes list: {body}"
    actual_ids = {note.get("id") for note in notes}
    assert actual_ids == expected_ids, (
        f"{name}: unexpected note IDs: expected {expected_ids}, got {actual_ids}"
    )
    assert all(note.get("owner") == name for note in notes), (
        f"{name}: a note belonged to another user: {notes}"
    )
    print(f"PASS: {name}'s note list contains only their own notes: {sorted(actual_ids)}")


def main():
    print("ACCESSLENS — PRIVACY AUDIT (LOCAL ONLY)")
    print("Hypothesis: Does /api/my-notes leak another user's notes?")

    check_owner("alex", "practice-alex", {"1001", "1002"})
    check_owner("jordan", "practice-jordan", {"2001", "2002"})

    status, body = request_my_notes()
    assert status == 401, f"No-token request: expected 401, got {status}: {body}"
    assert "notes" not in body, f"No-token request exposed notes: {body}"
    print("PASS: Missing authentication token is rejected without returning notes.")

    print("\nRESULT: 3 checks passed. No list-level privacy leak found in these scenarios.")
    print("These targeted tests do not establish that the whole application is secure.")


if __name__ == "__main__":
    try:
        main()
    except URLError as error:
        print(f"Could not reach the local server: {error}")
        print("Open another terminal and run: py server.py")
        raise SystemExit(1) from error
