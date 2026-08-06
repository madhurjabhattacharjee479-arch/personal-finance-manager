from decimal import Decimal
from pathlib import Path

from src.budget import Budget
from src.budget_file_manager import (
    load_budgets,
    save_budgets,
)
from src.reports import monthly_summary


BUDGETS_FILE = Path("data/budgets.json")


class BudgetManager:
    """Manage budgets and calculate spending against them."""

    WARNING_THRESHOLD = Decimal("80.00")

    def __init__(self, budgets=None):
        """
        Create a BudgetManager.

        Args:
            budgets: Optional list of existing Budget objects.
        """
        self.budgets = budgets if budgets is not None else []

    def add_budget(self, budget):
        """
        Add a new budget.

        Raises:
            TypeError: If the provided object is not a Budget.
            ValueError: If a budget already exists for the same month/year.
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                "Only Budget objects can be added."
            )

        for existing_budget in self.budgets:
            if (
                existing_budget.month == budget.month
                and existing_budget.year == budget.year
            ):
                raise ValueError(
                    f"A budget already exists for "
                    f"{budget.year}-{budget.month:02d}."
                )

        self.budgets.append(budget)

    def remove_budget(self, month, year):
        """
        Remove a budget for a specific month and year.

        Returns:
            True if a budget was removed, otherwise False.
        """
        for index, budget in enumerate(self.budgets):
            if (
                budget.month == month
                and budget.year == year
            ):
                self.budgets.pop(index)
                return True

        return False

    def get_budget(self, month, year):
        """
        Find a budget for a specific month and year.

        Returns:
            Budget object if found, otherwise None.
        """
        for budget in self.budgets:
            if (
                budget.month == month
                and budget.year == year
            ):
                return budget

        return None

    def calculate_budget_status(
        self,
        expenses,
        month,
        year
    ):
        """
        Calculate spending status for a monthly budget.

        Returns:
            A dictionary containing budget information.
            Returns None if no budget exists.
        """
        budget = self.get_budget(month, year)

        if budget is None:
            return None

        report = monthly_summary(
            expenses,
            year,
            month
        )

        spent = report["total"]
        budget_amount = budget.amount

        remaining = budget_amount - spent

        utilisation = (
            (spent / budget_amount) * Decimal("100")
        ).quantize(Decimal("0.01"))

        if spent > budget_amount:
            status = "EXCEEDED"
        elif utilisation >= self.WARNING_THRESHOLD:
            status = "WARNING"
        else:
            status = "OK"

        return {
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "utilisation": utilisation,
            "status": status,
        }

    def get_all_budgets(self):
        """
        Return all stored budgets.
        """
        return self.budgets

    def save(self, filename=BUDGETS_FILE):
        """
        Save all current budgets to JSON.
        """
        save_budgets(
            self.budgets,
            filename
        )

    def load(self, filename=BUDGETS_FILE):
        """
        Load budgets from JSON and replace
        the current in-memory budget list.
        """
        self.budgets = load_budgets(filename)
