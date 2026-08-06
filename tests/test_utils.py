
from decimal import Decimal

import pytest

from src.utils import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
)


# ========================================
# AMOUNT VALIDATION TESTS
# ========================================

def test_validate_amount_valid():
    assert validate_amount("45.50") == Decimal("45.50")
    assert validate_amount(100) == Decimal("100.00")


def test_validate_amount_invalid_text():
    with pytest.raises(ValueError):
        validate_amount("abc")


def test_validate_amount_zero():
    with pytest.raises(ValueError):
        validate_amount(0)


def test_validate_amount_negative():
    with pytest.raises(ValueError):
        validate_amount(-25)


# ========================================
# DATE VALIDATION TESTS
# ========================================

def test_validate_date_valid():
    assert validate_date("2026-07-26") == "2026-07-26"


def test_validate_date_invalid_format():
    with pytest.raises(ValueError):
        validate_date("26-07-2026")


def test_validate_date_invalid_calendar_date():
    with pytest.raises(ValueError):
        validate_date("2026-02-30")


# ========================================
# CATEGORY VALIDATION TESTS
# ========================================

def test_validate_category_lowercase():
    assert validate_category("food") == "Food"


def test_validate_category_uppercase():
    assert validate_category("FOOD") == "Food"


def test_validate_category_with_spaces():
    assert validate_category("  Transport  ") == "Transport"


def test_validate_category_empty():
    with pytest.raises(ValueError):
        validate_category("")


def test_validate_category_invalid():
    with pytest.raises(ValueError):
        validate_category("Bills")


# ========================================
# DESCRIPTION VALIDATION TESTS
# ========================================

def test_validate_description_valid():
    assert (
        validate_description("  Lunch at cafe  ")
        == "Lunch at cafe"
    )


def test_validate_description_empty():
    with pytest.raises(ValueError):
        validate_description("")


def test_validate_description_whitespace_only():
    with pytest.raises(ValueError):
        validate_description("   ")
