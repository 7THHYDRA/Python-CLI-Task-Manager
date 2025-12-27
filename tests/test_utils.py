import unittest
from task_manager.utils import validate_due_date


class TestUtils(unittest.TestCase):

    def test_valid_due_date(self):
        date = validate_due_date("2025-01-10")
        self.assertEqual(date, "2025-01-10")

    def test_none_due_date(self):
        self.assertIsNone(validate_due_date(None))

    def test_invalid_due_date_format(self):
        with self.assertRaises(ValueError):
            validate_due_date("10-01-2025")


if __name__ == "__main__":
    unittest.main()
