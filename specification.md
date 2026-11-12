# One-Page Specification — Event Registration Cleaner

## 1. Purpose

Build a console-based Python application that reads messy event registration entries, extracts participant information, validates and cleans the data, detects duplicates, and generates reports for the event team.

## 2. Input

The application reads `registrations.csv`, containing at least 20 records with two columns:

- `id` — unique registration identifier.
- `entry` — original registration text from a form or message.

CSV values containing commas must be quoted correctly. Original registration text must be preserved for fact-checking and human review.

## 3. LLM Extraction Contract

For each registration entry, the LLM must return exactly one JSON object containing five keys:

- `name`
- `phone`
- `email`
- `year`
- `branch`

The LLM extracts information only. It must not validate, repair, or guess missing information.

Extraction rules:

- Name: Copy as written or return null.
- Phone: Remove spaces, plus signs, and dashes only. Never change digits.
- Email: Copy exactly as written. Do not complete or correct it. Word-form addresses using terms such as "at" or "dot" return null.
- Year: Return an integer from 1 to 4. "Final year" means 4. Roman numerals I, II, III, and IV map to 1, 2, 3, and 4.
- Branch: Return CSE, IT, AIDS, ECE, EEE, MECH, CIVIL, other, or null.
- Unknown or unclear information must not be guessed.

## 4. Python Fact-Checking and Cleaning

Python performs deterministic checks after extraction.

- Phone digits must occur in the original entry.
- Email must occur in the original entry using a case-insensitive comparison.
- Unsupported phone or email values are rejected.
- Names are title-cased and repeated whitespace is collapsed.
- Phone formatting is removed. A leading 91 or 0 is removed only when the result is a valid 10-digit Indian mobile number.
- Emails are lowercased and checked for one `@`, no spaces, and a dot after `@`.
- Year must be an integer from 1 to 4.
- Unknown branches become `other`.
- The `other` branch and missing branches are flagged for human review.

Python must never invent phone digits or complete email addresses.

## 5. Duplicate Detection and Status

Duplicate detection happens after cleaning.

A registration is considered a duplicate if its cleaned phone number or cleaned email address has already appeared in an earlier registration.

The first matching registration ID is recorded as the duplicate reference.

Each entry receives one of three statuses:

- `valid` — all required fields pass validation and the entry is not a duplicate.
- `needs_fix` — one or more required fields are missing or invalid.
- `duplicate` — the cleaned phone or email matches an earlier registration.

Duplicate entries remain in `problems.csv`.

## 6. Output Files

The application generates three reports:

1. `clean_list.csv` — valid registrations only, with cleaned fields.
2. `problems.csv` — invalid and duplicate registrations, including original text and reasons.
3. `summary.txt` — total entries, counts by status, and valid registrations grouped by branch and year.

## 7. Human Review and Safety

The event team must review `problems.csv`, contact participants to confirm corrections, and update official records only after human confirmation.

The application must not silently invent or modify participant contact details.

Synthetic or anonymised data should be used for demonstrations and testing.

## 8. Testing and Evaluation

The project includes unit tests and an evaluation harness covering:

- Normal extraction and cleaning cases.
- Missing and invalid information.
- Unsupported or invented contact details.
- Prompt-injection attempts.
- Duplicate registrations with different formatting.

The offline evaluation harness uses fixed sample extraction results and does not represent live LLM performance.