"""
Student Scholarship Eligibility System
Topic: Conditional Statements (if, elif, else)

Evaluates a student's eligibility for a university scholarship based on
academic marks, attendance and monthly family income.

Rules
-----
* Marks       >= 80 %      * Attendance >= 85 %      * Income <= Rs. 50,000
* All met and marks >= 90  -> Full Scholarship
* All met and marks 80-89  -> Partial Scholarship
* Otherwise                -> Not eligible (every failed criterion is listed)
"""

import math

# ---- Eligibility criteria (kept as constants so they are easy to change) ----
MIN_MARKS = 80          # minimum academic marks (%)
FULL_SCHOLARSHIP = 90   # marks (%) at or above this earn a full scholarship
MIN_ATTENDANCE = 85     # minimum attendance (%)
MAX_INCOME = 50000      # maximum monthly family income (Rs.)

# Characters allowed in a name besides letters and spaces (e.g. Mary-Jane, O'Brien)
NAME_EXTRAS = "-'."


def is_valid_name(name):
    """True if the name has at least one letter and only letters, spaces, - ' ."""
    cleaned = name
    for ch in " " + NAME_EXTRAS:
        cleaned = cleaned.replace(ch, "")
    return cleaned.isalpha()


def get_name():
    """Ask for the student's name until a valid one is given."""
    while True:
        name = input("Enter student name: ").strip()
        if name and is_valid_name(name):
            return name.title()
        print("  Invalid name. Use letters, spaces, hyphens or apostrophes only.")


def get_number(prompt, minimum, maximum=None):
    """Ask for a number until it is numeric, finite and inside the allowed range."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue
        # float() also accepts 'nan' and 'inf'; neither is a meaningful measurement
        if not math.isfinite(value):
            print("  Invalid input. Please enter a real number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            if maximum is not None:
                print(f"  Value must be between {minimum} and {maximum}.")
            else:
                print(f"  Value must be at least {minimum}.")
            continue
        return value


def format_rupees(amount):
    """Whole rupees stay whole (40,000); fractional amounts keep paisas (50,000.50)."""
    return f"{amount:,.0f}" if amount == int(amount) else f"{amount:,.2f}"


def evaluate(marks, attendance, income):
    """Return (scholarship_type, list_of_reasons_for_ineligibility)."""
    reasons = []

    # Check each criterion independently so ALL failures are reported
    if marks < MIN_MARKS:
        reasons.append(f"Marks ({marks:.1f}%) are below the required {MIN_MARKS}%.")
    if attendance < MIN_ATTENDANCE:
        reasons.append(f"Attendance ({attendance:.1f}%) is below the required {MIN_ATTENDANCE}%.")
    if income > MAX_INCOME:
        reasons.append(f"Monthly family income (Rs. {format_rupees(income)}) exceeds Rs. {MAX_INCOME:,}.")

    # Decide the scholarship type
    if reasons:
        return "None", reasons
    elif marks >= FULL_SCHOLARSHIP:
        return "Full Scholarship", reasons
    else:  # marks are 80 to just under 90
        return "Partial Scholarship", reasons


def print_report(name, marks, attendance, income, scholarship, reasons):
    """Display the complete scholarship evaluation report."""
    line = "=" * 52
    print("\n" + line)
    print("        SCHOLARSHIP EVALUATION REPORT")
    print(line)
    print(f"Student Name          : {name}")
    print(f"Academic Marks        : {marks:.1f}%   (min {MIN_MARKS}%)")
    print(f"Attendance            : {attendance:.1f}%   (min {MIN_ATTENDANCE}%)")
    print(f"Monthly Family Income : Rs. {format_rupees(income)}   (max Rs. {MAX_INCOME:,})")
    print("-" * 52)
    if reasons:
        print("Status                : NOT ELIGIBLE")
        print("Reason(s):")
        for reason in reasons:
            print(f"  - {reason}")
    else:
        print("Status                : ELIGIBLE")
        print(f"Scholarship Awarded   : {scholarship}")
    print(line)


def main():
    print("=== Student Scholarship Eligibility System ===\n")
    while True:
        # 1 & 2. Collect and validate input
        name = get_name()
        marks = get_number("Enter academic marks (%): ", 0, 100)
        attendance = get_number("Enter attendance percentage (%): ", 0, 100)
        income = get_number("Enter monthly family income (Rs.): ", 0)

        # 3-5. Evaluate eligibility
        scholarship, reasons = evaluate(marks, attendance, income)

        # 6. Report
        print_report(name, marks, attendance, income, scholarship, reasons)

        again = input("\nEvaluate another student? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
