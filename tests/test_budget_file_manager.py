from decimal import Decimal
from pathlib import Path

from src.budget import Budget
from src.budget_file_manager import (
    load_budgets,
    save_budgets,
)


def test_save_and_load_budgets(tmp_path):
    test_file = tmp_path / "budgets.json"

    budgets = [
        Budget(7, 2026, 20000),
        Budget(8, 2026, 25000),
    ]

    save_budgets(
        budgets,
        test_file,
    )

    loaded = load_budgets(test_file)

    assert len(loaded) == 2

    assert loaded[0].month == 7
    assert loaded[0].year == 2026
    assert loaded[0].amount == Decimal("20000.00")

    assert loaded[1].month == 8
    assert loaded[1].year == 2026
    assert loaded[1].amount == Decimal("25000.00")

    assert isinstance(
        loaded[0].amount,
        Decimal,
    )


def test_load_missing_budget_file(tmp_path):
    missing = tmp_path / "missing.json"

    assert load_budgets(missing) == []
