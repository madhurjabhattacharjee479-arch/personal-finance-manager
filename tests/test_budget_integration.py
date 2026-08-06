from decimal import Decimal

from src.budget import Budget
from src.budget_manager import BudgetManager


def test_budget_manager_persistence(tmp_path):
    """Test BudgetManager save/load integration."""

    test_file = tmp_path / "integration_budgets.json"

    manager = BudgetManager()

    budget = Budget(
        month=7,
        year=2026,
        amount=20000,
    )

    manager.add_budget(budget)

    manager.save(test_file)

    new_manager = BudgetManager()
    new_manager.load(test_file)

    assert len(new_manager.get_all_budgets()) == 1

    loaded_budget = new_manager.get_budget(
        month=7,
        year=2026,
    )

    assert loaded_budget is not None
    assert loaded_budget.month == 7
    assert loaded_budget.year == 2026
    assert loaded_budget.amount == Decimal("20000.00")


def test_budget_manager_remove_after_load(tmp_path):
    """Test removing a loaded budget."""

    test_file = tmp_path / "integration_budgets.json"

    manager = BudgetManager()

    manager.add_budget(
        Budget(
            month=7,
            year=2026,
            amount=20000,
        )
    )

    manager.save(test_file)

    new_manager = BudgetManager()
    new_manager.load(test_file)

    removed = new_manager.remove_budget(
        month=7,
        year=2026,
    )

    assert removed is True
    assert new_manager.get_budget(
        7,
        2026,
    ) is None