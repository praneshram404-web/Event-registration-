# Judgment Framework — Event Registration Cleaner

| Tool part / decision | What can go wrong? | Who checks it and what happens? |
|---|---|---|
| LLM field extraction | The model may omit, misread, or invent a name, contact detail, year, or branch. | Python checks phone digits and email addresses against the original entry. The event team reviews problem rows. |
| Phone cleaning | Formatting or prefix removal may be applied incorrectly. | Python applies only the defined deterministic rules. Invalid numbers are sent to `problems.csv`. |
| Email cleaning | Lowercasing is allowed, but completing a missing domain would be guessing. | Python never completes an email address. The event team contacts the registrant for confirmation. |
| Year and branch mapping | A Roman numeral or branch name may be misunderstood. | Python accepts only years 1–4 and the allowed branch values. Unclear values are flagged. |
| Duplicate detection | Two different people may share a contact detail, or one person may register more than once. | The first matching registration ID is recorded. The event team reviews the match before deciding what to retain. |
| Report generation | A software error could omit or misclassify a registration. | The operator checks report totals against input rows and inspects `problems.csv`. |
| Changing contact details | An incorrect change could prevent event updates or certificate delivery. | **Human checkpoint:** The event team contacts the participant and confirms the correct details before changing the official record. |

## Three Judgment Questions

### 1. What can the tool decide?

The tool can:
- Format values using explicit cleaning rules.
- Validate required fields.
- Flag missing or invalid information.
- Identify registrations with matching cleaned contact details.
- Generate reports for review.

### 2. What must the tool not decide?

The tool must not:
- Guess missing phone digits.
- Complete or invent email addresses.
- Decide a person's true identity.
- Silently delete duplicate registrations.
- Change official participant records without confirmation.

### 3. Where is human judgment required?

The event team must:
- Review all entries in `problems.csv`.
- Contact participants to confirm missing or incorrect information.
- Verify suspected duplicates.
- Confirm corrections before updating official records.
- Decide how to handle duplicate registrations.

## Final Human Review Rule

The application supports the event team; it does not replace human judgment. All uncertain contact details and duplicate cases must be reviewed by a human before official changes are made.