from src.utils import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
)


class Expense:
    """Represents a single expense in the Personal Finance Manager."""

    def __init__(self, amount, category, date, description):
        """
        Create a new Expense object.

        Args:
            amount: The expense amount (int, float, or numeric string).
            category: The expense category (e.g. "Food", "Transport").
            date: The expense date in YYYY-MM-DD format.
            description: A short note about the expense.
        """
        self.amount = validate_amount(amount)
        self.category = validate_category(category)
        self.date = validate_date(date)
        self.description = validate_description(description)

    def __str__(self):
        """Return a clean, human-readable string for this expense."""
        return (
            f"{self.date} | {self.category} | "
            f"{self.amount:.2f} | {self.description}"
        )