
"""Console entry point and report generation."""

import argparse
import csv
import os
from collections import Counter

from cleaner import read_entry, check_facts, clean, is_valid
from llm_extractor import extract_registration


def process(input_path="registrations.csv", output_dir=".", extractor=None):
    """Read registrations, extract, validate, detect duplicates and write reports."""

    if extractor is None:
        extractor = extract_registration

    results = []
    seen_phones = {}
    seen_emails = {}

    with open(input_path, "r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames or not {"id", "entry"}.issubset(reader.fieldnames):
            raise ValueError("Input CSV must contain the columns: id, entry")

        for row_number, row in enumerate(reader, start=2):
            registration_id = (row.get("id") or f"ROW{row_number}").strip()
            original = read_entry(row.get("entry", ""))

            try:
                extracted = extractor(original)
                fact_checked = check_facts(original, extracted)
                cleaned = clean(fact_checked)
                problems = is_valid(cleaned)

                duplicate_of = None
                phone = cleaned["phone"]
                email = cleaned["email"]

                if phone and phone in seen_phones:
                    duplicate_of = seen_phones[phone]

                if email and email in seen_emails and duplicate_of is None:
                    duplicate_of = seen_emails[email]

                if duplicate_of:
                    status = "duplicate"
                    problems.append(f"Duplicate of {duplicate_of}")
                elif problems:
                    status = "needs_fix"
                else:
                    status = "valid"

                if phone:
                    seen_phones.setdefault(phone, registration_id)

                if email:
                    seen_emails.setdefault(email, registration_id)

            except Exception as error:
                cleaned = {
                    "name": None,
                    "phone": None,
                    "email": None,
                    "year": None,
                    "branch": None,
                }

                status = "needs_fix"
                problems = [
                    f"Extraction/API error: {type(error).__name__}: {error}"
                ]

            results.append({
                "id": registration_id,
                **cleaned,
                "status": status,
                "reasons": "; ".join(problems),
                "original": original,
            })

    write_reports(results, output_dir)
    return results


def write_reports(results, output_dir="."):
    """Generate clean_list.csv, problems.csv and summary.txt."""

    os.makedirs(output_dir, exist_ok=True)

    clean_fields = [
        "id", "name", "phone", "email", "year", "branch"
    ]

    with open(
        os.path.join(output_dir, "clean_list.csv"),
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=clean_fields)
        writer.writeheader()

        for row in results:
            if row["status"] == "valid":
                writer.writerow({
                    key: row[key] for key in clean_fields
                })

    problem_fields = [
        "id", "status", "reasons", "original",
        "name", "phone", "email", "year", "branch"
    ]

    with open(
        os.path.join(output_dir, "problems.csv"),
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=problem_fields)
        writer.writeheader()

        for row in results:
            if row["status"] != "valid":
                writer.writerow({
                    key: row[key] for key in problem_fields
                })

    status_counts = Counter(
        row["status"] for row in results
    )

    branch_counts = Counter(
        row["branch"]
        for row in results
        if row["status"] == "valid"
    )

    year_counts = Counter(
        row["year"]
        for row in results
        if row["status"] == "valid"
    )

    with open(
        os.path.join(output_dir, "summary.txt"),
        "w",
        encoding="utf-8"
    ) as file:

        file.write("EVENT REGISTRATION SUMMARY\n")
        file.write("===========================\n")
        file.write(f"Total entries: {len(results)}\n")

        for status in ("valid", "needs_fix", "duplicate"):
            file.write(
                f"{status}: {status_counts.get(status, 0)}\n"
            )

        file.write("\nVALID REGISTRATIONS BY BRANCH\n")

        for branch, count in sorted(branch_counts.items()):
            file.write(f"{branch}: {count}\n")

        file.write("\nVALID REGISTRATIONS BY YEAR\n")

        for year, count in sorted(year_counts.items()):
            file.write(f"Year {year}: {count}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Clean event registration entries."
    )

    parser.add_argument(
        "--input",
        default="registrations.csv",
        help="Input CSV path"
    )

    parser.add_argument(
        "--output-dir",
        default=".",
        help="Folder for the three reports"
    )

    parser.add_argument(
        "--offline-demo",
        action="store_true",
        help="Use the offline demonstration extractor"
    )

    args = parser.parse_args()

    extractor = None

    if args.offline_demo:
        from demo_extractor import extract_registration
        extractor = extract_registration

    results = process(
        args.input,
        args.output_dir,
        extractor=extractor
    )

    print(f"Processed {len(results)} registrations.")
    print(f"Reports written to: {args.output_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Project error: {exc}")
        raise SystemExit(1)
