\# AccessLens — Security Finding 001



\*\*Title:\*\* Broken Object Level Authorization (BOLA)



\*\*Environment:\*\* Local Python 3.14.10 application, fictional student data



\*\*Finding Status:\*\* Remediated and Retested



\*\*Test Results:\*\* 6 of 6 automated tests passed



\## 1. Summary



The AccessLens notes API contained a Broken Object Level Authorization (BOLA) vulnerability that allowed authenticated users to access private notes belonging to other users.



During testing, I discovered that Alex could retrieve Jordan's private note by changing the requested note ID. I investigated the HTTP traffic, identified the missing server-side authorization check, implemented a fix, and validated the remediation through manual testing and six automated security tests.



\## 2. Expected Security Rule



Authenticated users should only be permitted to access notes they own.



Any attempt to access another user's private notes must be denied, regardless of whether the requested note exists.



\## 3. Steps to Reproduce



1\. Start the AccessLens application locally using `py server.py`.

2\. Open the application at `http://127.0.0.1:8000`.

3\. Select Alex as the authenticated demo user.

4\. Request note `2001`, which belongs to Jordan.

5\. Before remediation, the API returned HTTP 200 OK and exposed Jordan's private note.



\*\*Vulnerable endpoint:\*\* `GET /api/notes/2001`



\## 4. Evidence



\### Before Remediation



\- Authenticated user: Alex

\- Requested resource: Jordan's note 2001

\- HTTP response: 200 OK

\- Result: Unauthorized access to another user's private information



\### After Remediation



\- Authenticated user: Alex

\- Requested resource: Jordan's note 2001

\- HTTP response: 403 Forbidden

\- Result: Access denied



Automated testing additionally confirmed that denied responses did not contain a `content` field.



\## 5. Security Impact



In a real application, this type of authorization vulnerability could allow authenticated users to retrieve private information belonging to other accounts.



Potential consequences include unauthorized disclosure of sensitive documents, personal information, or confidential business data.



This vulnerability was demonstrated exclusively in a local educational application using fictional data. No real user information was exposed.



\## 6. Root Cause



The application originally verified whether a requested note existed but failed to verify whether the authenticated user owned it.



The server returned the requested note without enforcing resource-level authorization.



\## 7. Remediation



I implemented a server-side ownership verification check:



```python

if note\["owner"] != user:

&#x20;   self.send\_json(403, {"error": "Forbidden"})

&#x20;   return

```



This change prevents authenticated users from retrieving notes belonging to other accounts.



Authorized requests continue to return HTTP 200 OK.



\## 8. Automated Security Test Results



| Test Scenario | Expected | Actual | Result |

|---|---|---|---|

| Alex reads own note 1001 | 200 | 200 | PASS |

| Alex requests Jordan's note 2001 | 403 | 403 | PASS |

| Jordan reads own note 2001 | 200 | 200 | PASS |

| Jordan requests Alex's note 1001 | 403 | 403 | PASS |

| Invalid authentication token | 401 | 401 | PASS |

| Alex requests nonexistent note 9999 | 404 | 404 | PASS |



\*\*Final Results:\*\*



\- Automated tests executed: 6

\- Tests passed: 6

\- Tests failed: 0

\- Denied-response content checks passed: 2



All six tests returned the expected HTTP status codes.



The two cross-user access tests also verified that the denied responses did not contain a private note's `content` field.



These tests validate the specified scenarios but do not establish that the application is free from all security vulnerabilities.



\## 9. Remaining Security Limitations



AccessLens is a local educational application and is not designed for production deployment.



Remaining limitations include:



\- Static demonstration bearer tokens instead of secure production authentication.

\- Limited user accounts and fictional test data.

\- No comprehensive assessment of every authentication or authorization edge case.

\- No automated continuous integration testing.

\- Additional input validation and security testing are still needed.



\## 10. How I Used AI and What I Verified Myself



I used ChatGPT to explain HTTP requests and responses, understand the authorization vulnerability, suggest remediation code, and troubleshoot Python indentation and testing errors.



I personally:



\- Launched the application locally using Python.

\- Reproduced unauthorized access to another user's private note.

\- Examined HTTP requests using Chrome Developer Tools.

\- Located the vulnerable authorization logic in `server.py`.

\- Applied and tested the server-side authorization fix.

\- Executed six automated security tests.

\- Confirmed the expected HTTP responses.

\- Documented the vulnerability, remediation, and verification results.



AI assistance supported the learning and development process, while the test execution and observations were verified directly in my local environment.



\## 11. Final Assessment



\*\*Finding 001: Remediated and Retested Successfully\*\*



The identified resource-level authorization flaw was corrected for the tested scenarios.



AccessLens now denies cross-user note requests while allowing authorized access to users' own notes.



All six automated security tests passed, providing repeatable evidence that the tested access-control behavior works as intended.



\*\*Next Project Milestone:\*\* Expand AccessLens with additional security scenarios, automated reporting, and AI-assisted vulnerability investigation.

