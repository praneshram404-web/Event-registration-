# AI Decision Journal — Event Registration Cleaner

This journal records important development decisions, changes, and testing outcomes during the project.

| Date | AI suggestion / decision | Accepted, changed, or rejected? | Reason and evidence |
|---|---|---|---|
| 2026-11-12 | Use the LLM only to extract registration fields and keep validation and cleaning in Python. | Accepted | This follows the project specification and makes the cleaning rules transparent and testable. |
| 2026-11-12 | Check extracted phone digits and email addresses against the original registration entry. | Accepted | This prevents unsupported contact details from entering the clean list. |
| 2026-11-12 | Automatically complete incomplete email addresses or invent missing phone digits. | Rejected | Contact details must never be guessed or invented. |
| 2026-11-12 | Keep duplicate registrations in `problems.csv` and record the first matching registration ID. | Accepted | The event team needs to review duplicates instead of losing records silently. |
| 2026-11-12 | Use deterministic Python rules for phone, email, year, and branch validation. | Accepted | Deterministic rules make the results easier to test, understand, and explain. |
| 2026-11-12 | Replace the OpenAI SDK request implementation with Python's standard-library `urllib` after a dependency loading error. | Accepted | The original SDK encountered a Windows Application Control DLL error involving `jiter`. The alternative avoids that dependency. |
| 2026-11-12 | Add an offline demonstration mode using regular expressions. | Accepted with limitation | The API account returned a `429 credit_balance_exhausted` error. Offline mode allows demonstration of the Python processing pipeline without API calls. It is not presented as live LLM extraction. |
| 2026-11-12 | Run unit tests and the evaluation harness using fixed sample extraction results. | Accepted | All 6 unit tests and all 9 evaluation, red-team, and duplicate checks passed. These tests verify the local processing logic, not live LLM performance. |

## Key Learning

The project showed that AI extraction and Python validation should have separate responsibilities. The LLM can interpret messy registration text, while Python applies predictable rules and checks the extracted information.

Testing also showed the importance of handling API failures and providing a clearly labelled offline demonstration mode.

Human review remains necessary whenever registration details are missing, invalid, or duplicated.