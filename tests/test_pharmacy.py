"""Tests for pharmacy_inventory_system.py (stdlib unittest, no dependencies)."""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pharmacy_inventory_system as p  # noqa: E402


def run_program(*answers):
    buf = io.StringIO()
    with patch("builtins.input", side_effect=list(answers)), redirect_stdout(buf):
        p.main()
    return buf.getvalue()


class TestProcessSale(unittest.TestCase):
    def test_successful_sale(self):
        self.assertEqual(p.process_sale(100, 5, 20), (True, 100.0, 80, False))

    def test_sale_leaving_low_stock(self):
        self.assertEqual(p.process_sale(15, 50, 10), (True, 500.0, 5, True))

    def test_rejected_sale_keeps_stock_and_earns_nothing(self):
        self.assertEqual(p.process_sale(8, 12, 9), (False, 0.0, 8, True))

    def test_selling_exactly_all_stock_is_accepted(self):
        accepted, amount, remaining, restock = p.process_sale(10, 2, 10)
        self.assertTrue(accepted)
        self.assertEqual((amount, remaining, restock), (20.0, 0, True))

    def test_low_stock_boundary(self):
        self.assertFalse(p.process_sale(20, 1, 10)[3])  # remaining 10 -> OK
        self.assertTrue(p.process_sale(20, 1, 11)[3])   # remaining 9  -> restock

    def test_zero_quantity_sale(self):
        self.assertEqual(p.process_sale(50, 3, 0), (True, 0.0, 50, False))

    def test_decimal_price(self):
        self.assertAlmostEqual(p.process_sale(100, 2.5, 4)[1], 10.0)


class TestValidation(unittest.TestCase):
    def test_get_int_reprompts(self):
        with patch("builtins.input", side_effect=["abc", "1.5", "0", "-2", "3"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(p.get_int("n: ", 1), 3)

    def test_get_int_allows_zero_when_minimum_is_zero(self):
        with patch("builtins.input", side_effect=["0"]), redirect_stdout(io.StringIO()):
            self.assertEqual(p.get_int("n: ", 0), 0)

    def test_get_price_rejects_bad_values(self):
        with patch("builtins.input", side_effect=["x", "0", "-1", "nan", "inf", "7.5"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(p.get_price("p: "), 7.5)

    def test_medicine_name_rejects_empty(self):
        with patch("builtins.input", side_effect=["", "   ", "panadol"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(p.get_medicine_name(), "Panadol")


class TestEndToEnd(unittest.TestCase):
    # The README's worked example: Panadol, Amoxil, Brufen
    SCENARIO = ["3",
                "panadol", "100", "5", "20",
                "amoxil", "15", "50", "10",
                "brufen", "8", "12", "9"]

    def test_readme_scenario_totals(self):
        out = run_program(*self.SCENARIO)
        self.assertIn("Total medicines processed    : 3", out)
        self.assertIn("Successful sales             : 2", out)
        self.assertIn("Rejected sales (low stock)   : 1", out)
        self.assertIn("Total revenue                : Rs. 600.00", out)
        self.assertIn("Medicines requiring restock  : 2", out)
        self.assertIn("Restock list                 : Amoxil, Brufen", out)

    def test_rejection_message_and_warning(self):
        out = run_program(*self.SCENARIO)
        self.assertIn("Sale rejected: only 8 unit(s) of Brufen in stock.", out)
        self.assertIn("[WARNING] Low stock for Amoxil! Only 5 left.", out)

    def test_loop_runs_exactly_n_times(self):
        out = run_program("2", "a", "100", "1", "1", "b", "100", "1", "1")
        self.assertIn("Medicine 1 of 2", out)
        self.assertIn("Medicine 2 of 2", out)
        self.assertNotIn("Medicine 3", out)

    def test_no_restock_list_when_nothing_is_low(self):
        out = run_program("1", "a", "100", "2", "5")
        self.assertIn("Medicines requiring restock  : 0", out)
        self.assertNotIn("Restock list", out)

    def test_revenue_sums_across_medicines(self):
        out = run_program("2", "a", "100", "2.5", "4", "b", "100", "10", "3")
        self.assertIn("Total revenue                : Rs. 40.00", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
