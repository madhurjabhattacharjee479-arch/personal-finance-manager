from decimal import Decimal, InvalidOperation


class Budget:
    """Represents a monthly budget."""

    def __init__(self, month, year, amount):
        """
        Create a new monthly budget.

        Args:
            month: The budget month (1-12).
            year: The budget year.
            amount: The budget amount.
        """
        self.month = self._validate_month(month)
        self.year = self._validate_year(year)
        self.amount = self._validate_amount(amount)

    @staticmethod
    def _validate_month(month):
        """Validate that the month is between 1 and 12."""
        try:
            month = int(month)
        except (ValueError, TypeError) as error:
            raise ValueError(
                "Month must be a valid number."
            ) from error

        if not 1 <= month <= 12:
            raise ValueError(
                "Month must be between 1 and 12."
            )

        return month

    @staticmethod
    def _validate_year(year):
        """Validate the budget year."""
        try:
            year = int(year)
        except (ValueError, TypeError) as error:
            raise ValueError(
                "Year must be a valid number."
            ) from error

        if year < 2000:
            raise ValueError(
                "Year must be 2000 or later."
            )

        return year

    @staticmethod
    def _validate_amount(amount):
        """Validate and convert budget amount to Decimal."""
        try:
            amount = Decimal(str(amount)).quantize(
                Decimal("0.01")
            )
        except (InvalidOperation, ValueError, TypeError) as error:
            raise ValueError(
                "Budget amount must be a valid number."
            ) from error

        if amount <= 0:
            raise ValueError(
                "Budget amount must be greater than zero."
            )

        return amount

    def __str__(self):
        """Return a human-readable representation."""
        return (
            f"{self.year}-{self.month:02d} | "
            f"Budget: {self.amount:.2f}"
        )