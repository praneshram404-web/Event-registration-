
"""Offline demonstration extractor for sample registrations.

This is a deterministic regex-based demo, not an LLM replacement.
"""

import re


def extract_registration(entry):
    text = entry.strip()

    # Extract name
    name_match = re.search(
        r"Name:\s*([^,|]+)",
        text,
        re.IGNORECASE
    )

    if not name_match:
        name_match = re.match(
            r"([A-Za-z]+(?:\s+[A-Za-z]+)?)",
            text
        )

    # Extract phone number
    phone_match = re.search(
        r"(?<!\d)(?:\+91[\s-]*)?(?:\d[\s-]*){10}(?!\d)",
        text
    )

    # Extract email
    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    # Extract year only when followed by "year" or "yr"
    year_match = re.search(
        r"\b(1st|2nd|3rd|4th|5th|III|II|IV|I|V|final)"
        r"\s*(?:year|yr)\b",
        text,
        re.IGNORECASE
    )

    # Extract branch
    branch_match = re.search(
        r"\b(CSE|ECE|IT|EEE|CIVIL|MECH|AIDS|BIO)\b",
        text,
        re.IGNORECASE
    )

    # Convert year formats into numbers
    year_map = {
        "1st": 1,
        "i": 1,
        "2nd": 2,
        "ii": 2,
        "3rd": 3,
        "iii": 3,
        "4th": 4,
        "iv": 4,
        "5th": 5,
        "v": 5,
        "final": 4
    }

    year_text = (
        year_match.group(1).lower()
        if year_match else None
    )

    # Normalize phone number
    phone = None

    if phone_match:
        digits = re.sub(r"\D", "", phone_match.group(0))

        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]

        phone = digits

    return {
        "name": name_match.group(1).strip() if name_match else None,
        "phone": phone,
        "email": email_match.group(0) if email_match else None,
        "year": year_map.get(year_text) if year_text else None,
        "branch": branch_match.group(1).upper() if branch_match else None
    }
