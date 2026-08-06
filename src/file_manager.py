import csv
from pathlib import Path
from src.expense import Expense

CSV_HEADER = ["Date", "Category", "Amount", "Description"]


def save_expenses(expenses, filename):
    """
    Save a list of Expense objects to a CSV file.
    Creates the file (and parent folders) if they do not exist.
    Each expense is written as one row with a header:
    Date, Category, Amount, Description.
    Args:
        expenses: A list of Expense objects to save.
        filename: Path to the CSV file (string or Path object).
    Raises:
        TypeError: If expenses contains items that are not Expense objects.
        OSError: If the file cannot be written.
    """
    file_path = Path(filename)
    for expense in expenses:
        if not isinstance(expense, Expense):
            raise TypeError(f"Expected Expense object, got {type(expense).__name__}.")
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADER)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(
                    {
                        "Date": expense.date,
                        "Category": expense.category,
                        "Amount": f"{expense.amount:.2f}",
                        "Description": expense.description,
                    }
                )
    except OSError as error:
        raise OSError(f"Unable to save expenses to '{file_path}'.") from error


def load_expenses(filename):
    """
    Load expenses from a CSV file and return them as Expense objects.
    Args:
        filename: Path to the CSV file (string or Path object).
    Returns:
        A list of Expense objects. Returns an empty list if the file
        does not exist or contains only a header row.
    Raises:
        OSError: If the file exists but cannot be read.
        csv.Error: If the CSV file structure is malformed.
        ValueError: If required columns are missing or a row has invalid data.
    """
    file_path = Path(filename)
    if not file_path.exists():
        return []
    expenses = []
    try:
        with file_path.open("r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames is None:
                return []
            missing_columns = set(CSV_HEADER) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(
                    "CSV file is missing required columns: "
                    f"{', '.join(sorted(missing_columns))}"
                )
            for row_number, row in enumerate(reader, start=2):
                try:
                    date = row.get("Date", "").strip()
                    category = row.get("Category", "").strip()
                    amount = row.get("Amount", "").strip()
                    description = row.get("Description", "").strip()
                    if not date or not category or not amount:
                        raise ValueError("Date, Category, and Amount cannot be empty.")
                    expense = Expense(amount, category, date, description)
                    expenses.append(expense)
                except ValueError as error:
                    raise ValueError(
                        f"Invalid expense data on row {row_number}: {error}"
                    ) from error
    except csv.Error as error:
        raise csv.Error(f"Malformed CSV in '{file_path}': {error}") from error
    except OSError as error:
        raise OSError(f"Unable to read expenses from '{file_path}'.") from error
    return expenses
