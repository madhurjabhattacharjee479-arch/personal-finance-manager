from decimal import Decimal

import pytest

from src.expense import Expense

# ========================================
# VALID EXPENSE TESTS
# ========================================


def test_create_valid_expense():
    expense = Expense(
        amount=45.50,
        category="Food",
        date="2026-07-26",
        description="Lunch at cafe",
    )

    assert expense.amount == Decimal("45.50")
    assert expense.category == "Food"
    assert expense.date == "2026-07-26"
    assert expense.description == "Lunch at cafe"


def test_expense_amount_is_decimal():
    expense = Expense(
        amount="120",
        category="Transport",
        date="2026-07-25",
        description="Bus pass",
    )

    assert isinstance(
        expense.amount,
        Decimal,
    )


def test_category_is_normalised():
    expense = Expense(
        amount=100,
        category="food",
        date="2026-07-26",
        description="Lunch",
    )

    assert expense.category == "Food"


# ========================================
# INVALID AMOUNT TESTS
# ========================================


def test_invalid_amount_text():
    with pytest.raises(ValueError):
        Expense(
            amount="abc",
            category="Food",
            date="2026-07-26",
            description="Test",
        )


def test_invalid_amount_zero():
    with pytest.raises(ValueError):
        Expense(
            amount=0,
            category="Food",
            date="2026-07-26",
            description="Test",
        )


def test_invalid_amount_negative():
    with pytest.raises(ValueError):
        Expense(
            amount=-25,
            category="Food",
            date="2026-07-26",
            description="Test",
        )


# ========================================
# INVALID DATE TESTS
# ========================================


def test_invalid_date_format():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="Food",
            date="26-07-2026",
            description="Test",
        )


def test_invalid_calendar_date():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="Food",
            date="2026-02-30",
            description="Test",
        )


# ========================================
# INVALID CATEGORY TESTS
# ========================================


def test_invalid_category():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="Bills",
            date="2026-07-26",
            description="Test",
        )


def test_empty_category():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="",
            date="2026-07-26",
            description="Test",
        )


# ========================================
# INVALID DESCRIPTION TESTS
# ========================================


def test_empty_description():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="Food",
            date="2026-07-26",
            description="",
        )


def test_whitespace_description():
    with pytest.raises(ValueError):
        Expense(
            amount=100,
            category="Food",
            date="2026-07-26",
            description="   ",
        )


# ========================================
# STRING REPRESENTATION TEST
# ========================================


def test_expense_string_representation():
    expense = Expense(
        amount=45.50,
        category="Food",
        date="2026-07-26",
        description="Lunch at cafe",
    )

    assert str(expense) == ("2026-07-26 | Food | 45.50 | Lunch at cafe")
