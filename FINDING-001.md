# AccessLens — Security Finding 001

**Finding:** Broken Object Level Authorization (BOLA / IDOR)  
**Environment:** Python 3.14.10 local-only practice application using fictional student data  
**Status:** Remediated and manually/automatically retested  
**Test results:** 6 of 6 API checks passed in the reported local run

## 1. Summary

The AccessLens notes API originally allowed one authenticated demo user to retrieve another user's private note by changing the note ID. As Alex, I reproduced the issue, inspected the HTTP request, found the missing server-side ownership check in `server.py`, implemented a fix, and validated the behavior using manual and automated tests.

## 2. Expected authorization rule

A demo user should be permitted to retrieve only notes for which `note["owner"]` matches the authenticated user. Cross-user requests must be denied without returning private note content.

## 3. Reproduction before remediation

1. Start the local application with `py server.py`.
2. In the browser, visit `http://127.0.0.1:8000`.
3. Select **Alex**.
4. Request Jordan's note with `GET /api/notes/2001`.
5. Observe an **HTTP 200 OK** response containing Jordan's fictional note.

**Note:** The currently published server is patched. These steps describe the observed **original** behavior, not a vulnerability presently reproduced against the fixed version.

## 4. Evidence

| Observation | Before remediation | After remediation |
| --- | --- | --- |
| Authenticated demo user | Alex | Alex |
| API request | `GET /api/notes/2001` | `GET /api/notes/2001` |
| Response status | `200 OK` | `403 Forbidden` |
| Jordan's private note returned | Yes | No |

The automated checks also confirmed that the two denied cross-user responses lacked a `content` field. That limited check does not prove every possible form of data disclosure is prevented.

## 5. Potential impact

In a real application, this weakness could allow authenticated accounts to retrieve other users' private records by changing object identifiers. This project used only fictional local test data; **no real personal data was exposed**.

## 6. Root cause

The original `/api/notes/{id}` handler checked whether the note existed, but not whether its `owner` was the authenticated user. It then serialized and returned the note.

## 7. Remediation

The server now verifies ownership **before** returning the requested note:

```python
if note["owner"] != user:
    self.send_json(403, {"error": "Forbidden"})
    return

self.send_json(200, note)
```

An owner still receives `200 OK`; another authenticated demo user receives `403 Forbidden`.

## 8. Retest results

| Scenario | Expected | Observed locally | Result |
| --- | ---: | ---: | --- |
| Alex reads note 1001 | 200 | 200 | PASS |
| Alex requests Jordan's note 2001 | 403 | 403 | PASS |
| Jordan reads note 2001 | 200 | 200 | PASS |
| Jordan requests Alex's note 1001 | 403 | 403 | PASS |
| Invalid demo token requests note 1001 | 401 | 401 | PASS |
| Alex requests nonexistent note 9999 | 404 | 404 | PASS |

**Recorded local results:** six tests passed, zero failed. Two denied-response checks additionally confirmed the `content` field was absent.

## 9. Remaining limitations

- Static demonstration tokens do not provide production-grade authentication.
- Tests exercise two fictional users and a small number of scenarios.
- Checking for a missing `content` field is not a comprehensive privacy assessment.
- Additional auth edge cases and response assertions would improve regression coverage. A GitHub Actions workflow has been added to run the current six checks automatically; its status is separate from the reported local run.
- The application must remain local; it is not intended for public deployment.

## 10. AI assistance and personal verification

ChatGPT helped generate the initial scaffold and propose explanations, remediation code, test cases, and report structure. I personally launched the application, reproduced the flaw, inspected requests through Chrome Developer Tools, located the faulty handler, modified the code, resolved execution/indentation errors, and ran the automated tests on my machine. This is a personal educational project, **not** an independent professional penetration test.

## 11. Conclusion

The identified missing ownership check has been fixed for the scenarios tested. The six locally executed automated checks returned the expected HTTP statuses. Broader security assurance would require additional testing.
