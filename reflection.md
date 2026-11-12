# Project Reflection — Event Registration Cleaner

This project focuses on a practical problem faced by event teams: registration information often arrives in different formats, and checking every entry manually takes time. The Event Registration Cleaner was designed to organize this information while avoiding unsafe guesses about participants' contact details.

One important learning from this project was the difference between information extraction and data cleaning. The planned LLM component extracts the name, phone number, email, year, and branch from an unstructured registration message. Python then checks and cleans the extracted values using clearly defined rules. Keeping these responsibilities separate makes the program easier to test, understand, and explain.

The fact-checking step is especially important. A phone number returned by the extractor must be supported by the digits in the original registration. An email address must also appear in the original entry. If a value is missing or invalid, the program flags it instead of completing or inventing information. This is important because incorrect contact details could prevent participants from receiving event updates or certificates.

I also learned why duplicate detection should happen after cleaning. The same phone number may be written with spaces, a country prefix, or punctuation. Comparing cleaned values helps identify likely duplicate registrations. The program records the first matching registration ID and sends later matches to the problem report. However, matching contact details do not prove that two registrations belong to the same person, so human review is necessary.

Testing helped identify normal and unusual inputs. The project includes six unit tests and an evaluation harness covering five evaluation cases, two red-team cases, and two duplicate-format checks. All these local tests passed. They check invalid values, phone formatting, unsupported contact details, and instructions embedded in registration entries.

One challenge was that the live OpenAI API returned a `429 credit_balance_exhausted` error because the account had no remaining credits. Therefore, I added an offline demonstration mode using regular expressions. This allowed me to demonstrate the Python cleaning, validation, duplicate detection, and reporting pipeline without API calls. The offline mode is not a replacement for live LLM extraction, and its results are not presented as live AI results.

The most important design decision is the human checkpoint. The software can organize information and flag problems, but the event team must contact participants and confirm corrections before changing official records.

Overall, this project taught me to separate AI extraction from deterministic processing, validate model output, test unusual inputs, handle API failures, and keep humans responsible for important decisions. Future improvements could include measuring real API latency and token usage, adding retry handling, and testing with a larger collection of anonymised registration examples.