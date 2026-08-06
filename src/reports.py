from collections import defaultdict
from decimal import Decimal


def calculate_total(expenses):
    """
    Calculate the total amount spent across all expenses.

    Args:
        expenses: A list of Expense objects.

    Returns:
        A Decimal representing the total expenses.
    """
    return sum(
        (expense.amount for expense in expenses),
        Decimal("0.00"),
    )


def calculate_average(expenses):
    """
    Calculate the average expense amount.

    Args:
        expenses: A list of Expense objects.

    Returns:
        A Decimal representing the average expense.
        Returns Decimal('0.00') if there are no expenses.
    """
    if not expenses:
        return Decimal("0.00")

    total = calculate_total(expenses)

    return (total / len(expenses)).quantize(Decimal("0.01"))


def category_summary(expenses):
    """
    Calculate spending statistics for each category.

    Args:
        expenses: A list of Expense objects.

    Returns:
        A dictionary containing the number of expenses,
        total spending, and average spending for each category.
    """
    summary = defaultdict(
        lambda: {
            "count": 0,
            "total": Decimal("0.00"),
        }
    )

    for expense in expenses:
        category = expense.category

        summary[category]["count"] += 1
        summary[category]["total"] += expense.amount

    for category, data in summary.items():
        data["average"] = (data["total"] / data["count"]).quantize(Decimal("0.01"))

    return dict(summary)


def monthly_summary(expenses, year, month):
    """
    Calculate spending statistics for a specific month.

    Args:
        expenses: A list of Expense objects.
        year: The year to analyse.
        month: The month to analyse.

    Returns:
        A dictionary containing the matching expenses,
        count, total, and average.
    """
    matching_expenses = [
        expense
        for expense in expenses
        if expense.date.startswith(f"{year:04d}-{month:02d}")
    ]

    total = calculate_total(matching_expenses)

    average = calculate_average(matching_expenses)

    return {
        "expenses": matching_expenses,
        "count": len(matching_expenses),
        "total": total,
        "average": average,
    }


def find_highest_expense(expenses):
    """
    Find the expense with the highest amount.

    Returns:
        The highest Expense object, or None if the list is empty.
    """
    if not expenses:
        return None

    return max(expenses, key=lambda expense: expense.amount)


def find_lowest_expense(expenses):
    """
    Find the expense with the lowest amount.

    Returns:
        The lowest Expense object, or None if the list is empty.
    """
    if not expenses:
        return None

    return min(expenses, key=lambda expense: expense.amount)
