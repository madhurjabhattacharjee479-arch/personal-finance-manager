from decimal import Decimal

import pytest

from src.expense import Expense
from src.file_manager import load_expenses, save_expenses

# ========================================
# SAVE EXPENSES TEST
# ========================================


def test_save_expenses_creates_csv(tmp_path):
    data_file = tmp_path / "expenses.csv"

    expenses = [
        Expense(
            45.50,
            "Food",
            "2026-07-26",
            "Lunch at cafe",
        ),
        Expense(
            "120.00",
            "Transport",
            "2026-07-25",
            "Bus pass",
        ),
    ]

    save_expenses(expenses, data_file)

    assert data_file.exists()


# ========================================
# SAVE AND LOAD TEST
# ========================================


def test_save_and_load_expenses(tmp_path):
    data_file = tmp_path / "expenses.csv"

    expenses = [
        Expense(
            45.50,
            "Food",
            "2026-07-26",
            "Lunch at cafe",
        ),
        Expense(
            120,
            "Transport",
            "2026-07-25",
            "Bus pass",
        ),
    ]

    save_expenses(expenses, data_file)

    loaded_expenses = load_expenses(data_file)

    assert len(loaded_expenses) == 2

    assert loaded_expenses[0].amount == Decimal("45.50")
    assert loaded_expenses[0].category == "Food"
    assert loaded_expenses[0].date == "2026-07-26"
    assert loaded_expenses[0].description == "Lunch at cafe"

    assert loaded_expenses[1].amount == Decimal("120.00")
    assert loaded_expenses[1].category == "Transport"


# ========================================
# DECIMAL PRESERVATION TEST
# ========================================


def test_loaded_amount_is_decimal(tmp_path):
    data_file = tmp_path / "expenses.csv"

    expenses = [
        Expense(
            "45.50",
            "Food",
            "2026-07-26",
            "Lunch",
        )
    ]

    save_expenses(expenses, data_file)

    loaded_expenses = load_expenses(data_file)

    assert isinstance(
        loaded_expenses[0].amount,
        Decimal,
    )

    assert loaded_expenses[0].amount == Decimal("45.50")


# ========================================
# MISSING FILE TEST
# ========================================


def test_load_missing_file_returns_empty_list(tmp_path):
    data_file = tmp_path / "does_not_exist.csv"

    result = load_expenses(data_file)

    assert result == []


# ========================================
# EMPTY CSV TEST
# ========================================


def test_load_empty_csv_returns_empty_list(tmp_path):
    data_file = tmp_path / "empty.csv"

    data_file.write_text(
        "",
        encoding="utf-8",
    )

    result = load_expenses(data_file)

    assert result == []


# ========================================
# HEADER-ONLY CSV TEST
# ========================================


def test_load_header_only_csv_returns_empty_list(tmp_path):
    data_file = tmp_path / "header_only.csv"

    data_file.write_text(
        "Date,Category,Amount,Description\n",
        encoding="utf-8",
    )

    result = load_expenses(data_file)

    assert result == []


# ========================================
# INVALID COLUMN TEST
# ========================================


def test_load_csv_with_missing_column_raises_error(tmp_path):
    data_file = tmp_path / "invalid.csv"

    data_file.write_text(
        "Date,Category,Amount\n" "2026-07-26,Food,45.50\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_expenses(data_file)


# ========================================
# INVALID EXPENSE DATA TEST
# ========================================


def test_load_csv_with_invalid_amount_raises_error(tmp_path):
    data_file = tmp_path / "invalid_amount.csv"

    data_file.write_text(
        "Date,Category,Amount,Description\n" "2026-07-26,Food,abc,Lunch\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_expenses(data_file)


# ========================================
# INVALID CATEGORY TEST
# ========================================


def test_load_csv_with_invalid_category_raises_error(tmp_path):
    data_file = tmp_path / "invalid_category.csv"

    data_file.write_text(
        "Date,Category,Amount,Description\n" "2026-07-26,Bills,45.50,Electricity\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_expenses(data_file)


# ========================================
# MULTIPLE EXPENSES TEST
# ========================================


def test_save_and_load_multiple_expenses(tmp_path):
    data_file = tmp_path / "multiple.csv"

    expenses = [
        Expense(
            45.50,
            "Food",
            "2026-07-26",
            "Lunch",
        ),
        Expense(
            120,
            "Transport",
            "2026-07-25",
            "Bus pass",
        ),
        Expense(
            350,
            "Entertainment",
            "2026-07-24",
            "Movie tickets",
        ),
    ]

    save_expenses(expenses, data_file)

    loaded_expenses = load_expenses(data_file)

    assert len(loaded_expenses) == 3

    assert loaded_expenses[0].description == "Lunch"
    assert loaded_expenses[1].description == "Bus pass"
    assert loaded_expenses[2].description == "Movie tickets"
