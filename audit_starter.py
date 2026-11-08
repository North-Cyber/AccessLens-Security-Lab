
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_URL = "http://127.0.0.1:8000"


def get_note(token, note_id):
    url = f"{BASE_URL}/api/notes/{note_id}"

    request = Request(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)

    except HTTPError as error:
        return error.code, json.load(error)


def run_test(name, token, note_id, expected):
    status, body = get_note(token, note_id)

    print(f"\n{name}")
    print(f"HTTP Status: {status}")

    assert status == expected, (
        f"FAILED: Expected {expected}, got {status}. "
        f"Response: {body}"
    )

    if expected == 403:
        assert "content" not in body, (
            "SECURITY FAILURE: Private note content was leaked!"
        )
        print("PASS: No private note content leaked.")

    print("PASS: Security behavior is correct!")


def main():
    print("ACCESSLENS AUTOMATED SECURITY TESTS")
    print("-----------------------------------")

    run_test(
        "Test 1: Alex reads his own note",
        "practice-alex", "1001", 200
    )

    run_test(
        "Test 2: Alex attempts Jordan's note",
        "practice-alex", "2001", 403
    )

    run_test(
        "Test 3: Jordan reads his own note",
        "practice-jordan", "2001", 200
    )

    run_test(
        "Test 4: Jordan attempts Alex's note",
        "practice-jordan", "1001", 403
    )

    
    run_test(
        "Test 5: Invalid authentication token",
        "invalid-token", "1001", 401
    )

    run_test(
        "Test 6: Alex requests a nonexistent note",
        "practice-alex", "9999", 404
    )

    print("\nALL 6 SECURITY TESTS PASSED!")



if __name__ == "__main__":
    main()
