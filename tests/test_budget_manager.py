from decimal import Decimal

from src.budget import Budget
from src.budget_manager import BudgetManager
from src.expense import Expense


def sample_expenses():
    return [
        Expense(
            4000,
            "Food",
            "2026-07-05",
            "Groceries",
        ),
        Expense(
            3000,
            "Shopping",
            "2026-07-10",
            "Clothes",
        ),
        Expense(
            2000,
            "Transport",
            "2026-07-15",
            "Travel",
        ),
    ]


def test_budget_status_warning():
    """Budget utilisation should report WARNING at 90%."""

    expenses = sample_expenses()

    manager = BudgetManager()

    manager.add_budget(
        Budget(
            month=7,
            year=2026,
            amount=10000,
        )
    )

    status = manager.calculate_budget_status(
        expenses,
        month=7,
        year=2026,
    )

    assert status["budget"] == Decimal("10000.00")
    assert status["spent"] == Decimal("9000.00")
    assert status["remaining"] == Decimal("1000.00")
    assert status["utilisation"] == Decimal("90.00")
    assert status["status"] == "WARNING"


def test_budget_status_exceeded():
    """Budget should report EXCEEDED after overspending."""

    expenses = sample_expenses()

    expenses.append(
        Expense(
            2000,
            "Entertainment",
            "2026-07-20",
            "Movie",
        )
    )

    manager = BudgetManager()

    manager.add_budget(
        Budget(
            month=7,
            year=2026,
            amount=10000,
        )
    )

    status = manager.calculate_budget_status(
        expenses,
        month=7,
        year=2026,
    )

    assert status["budget"] == Decimal("10000.00")
    assert status["spent"] == Decimal("11000.00")
    assert status["remaining"] == Decimal("-1000.00")
    assert status["utilisation"] == Decimal("110.00")
    assert status["status"] == "EXCEEDED"