from pathlib import Path

from src.budget_manager import BudgetManager
from src.config import load_settings
from src.file_manager import load_expenses, save_expenses
from src.menu import run_menu

DATA_FILE = Path("data/expenses.csv")
BUDGETS_FILE = Path("data/budgets.json")


def main():
    print("=== Personal Finance Manager ===")

    # Load saved user settings, including currency preference
    load_settings()

    # Load expenses from CSV
    try:
        expenses = load_expenses(DATA_FILE)
        print(f"Loaded {len(expenses)} expense(s).")
    except (OSError, ValueError) as error:
        print(f"Error loading expenses: {error}")
        expenses = []

    # Create BudgetManager and load saved budgets
    budget_manager = BudgetManager()

    try:
        budget_manager.load(BUDGETS_FILE)
        print(f"Loaded " f"{len(budget_manager.get_all_budgets())} " f"budget(s).")
    except (OSError, ValueError) as error:
        print(f"Error loading budgets: {error}")

    # Run the interactive application
    run_menu(expenses, budget_manager)

    # Save all expenses when the user exits
    try:
        save_expenses(expenses, DATA_FILE)
        print(f"\n✅ Saved " f"{len(expenses)} expense(s).")
    except (OSError, TypeError) as error:
        print(f"\n❌ Error saving expenses: " f"{error}")

    # Save all budgets when the user exits
    try:
        budget_manager.save(BUDGETS_FILE)
        print(f"✅ Saved " f"{len(budget_manager.get_all_budgets())} " f"budget(s).")
    except (OSError, TypeError) as error:
        print(f"❌ Error saving budgets: " f"{error}")


if __name__ == "__main__":
    main()
