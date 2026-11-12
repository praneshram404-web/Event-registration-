"""Pure-Python validation and cleaning for event registrations."""
import re

ALLOWED_BRANCHES = {"CSE", "IT", "AIDS", "ECE", "EEE", "MECH", "CIVIL"}
REQUIRED_KEYS = ("name", "phone", "email", "year", "branch")


def read_entry(entry):
    """Return the original registration text with outer whitespace removed."""
    return entry.strip() if isinstance(entry, str) else ""


def check_facts(original, data):
    """Reject phone/email values that are not supported by the original text."""
    if not isinstance(data, dict):
        return {key: None for key in REQUIRED_KEYS}

    checked = {key: data.get(key) for key in REQUIRED_KEYS}

    phone = checked["phone"]
    if phone is not None:
        if not isinstance(phone, str) or not phone.isdigit():
            checked["phone"] = None
        else:
            original_digits = re.sub(r"\D", "", original)
            if phone not in original_digits:
                checked["phone"] = None

    email = checked["email"]
    if email is not None:
        if not isinstance(email, str):
            checked["email"] = None
        elif ("@" not in email or " " in email or
              " at " in email.lower() or " dot " in email.lower()):
            checked["email"] = None
        elif email.lower() not in original.lower():
            checked["email"] = None

    name = checked["name"]
    if name is not None and not isinstance(name, str):
        checked["name"] = None

    year = checked["year"]
    if isinstance(year, bool) or not isinstance(year, int):
        checked["year"] = None

    branch = checked["branch"]
    if branch is not None and not isinstance(branch, str):
        checked["branch"] = None

    return checked


def clean_phone(phone):
    """Remove formatting and an allowed country/trunk prefix; never alter digits otherwise."""
    if not isinstance(phone, str) or not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) == 10 and digits[0] in "6789":
        return digits
    return None


def clean_email(email):
    """Lowercase an email only if the basic project checks pass."""
    if not isinstance(email, str) or not email:
        return None
    email = email.strip().lower()
    if email.count("@") != 1 or any(ch.isspace() for ch in email):
        return None
    local, domain = email.split("@")
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        return None
    return email


def clean(data):
    """Apply the project's transparent cleaning rules."""
    name = data.get("name")
    if isinstance(name, str) and name.strip():
        name = " ".join(name.split()).title()
    else:
        name = None

    phone = clean_phone(data.get("phone"))
    email = clean_email(data.get("email"))

    year = data.get("year")
    if isinstance(year, bool) or year not in (1, 2, 3, 4):
        year = None

    branch = data.get("branch")
    if isinstance(branch, str) and branch.strip():
        branch = branch.strip().upper()
        if branch not in ALLOWED_BRANCHES:
            branch = "other"
    else:
        branch = None

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "year": year,
        "branch": branch,
    }


def is_valid(data):
    """Return a list of human-readable problems; an empty list means valid."""
    problems = []
    if not data.get("name"):
        problems.append("Missing name")
    if not data.get("phone"):
        problems.append("Invalid or missing phone")
    if not data.get("email"):
        problems.append("Invalid or missing email")
    if data.get("year") not in (1, 2, 3, 4):
        problems.append("Invalid or missing year")
    if data.get("branch") not in ALLOWED_BRANCHES:
        problems.append("Invalid or missing branch")
    return problems
