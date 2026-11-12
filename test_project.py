"""Small unit tests for the deterministic cleaning rules. Run: python -m unittest."""
import unittest
from cleaner import clean_phone, clean_email, clean, check_facts, is_valid


class CleanerTests(unittest.TestCase):
    def test_phone_formatting(self):
        self.assertEqual(clean_phone("+91 98400-12345"), "9840012345")

    def test_invalid_phone_is_not_repaired(self):
        self.assertIsNone(clean_phone("12345"))

    def test_email_lowercased(self):
        self.assertEqual(clean_email("PRIYA.K@gmail.com"), "priya.k@gmail.com")

    def test_email_not_completed(self):
        self.assertIsNone(clean_email("name@gmail"))

    def test_unknown_branch_becomes_other_and_is_problem(self):
        result = clean({"name":"gopi","phone":"9000000019","email":"gopi@example.com","year":4,"branch":"BIO"})
        self.assertEqual(result["branch"], "other")
        self.assertIn("Invalid or missing branch", is_valid(result))

    def test_fact_check_rejects_invented_phone(self):
        checked = check_facts("Call me at 9840012345", {
            "name":"A", "phone":"9999999999", "email":None, "year":1, "branch":"CSE"
        })
        self.assertIsNone(checked["phone"])


if __name__ == "__main__":
    unittest.main()
