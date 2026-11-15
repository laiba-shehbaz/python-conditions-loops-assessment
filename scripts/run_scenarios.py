"""
Run both programs on a fixed set of scenarios and record REAL results.

* Transcripts  -> docs/outputs/*.txt   (what a user sees in a terminal)
* Structured   -> docs/outputs/results.json  (used by generate_visuals.py)

input() is patched to echo the scripted answer after each prompt, exactly like
a terminal does, so the transcripts read like a real session. The programs'
own code paths are executed unchanged.
"""
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "docs", "outputs")
os.makedirs(OUT, exist_ok=True)

import student_scholarship_system as sch   # noqa: E402
import pharmacy_inventory_system as pha    # noqa: E402


def run_session(main, answers):
    """Run main() feeding `answers`; return the terminal-style transcript."""
    answers = iter(answers)
    buf = io.StringIO()

    def fake_input(prompt=""):
        value = next(answers)
        print(f"{prompt}{value}")        # echo like a terminal
        return value

    with patch("builtins.input", fake_input), redirect_stdout(buf):
        main()
    return buf.getvalue()


def save(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(text)


# --------------------------------------------------------------------------
# Task 1 - scholarship scenarios: (label, name, marks, attendance, income)
# --------------------------------------------------------------------------
SCHOLARSHIP_CASES = [
    ("S1 Full scholarship",        "Ali Khan",  95,  90, 40000),
    ("S2 Partial scholarship",     "Sara Noor", 85,  88, 50000),
    ("S3 All criteria fail",       "Bilal",     70,  80, 60000),
    ("S4 Marks boundary (90)",     "Hina",      90,  85, 50000),
    ("S5 Marks boundary (80)",     "Usman",     80,  85, 50000),
    ("S6 Attendance fails only",   "Zara",      92,  84, 30000),
    ("S7 Income fails only",       "Omar",      88,  95, 50001),
    ("S8 Marks fails only",        "Ayesha",    79,  90, 20000),
]

scholarship_results = []
for label, name, m, a, inc in SCHOLARSHIP_CASES:
    award, reasons = sch.evaluate(m, a, inc)
    scholarship_results.append({
        "label": label, "name": name, "marks": m, "attendance": a, "income": inc,
        "award": award, "eligible": not reasons, "reasons": reasons,
        "marks_ok": m >= sch.MIN_MARKS,
        "attendance_ok": a >= sch.MIN_ATTENDANCE,
        "income_ok": inc <= sch.MAX_INCOME,
    })

# Terminal transcripts: three evaluations in one run, then an invalid-input demo
scholarship_main = run_session(sch.main, [
    "ali khan", "95", "90", "40000", "y",
    "bilal", "70", "80", "60000", "y",
    "sara noor", "85", "88", "50000", "n",
])
save("scholarship_session.txt", scholarship_main)

scholarship_invalid = run_session(sch.main, [
    "ali123", "ali khan",
    "abc", "150", "nan", "95",
    "90",
    "-5", "40000",
    "n",
])
save("scholarship_invalid_input.txt", scholarship_invalid)

# --------------------------------------------------------------------------
# Task 2 - pharmacy scenarios
# --------------------------------------------------------------------------
PHARMACY_MEDICINES = [          # name, stock, price, quantity
    ("Panadol", 100, 5, 20),
    ("Amoxil",   15, 50, 10),
    ("Brufen",    8, 12, 9),
]
pharmacy_answers = ["0", "3"]
for n, st, pr, q in PHARMACY_MEDICINES:
    pharmacy_answers += [n.lower(), str(st), str(pr), str(q)]
pharmacy_transcript = run_session(pha.main, pharmacy_answers)
save("pharmacy_session.txt", pharmacy_transcript)

meds, revenue, sold, failed, restock = [], 0.0, 0, 0, []
for n, st, pr, q in PHARMACY_MEDICINES:
    ok, amount, remaining, low = pha.process_sale(st, pr, q)
    revenue += amount
    sold += ok
    failed += (not ok)
    if low:
        restock.append(n)
    meds.append({"name": n, "stock": st, "price": pr, "quantity": q,
                 "accepted": ok, "amount": amount, "remaining": remaining,
                 "low_stock": low})
pharmacy_results = {"medicines": meds, "total_revenue": revenue, "sold": sold,
                    "failed": failed, "restock": restock,
                    "low_stock_limit": pha.LOW_STOCK_LIMIT}

pharmacy_invalid = run_session(pha.main, [
    "x", "-1", "1",
    "", "  ", "dispirin",
    "abc", "50",
    "0", "nan", "-3", "2.5",
    "1.5", "4",
])
save("pharmacy_invalid_input.txt", pharmacy_invalid)

# --------------------------------------------------------------------------
# Test-suite results (run the real tests, count outcomes per class)
# --------------------------------------------------------------------------
suite = unittest.defaultTestLoader.discover(os.path.join(ROOT, "tests"))
per_class = {}


def walk(s):
    for t in s:
        if isinstance(t, unittest.TestSuite):
            walk(t)
        else:
            per_class.setdefault(t.__class__.__module__ + "." + t.__class__.__name__, []).append(t)


walk(suite)
test_summary = {}
total_run = total_fail = 0
for cls, tests in per_class.items():
    res = unittest.TestResult()
    for t in tests:
        t.run(res)
    failed_n = len(res.failures) + len(res.errors)
    test_summary[cls] = {"total": len(tests), "passed": len(tests) - failed_n}
    total_run += len(tests)
    total_fail += failed_n

results = {
    "scholarship": scholarship_results,
    "pharmacy": pharmacy_results,
    "tests": {"by_class": test_summary, "total": total_run, "failed": total_fail},
    "constants": {"MIN_MARKS": sch.MIN_MARKS, "FULL": sch.FULL_SCHOLARSHIP,
                  "MIN_ATT": sch.MIN_ATTENDANCE, "MAX_INCOME": sch.MAX_INCOME,
                  "LOW_STOCK": pha.LOW_STOCK_LIMIT},
}
with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2)

print(f"Scenarios recorded. Tests: {total_run - total_fail}/{total_run} passed.")
