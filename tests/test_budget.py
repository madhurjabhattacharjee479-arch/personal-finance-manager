from decimal import Decimal

import pytest

from src.budget import Budget


def test_valid_budget():
    """Test creation of a valid budget."""

    budget = Budget(
        month=7,
        year=2026,
        amount=20000,
    )

    assert budget.month == 7
    assert budget.year == 2026
    assert budget.amount == Decimal("20000.00")


@pytest.mark.parametrize(
    "month, year, amount",
    [
        (13, 2026, 20000),      # Invalid month
        (7, 1999, 20000),       # Invalid year
        (7, 2026, "abc"),       # Invalid amount type
        (7, 2026, 0),           # Zero amount
        (7, 2026, -5000),       # Negative amount
    ],
)
def test_invalid_budget(month, year, amount):
    """Invalid budget values should raise ValueError."""

    with pytest.raises(ValueError):
        Budget(
            month=month,
            year=year,
            amount=amount,
        )