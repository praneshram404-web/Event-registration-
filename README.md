# Event Registration Cleaner

A console-based Python project that processes messy event registrations, extracts information, validates and cleans it, detects duplicates, and generates three reports.

## Features

- Extracts name, phone, email, year, and branch.
- Uses Python to fact-check extracted information.
- Validates phone numbers and email addresses.
- Detects duplicate registrations.
- Generates clean and problem reports.
- Produces a summary by branch and year.

## Requirements

- Python 3.10 or later
- Internet connection for live model requests
- OpenAI API key with available credits for live LLM mode
- python-dotenv package

## Setup

1. Create a virtual environment.

   **Windows:**
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`.

4. Add your API key to `.env`:

   ```text
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```

5. Never upload `.env` or your API key to GitHub.

6. Check that `registrations.csv` contains the required `id` and `entry` columns.

## Running the Project

### Live LLM Mode

```bash
python main.py
```

This mode sends registration entries to the configured OpenAI model for information extraction. It requires an API key, internet access, and available API credits.

### Offline Demonstration Mode

```bash
python main.py --offline-demo
```

This mode uses a deterministic regular-expression extractor. It does not call an LLM and demonstrates the cleaning, validation, duplicate detection, and reporting pipeline without API calls.

**Note:** Offline demonstration mode is not a replacement for live LLM extraction.

## Output Files

The program generates three output files:

1. `clean_list.csv` — Contains valid registrations only.
2. `problems.csv` — Contains invalid and duplicate registrations with reasons.
3. `summary.txt` — Contains status counts and valid registrations grouped by branch and year.

## Testing

Run the unit tests:

```bash
python -m unittest -v
```

Run the evaluation harness:

```bash
python eval_harness.py
```

The evaluation harness uses fixed sample extraction results, so it does not require an API key or API credits.

It checks evaluation cases, red-team cases, and duplicate detection.

## Project Structure

| File | Description |
|---|---|
| `main.py` | Main processing pipeline and report generation |
| `cleaner.py` | Fact-checking, cleaning, and validation |
| `llm_extractor.py` | Live OpenAI model API integration |
| `demo_extractor.py` | Offline demonstration extractor |
| `system_prompt.txt` | Extraction instructions using the five-role framework |
| `registrations.csv` | 20 synthetic sample registrations |
| `test_project.py` | Unit tests |
| `eval_harness.py` | Evaluation and red-team tests |
| `specification.md` | One-page project specification |
| `judgment_framework.md` | Human judgment framework |
| `cost_latency.md` | Cost and latency analysis |
| `AI_decision_journal.md` | AI decision journal |
| `reflection.md` | Project reflection |

## Safety and Human Review

The LLM is responsible for extracting information. Python checks the extracted values and applies transparent cleaning rules.

The system does not invent phone digits or complete missing email addresses.

Registrations with missing or invalid information are sent to `problems.csv`. Duplicate registrations are also identified.

The event team must review the problem report and contact participants to confirm corrections before changing official records.

Use synthetic or anonymised data for demonstrations. Do not expose real participants' contact details without appropriate permission.

## GitHub

Before committing the project, verify that `.env` is excluded from Git:

```bash
git status --ignored
```

Suggested meaningful commits:

1. `Add project specification and sample registrations`
2. `Implement extraction, validation, and report generation`
3. `Add evaluation, red-team tests, and submission documents`

Never upload `.env` or API keys to GitHub.

## Important Notes

- Offline demonstration results are not live LLM results.
- The evaluation harness uses fixed sample extraction results.
- Live model execution requires available API credits.
- Verify current API pricing before reporting estimated costs.
- Be prepared to explain the code, validation rules, and limitations during the project presentation.