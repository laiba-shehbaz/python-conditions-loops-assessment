"""
Smart Pharmacy Inventory & Sales Management System
Topic: Loop Structures (for loop, range(), conditions in loops,
       counters and accumulators)

Processes sales for a number of medicines, updates stock, warns about low
stock and produces a final daily report.
"""

import math

LOW_STOCK_LIMIT = 10  # remaining stock below this needs restocking


def get_int(prompt, minimum):
    """Ask for a whole number >= minimum until valid."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("  Invalid input. Please enter a whole number.")
            continue
        if value < minimum:
            print(f"  Value must be at least {minimum}.")
            continue
        return value


def get_price(prompt):
    """Ask for a finite price greater than zero until valid."""
    while True:
        try:
            value = float(input(prompt).strip())
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue
        # float() also accepts 'nan' and 'inf', which would corrupt revenue totals
        if not math.isfinite(value):
            print("  Invalid input. Please enter a real number.")
            continue
        if value <= 0:
            print("  Price must be greater than 0.")
            continue
        return value


def get_medicine_name():
    """Ask for a non-empty medicine name."""
    while True:
        name = input("Medicine name: ").strip()
        if name:
            return name.title()
        print("  Name cannot be empty.")


def process_sale(stock, price, quantity):
    """Apply one sale to one medicine.

    Returns (accepted, sale_amount, remaining_stock, needs_restock).
    A sale larger than the available stock is rejected and stock is unchanged.
    """
    if quantity > stock:
        accepted, sale_amount, remaining = False, 0.0, stock
    else:
        accepted, sale_amount, remaining = True, quantity * price, stock - quantity
    return accepted, sale_amount, remaining, remaining < LOW_STOCK_LIMIT


def main():
    print("=== Smart Pharmacy Inventory & Sales Management System ===\n")

    # 1. How many medicines to process
    total_medicines = get_int("How many different medicines to process? ", 1)

    # Accumulators and counters
    total_revenue = 0.0     # accumulator: money earned
    restock_count = 0       # counter: medicines needing restock
    sold_count = 0          # counter: successful sales
    failed_count = 0        # counter: rejected sales
    restock_list = []       # names of medicines to restock

    # 2. Process each medicine with a for loop
    for i in range(1, total_medicines + 1):
        print(f"\n--- Medicine {i} of {total_medicines} ---")

        # 3. Collect details (validated)
        name = get_medicine_name()
        stock = get_int("Available stock (units): ", 0)
        price = get_price("Price per unit (Rs.): ")
        quantity = get_int("Quantity sold: ", 0)

        # 4-6. Check stock, compute sale amount and remaining stock
        accepted, sale_amount, remaining, needs_restock = process_sale(stock, price, quantity)

        if not accepted:
            print(f"  [!] Sale rejected: only {stock} unit(s) of {name} in stock.")
            failed_count += 1
        else:
            total_revenue += sale_amount
            sold_count += 1
            print(f"  Sale amount     : Rs. {sale_amount:,.2f}")
            print(f"  Remaining stock : {remaining} unit(s)")

        # 7 & 9. Low-stock warning and restock counter
        if needs_restock:
            print(f"  [WARNING] Low stock for {name}! Only {remaining} left.")
            restock_count += 1
            restock_list.append(name)

    # 10. Final report
    line = "=" * 50
    print("\n" + line)
    print("        DAILY PHARMACY REPORT")
    print(line)
    print(f"Total medicines processed    : {total_medicines}")
    print(f"Successful sales             : {sold_count}")
    print(f"Rejected sales (low stock)   : {failed_count}")
    print(f"Total revenue                : Rs. {total_revenue:,.2f}")
    print(f"Medicines requiring restock  : {restock_count}")
    if restock_list:
        print("Restock list                 : " + ", ".join(restock_list))
    print(line)


if __name__ == "__main__":
    main()
