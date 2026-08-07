from decimal import Decimal

import pytest

from src.expense import Expense
from src.reports import (
    calculate_average,
    calculate_total,
    category_summary,
    find_highest_expense,
    find_lowest_expense,
    monthly_summary,
)

# ========================================
# TEST DATA
# ========================================


@pytest.fixture
def sample_expenses():
    return [
        Expense(
            45.50,
            "Food",
            "2026-07-26",
            "Lunch at cafe",
        ),
        Expense(
            120.00,
            "Transport",
            "2026-07-25",
            "Bus pass",
        ),
        Expense(
            350.00,
            "Entertainment",
            "2026-07-24",
            "Movie tickets",
        ),
        Expense(
            250.00,
            "Food",
            "2026-06-24",
            "Groceries",
        ),
        Expense(
            750.00,
            "Shopping",
            "2026-07-19",
            "Backpack",
        ),
    ]


# ========================================
# TOTAL SPENDING TESTS
# ========================================


def test_calculate_total(sample_expenses):
    total = calculate_total(sample_expenses)

    assert total == Decimal("1515.50")


def test_calculate_total_empty_list():
    assert calculate_total([]) == Decimal("0.00")


# ========================================
# AVERAGE SPENDING TESTS
# ========================================


def test_calculate_average(sample_expenses):
    average = calculate_average(sample_expenses)

    assert average == Decimal("303.10")


def test_calculate_average_empty_list():
    assert calculate_average([]) == Decimal("0.00")


# ========================================
# CATEGORY SUMMARY TESTS
# ========================================


def test_category_summary(sample_expenses):
    summary = category_summary(sample_expenses)

    assert summary["Food"]["count"] == 2
    assert summary["Food"]["total"] == Decimal("295.50")
    assert summary["Food"]["average"] == Decimal("147.75")

    assert summary["Transport"]["count"] == 1
    assert summary["Transport"]["total"] == Decimal("120.00")

    assert summary["Entertainment"]["count"] == 1
    assert summary["Entertainment"]["total"] == Decimal("350.00")

    assert summary["Shopping"]["count"] == 1
    assert summary["Shopping"]["total"] == Decimal("750.00")


def test_category_summary_empty_list():
    assert category_summary([]) == {}


# ========================================
# MONTHLY SUMMARY TESTS
# ========================================


def test_monthly_summary(sample_expenses):
    report = monthly_summary(
        sample_expenses,
        2026,
        7,
    )

    assert report["count"] == 4
    assert report["total"] == Decimal("1265.50")
    assert report["average"] == Decimal("316.38")


def test_monthly_summary_different_month(sample_expenses):
    report = monthly_summary(
        sample_expenses,
        2026,
        6,
    )

    assert report["count"] == 1
    assert report["total"] == Decimal("250.00")
    assert report["average"] == Decimal("250.00")


def test_monthly_summary_no_matching_expenses(sample_expenses):
    report = monthly_summary(
        sample_expenses,
        2025,
        1,
    )

    assert report["count"] == 0
    assert report["total"] == Decimal("0.00")
    assert report["average"] == Decimal("0.00")


# ========================================
# HIGHEST EXPENSE TESTS
# ========================================


def test_find_highest_expense(sample_expenses):
    highest = find_highest_expense(sample_expenses)

    assert highest is not None
    assert highest.amount == Decimal("750.00")
    assert highest.category == "Shopping"


def test_find_highest_expense_empty_list():
    assert find_highest_expense([]) is None


# ========================================
# LOWEST EXPENSE TESTS
# ========================================


def test_find_lowest_expense(sample_expenses):
    lowest = find_lowest_expense(sample_expenses)

    assert lowest is not None
    assert lowest.amount == Decimal("45.50")
    assert lowest.category == "Food"


def test_find_lowest_expense_empty_list():
    assert find_lowest_expense([]) is None
