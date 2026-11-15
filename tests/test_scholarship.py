"""Tests for student_scholarship_system.py (stdlib unittest, no dependencies)."""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import student_scholarship_system as s  # noqa: E402


def run_program(*answers):
    """Run main() with scripted input; return everything printed."""
    buf = io.StringIO()
    with patch("builtins.input", side_effect=list(answers)), redirect_stdout(buf):
        s.main()
    return buf.getvalue()


class TestEvaluate(unittest.TestCase):
    def test_full_scholarship(self):
        self.assertEqual(s.evaluate(95, 90, 40000), ("Full Scholarship", []))

    def test_partial_scholarship(self):
        self.assertEqual(s.evaluate(85, 88, 50000), ("Partial Scholarship", []))

    def test_all_three_criteria_fail(self):
        scholarship, reasons = s.evaluate(70, 80, 60000)
        self.assertEqual(scholarship, "None")
        self.assertEqual(len(reasons), 3)

    # ---- exact boundaries ----
    def test_marks_exactly_90_is_full(self):
        self.assertEqual(s.evaluate(90, 85, 50000)[0], "Full Scholarship")

    def test_marks_just_below_90_is_partial(self):
        self.assertEqual(s.evaluate(89.99, 85, 50000)[0], "Partial Scholarship")

    def test_marks_exactly_80_is_eligible(self):
        self.assertEqual(s.evaluate(80, 85, 50000)[0], "Partial Scholarship")

    def test_marks_just_below_80_fails(self):
        self.assertEqual(len(s.evaluate(79.99, 90, 1000)[1]), 1)

    def test_attendance_boundary(self):
        self.assertEqual(s.evaluate(90, 85, 1000)[1], [])
        self.assertEqual(len(s.evaluate(90, 84.99, 1000)[1]), 1)

    def test_income_boundary(self):
        self.assertEqual(s.evaluate(90, 90, 50000)[1], [])
        self.assertEqual(len(s.evaluate(90, 90, 50001)[1]), 1)

    def test_high_marks_do_not_override_other_failures(self):
        scholarship, reasons = s.evaluate(99, 50, 1000)
        self.assertEqual(scholarship, "None")
        self.assertEqual(len(reasons), 1)
        self.assertIn("Attendance", reasons[0])

    def test_fractional_income_is_not_rounded_into_a_confusing_message(self):
        reasons = s.evaluate(90, 90, 50000.5)[1]
        self.assertEqual(len(reasons), 1)
        self.assertIn("50,000.50", reasons[0])

    def test_each_single_failure_is_reported_alone(self):
        self.assertIn("Marks", s.evaluate(50, 90, 1000)[1][0])
        self.assertIn("Attendance", s.evaluate(90, 50, 1000)[1][0])
        self.assertIn("income", s.evaluate(90, 90, 99999)[1][0])


class TestValidation(unittest.TestCase):
    def test_name_validation(self):
        for good in ("Ali Khan", "Mary-Jane", "O'Brien", "A. Rahman"):
            self.assertTrue(s.is_valid_name(good), good)
        for bad in ("", "   ", "Ali123", "---", "'", "R2D2"):
            self.assertFalse(s.is_valid_name(bad), bad)

    def test_get_number_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "150", "-5", "nan", "inf", "75"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(s.get_number("x: ", 0, 100), 75.0)

    def test_get_number_accepts_range_ends(self):
        with patch("builtins.input", side_effect=["0"]), redirect_stdout(io.StringIO()):
            self.assertEqual(s.get_number("x: ", 0, 100), 0.0)
        with patch("builtins.input", side_effect=["100"]), redirect_stdout(io.StringIO()):
            self.assertEqual(s.get_number("x: ", 0, 100), 100.0)

    def test_income_has_no_upper_limit(self):
        with patch("builtins.input", side_effect=["9999999"]), redirect_stdout(io.StringIO()):
            self.assertEqual(s.get_number("x: ", 0), 9999999.0)

    def test_get_name_title_cases_and_reprompts(self):
        with patch("builtins.input", side_effect=["", "123", "ali khan"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(s.get_name(), "Ali Khan")


class TestEndToEnd(unittest.TestCase):
    def test_full_run_full_scholarship(self):
        out = run_program("ali khan", "95", "90", "40000", "n")
        self.assertIn("Ali Khan", out)
        self.assertIn("ELIGIBLE", out)
        self.assertIn("Full Scholarship", out)

    def test_full_run_not_eligible_lists_three_reasons(self):
        out = run_program("bilal", "70", "80", "60000", "n")
        self.assertIn("NOT ELIGIBLE", out)
        self.assertEqual(out.count("  - "), 3)

    def test_nan_marks_cannot_win_a_scholarship(self):
        out = run_program("ali", "nan", "85", "90", "1000", "n")
        self.assertIn("Partial Scholarship", out)  # marks 85 after re-prompt
        self.assertNotIn("nan%", out)

    def test_evaluates_multiple_students_in_one_run(self):
        out = run_program("ali", "95", "90", "1000", "y",
                          "sara", "60", "90", "1000", "n")
        self.assertEqual(out.count("SCHOLARSHIP EVALUATION REPORT"), 2)
        self.assertIn("Goodbye!", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
