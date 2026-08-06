import json
from pathlib import Path
from decimal import Decimal

from src.budget import Budget

BUDGETS_FILE = Path("data/budgets.json")


def save_budgets(budgets, filename=BUDGETS_FILE):
    """
    Save a list of Budget objects to a JSON file.

    Args:
        budgets: A list of Budget objects.
        filename: Path to the JSON file.

    Raises:
        TypeError: If the list contains a non-Budget object.
        OSError: If the file cannot be written.
    """
    file_path = Path(filename)

    for budget in budgets:
        if not isinstance(budget, Budget):
            raise TypeError(f"Expected Budget object, " f"got {type(budget).__name__}.")

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        budget_data = []

        for budget in budgets:
            budget_data.append(
                {
                    "month": budget.month,
                    "year": budget.year,
                    "amount": str(budget.amount),
                }
            )

        with file_path.open("w", encoding="utf-8") as json_file:
            json.dump(budget_data, json_file, indent=4)

    except OSError as error:
        raise OSError(f"Unable to save budgets to '{file_path}'.") from error


def load_budgets(filename=BUDGETS_FILE):
    """
    Load budgets from a JSON file.

    Returns:
        A list of Budget objects.

    If the file does not exist, an empty list is returned.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If the JSON data is invalid.
    """
    file_path = Path(filename)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as json_file:
            budget_data = json.load(json_file)

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON data in '{file_path}'.") from error

    except OSError as error:
        raise OSError(f"Unable to read budgets from '{file_path}'.") from error

    if not isinstance(budget_data, list):
        raise ValueError("Budget data must be stored as a JSON list.")

    budgets = []

    for index, data in enumerate(budget_data, start=1):
        if not isinstance(data, dict):
            raise ValueError(f"Invalid budget data at item {index}.")

        try:
            month = data["month"]
            year = data["year"]
            amount = Decimal(str(data["amount"]))

            budget = Budget(month=month, year=year, amount=amount)

            budgets.append(budget)

        except KeyError as error:
            raise ValueError(
                f"Missing required budget field " f"at item {index}: {error}"
            ) from error

        except (ValueError, TypeError) as error:
            raise ValueError(
                f"Invalid budget data at item {index}: " f"{error}"
            ) from error

    return budgets
