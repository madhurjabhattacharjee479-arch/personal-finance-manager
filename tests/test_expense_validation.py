from src.expense import Expense


def check_invalid(label, create_expense):
    """Try to create an expense and expect ValueError."""
    try:
        create_expense()
        print(f"  FAIL: {label} should have raised ValueError")
    except ValueError as error:
        print(f"  PASS: {label} rejected -> {error}")


def main():
    print("=== Expense Validation Tests ===\n")

    # Valid expense
    expense = Expense(
        amount=45.50,
        category="food",  # lowercase input
        date="2026-07-26",
        description="Lunch at cafe",
    )
    print("Valid expense created:")
    print(f"  {expense}")
    print(f"  Category stored as: {expense.category!r}\n")

    # Invalid inputs
    print("--- Invalid Input Tests ---")
    check_invalid(
        "amount",
        lambda: Expense("abc", "Food", "2026-07-26", "Test"),
    )
    check_invalid(
        "date",
        lambda: Expense(10, "Food", "2026-02-30", "Test"),
    )
    check_invalid(
        "category",
        lambda: Expense(10, "Bills", "2026-07-26", "Test"),
    )
    check_invalid(
        "description",
        lambda: Expense(10, "Food", "2026-07-26", "   "),
    )


if __name__ == "__main__":
    main()
