from src import budget_manager
from src.expense import Expense
from src.utils import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
)
from datetime import datetime

from src.reports import (
    calculate_total,
    calculate_average,
    category_summary,
    monthly_summary,
    find_highest_expense,
    find_lowest_expense,
)
from src.config import format_money, choose_currency
from src.budget import Budget
from src.charts import (
    generate_category_pie_chart,
    generate_monthly_bar_chart,
)
from src.export import (
    export_to_csv,
    export_to_json,
    export_report,
)
from src.backup import (
    create_backup,
    restore_backup,
)
from pathlib import Path
from src.dashboard import dashboard_menu
from src.file_manager import load_expenses

DATA_FILE = Path("data/expenses.csv")
BUDGETS_FILE = Path("data/budgets.json")

from src.file_manager import save_expenses
DATA_FILE = Path("data/expenses.csv")

def get_valid_input(prompt, validation_function):
    """
    Repeatedly ask the user for input until it passes validation.

    Args:
        prompt: The message displayed to the user.
        validation_function: A function used to validate the input.

    Returns:
        The validated and cleaned value.
    """
    while True:
        value = input(prompt)

        try:
            return validation_function(value)
        except ValueError as error:
            print(f"❌ Invalid input: {error}")
            print("Please try again.\n")
def add_expense(expenses, budget_manager):
    """
    Collect expense details from the user, add a new Expense,
    and check the user's monthly budget status.
    """

    print("\n=== ADD NEW EXPENSE ===")

    # ----------------------------------------
    # 1. GET VALIDATED EXPENSE DETAILS
    # ----------------------------------------

    amount = get_valid_input(
        "Enter amount: ",
        validate_amount,
    )

    category = get_valid_input(
        "Enter category (Food/Transport/Entertainment/Shopping/Other): ",
        validate_category,
    )

    date = get_valid_input(
        "Enter date (YYYY-MM-DD): ",
        validate_date,
    )

    description = get_valid_input(
        "Enter description: ",
        validate_description,
    )

    # ----------------------------------------
    # 2. CREATE THE EXPENSE
    # ----------------------------------------

    expense = Expense(
        amount=amount,
        category=category,
        date=date,
        description=description,
    )

    # Add expense to the list
    expenses.append(expense)

    # Save immediately
    save_expenses(
        expenses,
        DATA_FILE,
    )

    print("\n✅ Expense added successfully!")
    print(f"   {expense}")

    # ----------------------------------------
    # 3. CHECK MONTHLY BUDGET
    # ----------------------------------------

    try:
        expense_date = datetime.strptime(
            expense.date,
            "%Y-%m-%d"
        )

        year = expense_date.year
        month = expense_date.month

        status = budget_manager.calculate_budget_status(
            expenses,
            month,
            year,
        )

        if status is None:
            return

        print(
            f"\n=== BUDGET STATUS: "
            f"{year:04d}-{month:02d} ==="
        )

        print(
            f"Budget: "
            f"{format_money(status['budget'])}"
        )

        print(
            f"Spent: "
            f"{format_money(status['spent'])}"
        )

        print(
            f"Remaining: "
            f"{format_money(status['remaining'])}"
        )

        print(
            f"Budget utilisation: "
            f"{status['utilisation']:.2f}%"
        )

        if status["status"] == "EXCEEDED":

            print("\n🚨 BUDGET EXCEEDED!")

            print(
                f"You are over budget by "
                f"{format_money(abs(status['remaining']))}."
            )

        elif status["status"] == "WARNING":

            print("\n⚠️ BUDGET WARNING!")

            print(
                "You have used 80% or more "
                "of your monthly budget."
            )

        else:

            print(
                "\n✅ Your spending is within "
                "your monthly budget."
            )

    except (ValueError, KeyError, TypeError) as error:

        print(
            f"\n⚠️ Unable to check budget status: "
            f"{error}"
        )
def view_expenses(expenses):
    """
    Display all expenses in a numbered list.
    """
    print("\n=== ALL EXPENSES ===")

    if not expenses:
        print("No expenses found.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. {expense}")
        
def search_expenses(expenses):
    """
    Search expenses by category, description, or date.
    """
    print("\n=== SEARCH EXPENSES ===")

    if not expenses:
        print("No expenses available to search.")
        return

    print("1. Search by Category")
    print("2. Search by Description")
    print("3. Search by Date")
    print("4. Back")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "4":
        return

    if choice not in ("1", "2", "3"):
        print("❌ Invalid choice.")
        return

    search_term = input("Enter search term: ").strip()

    if not search_term:
        print("❌ Search term cannot be empty.")
        return

    matches = []

    for expense in expenses:
        if choice == "1":
            if search_term.lower() in expense.category.lower():
                matches.append(expense)

        elif choice == "2":
            if search_term.lower() in expense.description.lower():
                matches.append(expense)

        elif choice == "3":
            if search_term == expense.date:
                matches.append(expense)

    print("\n=== SEARCH RESULTS ===")

    if not matches:
        print("No matching expenses found.")
        return

    for index, expense in enumerate(matches, start=1):
        print(f"{index}. {expense}")

    print(f"\nFound {len(matches)} matching expense(s).")
    
def delete_expense(expenses):
    """
    Delete an expense selected by the user.

    The user selects an expense by its displayed number
    and confirms the deletion before it is removed.
    """

    print("\n=== DELETE EXPENSE ===")

    # ----------------------------------------
    # 1. CHECK IF EXPENSES EXIST
    # ----------------------------------------

    if not expenses:
        print("No expenses available to delete.")
        return

    # ----------------------------------------
    # 2. DISPLAY ALL EXPENSES
    # ----------------------------------------

    view_expenses(expenses)

    # ----------------------------------------
    # 3. ASK WHICH EXPENSE TO DELETE
    # ----------------------------------------

    while True:

        choice = input(
            "\nEnter the expense number to delete "
            "(or 0 to cancel): "
        ).strip()

        # Validate that the input is a number
        try:
            expense_number = int(choice)

        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        # Allow cancellation
        if expense_number == 0:
            print("Deletion cancelled.")
            return

        # Validate number range
        if (
            expense_number < 1
            or expense_number > len(expenses)
        ):
            print(
                f"❌ Please enter a number between "
                f"1 and {len(expenses)}."
            )
            continue

        break

    # ----------------------------------------
    # 4. GET SELECTED EXPENSE
    # ----------------------------------------

    selected_expense = expenses[
        expense_number - 1
    ]

    print("\nYou selected:")
    print(f"  {selected_expense}")

    # ----------------------------------------
    # 5. ASK FOR CONFIRMATION
    # ----------------------------------------

    while True:

        confirmation = input(
            "\nAre you sure you want to delete "
            "this expense? (y/n): "
        ).strip().lower()

        if confirmation == "y":

            # Delete the selected expense
            expenses.pop(
                expense_number - 1
            )

            # Save updated list immediately
            save_expenses(
                expenses,
                DATA_FILE,
            )

            print(
                "\n✅ Expense deleted successfully!"
            )

            return

        elif confirmation == "n":

            print(
                "\nDeletion cancelled."
            )

            return

        else:

            print(
                "❌ Please enter 'y' for yes "
                "or 'n' for no."
            )
            
def edit_expense(expenses):
    """
    Edit an existing expense selected by the user.

    The user selects an expense by its displayed number,
    enters new values, and the updated expense replaces
    the original expense in the list.
    """

    print("\n=== EDIT EXPENSE ===")

    # ----------------------------------------
    # 1. CHECK IF EXPENSES EXIST
    # ----------------------------------------

    if not expenses:
        print("No expenses available to edit.")
        return

    # ----------------------------------------
    # 2. DISPLAY ALL EXPENSES
    # ----------------------------------------

    view_expenses(expenses)

    # ----------------------------------------
    # 3. ASK WHICH EXPENSE TO EDIT
    # ----------------------------------------

    while True:

        choice = input(
            "\nEnter the expense number to edit "
            "(or 0 to cancel): "
        ).strip()

        try:
            expense_number = int(choice)

        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        # Allow cancellation
        if expense_number == 0:
            print("Edit cancelled.")
            return

        # Validate expense number
        if (
            expense_number < 1
            or expense_number > len(expenses)
        ):
            print(
                f"❌ Please enter a number between "
                f"1 and {len(expenses)}."
            )
            continue

        break

    # ----------------------------------------
    # 4. GET SELECTED EXPENSE
    # ----------------------------------------

    selected_expense = expenses[
        expense_number - 1
    ]

    print("\nCurrent expense:")
    print(f"  {selected_expense}")

    # ----------------------------------------
    # 5. GET NEW VALIDATED DETAILS
    # ----------------------------------------

    print("\nEnter the new details:")

    amount = get_valid_input(
        "Enter new amount: ",
        validate_amount,
    )

    category = get_valid_input(
        "Enter new category "
        "(Food/Transport/Entertainment/Shopping/Other): ",
        validate_category,
    )

    date = get_valid_input(
        "Enter new date (YYYY-MM-DD): ",
        validate_date,
    )

    description = get_valid_input(
        "Enter new description: ",
        validate_description,
    )

    # ----------------------------------------
    # 6. CREATE UPDATED EXPENSE
    # ----------------------------------------

    updated_expense = Expense(
        amount=amount,
        category=category,
        date=date,
        description=description,
    )

    # ----------------------------------------
    # 7. REPLACE OLD EXPENSE
    # ----------------------------------------

    expenses[
        expense_number - 1
    ] = updated_expense

    # ----------------------------------------
    # 8. SAVE IMMEDIATELY
    # ----------------------------------------

    save_expenses(
        expenses,
        DATA_FILE,
    )

    print("\n✅ Expense updated successfully!")
    print(f"Updated expense: {updated_expense}")
    
def reports_menu(expenses, budget_manager):
    """
    Display the reports and analytics submenu.
    """

    while True:
        print("\n" + "=" * 40)
        print("       REPORTS & ANALYTICS")
        print("=" * 40)
        print("1. Total & Average Spending")
        print("2. Category-wise Summary")
        print("3. Monthly Report")
        print("4. Highest & Lowest Expense")
        print("5. Budget Status")
        print("6. Back to Main Menu")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-6): "
        ).strip()

        # ----------------------------------------
        # 1. TOTAL & AVERAGE SPENDING
        # ----------------------------------------
        if choice == "1":
            total = calculate_total(expenses)
            average = calculate_average(expenses)

            print(
                "\n=== TOTAL & AVERAGE SPENDING ==="
            )

            print(
                f"Total spending: "
                f"{format_money(total)}"
            )

            print(
                f"Average expense: "
                f"{format_money(average)}"
            )

        # ----------------------------------------
        # 2. CATEGORY-WISE SUMMARY
        # ----------------------------------------
        elif choice == "2":
            summary = category_summary(expenses)

            print(
                "\n=== CATEGORY-WISE SUMMARY ==="
            )

            if not summary:
                print(
                    "No expenses available."
                )
                continue

            for category, data in summary.items():
                print(f"\n{category}")

                print(
                    f"  Number of expenses: "
                    f"{data['count']}"
                )

                print(
                    f"  Total spending: "
                    f"{format_money(data['total'])}"
                )

                print(
                    f"  Average spending: "
                    f"{format_money(data['average'])}"
                )

        # ----------------------------------------
        # 3. MONTHLY REPORT
        # ----------------------------------------
        elif choice == "3":
            year_input = input(
                "Enter year (YYYY): "
            ).strip()

            month_input = input(
                "Enter month (1-12): "
            ).strip()

            try:
                year = int(year_input)
                month = int(month_input)

                if month < 1 or month > 12:
                    print(
                        "❌ Month must be between "
                        "1 and 12."
                    )
                    continue

                report = monthly_summary(
                    expenses,
                    year,
                    month,
                )

                print(
                    f"\n=== MONTHLY REPORT: "
                    f"{year:04d}-{month:02d} ==="
                )

                print(
                    f"Number of expenses: "
                    f"{report['count']}"
                )

                print(
                    f"Total spent: "
                    f"{format_money(report['total'])}"
                )

                print(
                    f"Average expense: "
                    f"{format_money(report['average'])}"
                )

            except ValueError:
                print(
                    "❌ Please enter valid numbers."
                )

        # ----------------------------------------
        # 4. HIGHEST & LOWEST EXPENSE
        # ----------------------------------------
        elif choice == "4":
            highest = find_highest_expense(
                expenses
            )

            lowest = find_lowest_expense(
                expenses
            )

            print(
                "\n=== HIGHEST & LOWEST EXPENSE ==="
            )

            if highest is None:
                print(
                    "No expenses available."
                )
                continue

            print(
                "\nHighest Expense:"
            )

            print(
                f"  {highest}"
            )

            print(
                "\nLowest Expense:"
            )

            print(
                f"  {lowest}"
            )

        # ----------------------------------------
        # 5. BUDGET STATUS
        # ----------------------------------------
        elif choice == "5":
            print(
                "\n=== BUDGET STATUS ==="
            )

            try:
                year = int(
                    input(
                        "Enter year (YYYY): "
                    ).strip()
                )

                month = int(
                    input(
                        "Enter month (1-12): "
                    ).strip()
                )

                if month < 1 or month > 12:
                    print(
                        "❌ Month must be between "
                        "1 and 12."
                    )
                    continue

                status = (
                    budget_manager
                    .calculate_budget_status(
                        expenses,
                        month,
                        year,
                    )
                )

                if status is None:
                    print(
                        f"\n❌ No budget found for "
                        f"{year}-{month:02d}."
                    )
                    print(
                        "Set a budget first from "
                        "Budget Management."
                    )
                    continue

                print(
                    f"\n=== BUDGET STATUS: "
                    f"{year:04d}-{month:02d} ==="
                )

                print(
                    f"Budget: "
                    f"{format_money(status['budget'])}"
                )

                print(
                    f"Total spent: "
                    f"{format_money(status['spent'])}"
                )

                print(
                    f"Remaining: "
                    f"{format_money(status['remaining'])}"
                )

                print(
                    f"Budget utilisation: "
                    f"{status['utilisation']:.2f}%"
                )

                # Budget exceeded
                if status["status"] == "EXCEEDED":
                    print(
                        "\n🚨 BUDGET EXCEEDED!"
                    )

                    print(
                        f"You have exceeded your "
                        f"budget by "
                        f"{format_money(abs(status['remaining']))}."
                    )

                # 80% or more used
                elif status["status"] == "WARNING":
                    print(
                        "\n⚠️ WARNING!"
                    )

                    print(
                        "You have used 80% or more "
                        "of your monthly budget."
                    )

                # Budget is safe
                else:
                    print(
                        "\n✅ Budget is within "
                        "the safe spending limit."
                    )

            except ValueError:
                print(
                    "❌ Please enter valid numbers."
                )

        # ----------------------------------------
        # 6. BACK TO MAIN MENU
        # ----------------------------------------
        elif choice == "6":
            print(
                "\nReturning to main menu..."
            )
            break

        # ----------------------------------------
        # INVALID CHOICE
        # ----------------------------------------
        else:
            print(
                "\n❌ Invalid choice. "
                "Please enter a number between "
                "1 and 6."
            )

def budget_menu(expenses, budget_manager):
    """
    Display and manage the monthly budget submenu.
    """

    while True:
        print("\n" + "=" * 40)
        print("          BUDGET MANAGEMENT")
        print("=" * 40)
        print("1. Set Monthly Budget")
        print("2. View Budget Status")
        print("3. View All Budgets")
        print("4. Delete Budget")
        print("5. Back to Main Menu")
        print("=" * 40)

        choice = input("Enter your choice (1-5): ").strip()

        # ----------------------------------------
        # 1. SET MONTHLY BUDGET
        # ----------------------------------------
        if choice == "1":
            print("\n=== SET MONTHLY BUDGET ===")

            try:
                year = int(
                    input("Enter year (YYYY): ").strip()
                )

                month = int(
                    input("Enter month (1-12): ").strip()
                )

                if month < 1 or month > 12:
                    print(
                        "❌ Month must be between 1 and 12."
                    )
                    continue

                amount = validate_amount(
                    input(
                        "Enter monthly budget amount: "
                    ).strip()
                )

                # Check whether budget already exists
                existing_budget = (
                    budget_manager.get_budget(
                        month,
                        year
                    )
                )

                if existing_budget is not None:
                    print(
                        "\n❌ A budget already exists "
                        f"for {year}-{month:02d}."
                    )
                    print(
                        f"Current budget: "
                        f"{format_money(existing_budget.amount)}"
                    )
                    continue

                # Create new Budget object
                budget = Budget(
                    month=month,
                    year=year,
                    amount=amount
                )

                # Add to manager
                budget_manager.add_budget(
                    budget
                )

                print(
                    "\n✅ Monthly budget added "
                    "successfully!"
                )
                print(
                    f"   Period: "
                    f"{year}-{month:02d}"
                )
                print(
                    f"   Budget: "
                    f"{format_money(amount)}"
                )

            except ValueError as error:
                print(
                    f"\n❌ Invalid input: {error}"
                )

        # ----------------------------------------
        # 2. VIEW BUDGET STATUS
        # ----------------------------------------
        elif choice == "2":
            print("\n=== VIEW BUDGET STATUS ===")

            try:
                year = int(
                    input("Enter year (YYYY): ").strip()
                )

                month = int(
                    input("Enter month (1-12): ").strip()
                )

                if month < 1 or month > 12:
                    print(
                        "❌ Month must be between 1 and 12."
                    )
                    continue

                status = (
                    budget_manager
                    .calculate_budget_status(
                        expenses,
                        month,
                        year
                    )
                )

                if status is None:
                    print(
                        f"\n❌ No budget found for "
                        f"{year}-{month:02d}."
                    )
                    continue

                print(
                    f"\n=== BUDGET STATUS: "
                    f"{year}-{month:02d} ==="
                )

                print(
                    f"Budget: "
                    f"{format_money(status['budget'])}"
                )

                print(
                    f"Total spent: "
                    f"{format_money(status['spent'])}"
                )

                print(
                    f"Remaining: "
                    f"{format_money(status['remaining'])}"
                )

                print(
                    f"Budget utilisation: "
                    f"{status['utilisation']:.2f}%"
                )

                if status["status"] == "EXCEEDED":
                    print(
                        "\n🚨 BUDGET EXCEEDED!"
                    )
                    print(
                        f"You have exceeded your budget by "
                        f"{format_money(abs(status['remaining']))}."
                    )

                elif status["status"] == "WARNING":
                    print(
                        "\n⚠️ WARNING: "
                        "You have used 80% or more "
                        "of your budget."
                    )

                else:
                    print(
                        "\n✅ Budget is within the "
                        "safe spending limit."
                    )

            except ValueError as error:
                print(
                    f"\n❌ Invalid input: {error}"
                )

        # ----------------------------------------
        # 3. VIEW ALL BUDGETS
        # ----------------------------------------
        elif choice == "3":
            print("\n=== ALL BUDGETS ===")

            budgets = (
                budget_manager.get_all_budgets()
            )

            if not budgets:
                print(
                    "No budgets have been set."
                )
                continue

            for index, budget in enumerate(
                budgets,
                start=1
            ):
                print(
                    f"{index}. "
                    f"{budget.year}-"
                    f"{budget.month:02d} | "
                    f"Budget: "
                    f"{format_money(budget.amount)}"
                )

        # ----------------------------------------
        # 4. DELETE BUDGET
        # ----------------------------------------
        elif choice == "4":
            print("\n=== DELETE BUDGET ===")

            budgets = (
                budget_manager.get_all_budgets()
            )

            if not budgets:
                print(
                    "No budgets available to delete."
                )
                continue

            for index, budget in enumerate(
                budgets,
                start=1
            ):
                print(
                    f"{index}. "
                    f"{budget.year}-"
                    f"{budget.month:02d} | "
                    f"{format_money(budget.amount)}"
                )

            try:
                choice_number = int(
                    input(
                        "\nEnter budget number "
                        "to delete "
                        "(or 0 to cancel): "
                    ).strip()
                )

                if choice_number == 0:
                    print(
                        "Deletion cancelled."
                    )
                    continue

                if (
                    choice_number < 1
                    or choice_number > len(budgets)
                ):
                    print(
                        "❌ Invalid budget number."
                    )
                    continue

                selected_budget = budgets[
                    choice_number - 1
                ]

                print(
                    "\nYou selected:"
                )
                print(
                    f"  {selected_budget.year}-"
                    f"{selected_budget.month:02d} | "
                    f"{format_money(selected_budget.amount)}"
                )

                confirmation = input(
                    "\nAre you sure you want "
                    "to delete this budget? (y/n): "
                ).strip().lower()

                if confirmation == "y":
                    removed = (
                        budget_manager
                        .remove_budget(
                            selected_budget.month,
                            selected_budget.year
                        )
                    )

                    if removed:
                        print(
                            "\n✅ Budget deleted "
                            "successfully!"
                        )

                elif confirmation == "n":
                    print(
                        "\nDeletion cancelled."
                    )

                else:
                    print(
                        "\n❌ Please enter "
                        "'y' or 'n'."
                    )

            except ValueError:
                print(
                    "❌ Please enter a valid number."
                )

        # ----------------------------------------
        # 5. BACK TO MAIN MENU
        # ----------------------------------------
        elif choice == "5":
            print(
                "\nReturning to main menu..."
            )
            break

        else:
            print(
                "\n❌ Invalid choice. "
                "Please enter a number between 1 and 5."
            )


    while True:

        print("\n" + "=" * 40)
        print("        BACKUP & RESTORE")
        print("=" * 40)
        print("1. Create Backup")
        print("2. Restore Backup")
        print("3. Back to Main Menu")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-3): "
        ).strip()

        # ----------------------------------------
        # 1. CREATE BACKUP
        # ----------------------------------------
        if choice == "1":

            create_backup()

        # ----------------------------------------
        # 2. RESTORE BACKUP
        # ----------------------------------------
        elif choice == "2":

            confirmation = input(
                "\nRestoring will overwrite current data.\n"
                "Continue? (y/n): "
            ).strip().lower()

            if confirmation != "y":
                print(
                    "\nRestore cancelled."
                )
                continue

            try:

                # Restore files from backup folder
                restore_backup()

                # ----------------------------------------
                # RELOAD EXPENSES
                # ----------------------------------------

                restored_expenses = load_expenses(
                    DATA_FILE
                )

                # Replace contents of existing list
                # instead of creating a new list.
                expenses.clear()
                expenses.extend(
                    restored_expenses
                )

                # ----------------------------------------
                # RELOAD BUDGETS
                # ----------------------------------------

                budget_manager.load(
                    BUDGETS_FILE
                )

                print(
                    "\n✅ Application data reloaded successfully."
                )

                print(
                    f"Expenses currently loaded: "
                    f"{len(expenses)}"
                )

                print(
                    f"Budgets currently loaded: "
                    f"{len(budget_manager.get_all_budgets())}"
                )

            except (
                OSError,
                ValueError,
                TypeError,
            ) as error:

                print(
                    "\n❌ Failed to reload restored data:"
                )

                print(
                    f"   {error}"
                )

        # ----------------------------------------
        # 3. BACK TO MAIN MENU
        # ----------------------------------------
        elif choice == "3":

            print(
                "\nReturning to Main Menu..."
            )

            break

        # ----------------------------------------
        # INVALID CHOICE
        # ----------------------------------------
        else:

            print(
                "\n❌ Invalid choice."
            )
                                  
def charts_menu(expenses):
    """
    Display the charts submenu.
    """

    while True:

        print("\n" + "=" * 40)
        print("             CHARTS")
        print("=" * 40)
        print("1. Category-wise Pie Chart")
        print("2. Monthly Spending Bar Chart")
        print("3. Back")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-3): "
        ).strip()

        if choice == "1":

            generate_category_pie_chart(
                expenses
            )

        elif choice == "2":

            try:

                year = int(
                    input(
                        "Enter year (YYYY): "
                    ).strip()
                )

                generate_monthly_bar_chart(
                    expenses,
                    year,
                )

            except ValueError:

                print(
                    "❌ Please enter a valid year."
                )

        elif choice == "3":

            print(
                "\nReturning to Main Menu..."
            )

            break

        else:

            print(
                "\n❌ Invalid choice."
            )


def export_menu(expenses):
    """
    Display the export submenu.
    """

    while True:

        print("\n" + "=" * 40)
        print("          EXPORT DATA")
        print("=" * 40)
        print("1. Export to CSV")
        print("2. Export to JSON")
        print("3. Export Finance Report")
        print("4. Export Everything")
        print("5. Back")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-5): "
        ).strip()

        if choice == "1":

            export_to_csv(expenses)

        elif choice == "2":

            export_to_json(expenses)

        elif choice == "3":

            export_report(expenses)

        elif choice == "4":

            export_to_csv(expenses)
            export_to_json(expenses)
            export_report(expenses)

            print(
                "\n✅ All reports exported successfully!"
            )

        elif choice == "5":

            print(
                "\nReturning to Main Menu..."
            )

            break

        else:

            print(
                "\n❌ Invalid choice."
            )
def backup_menu(expenses, budget_manager):
    """
  ##  Display the backup and restore submenu.

    #Allows the user to create backups and restore previously
    #backed-up data. After restoration, expenses and budgets
   # are reloaded into memory so the running application
   # immediately reflects the restored data.
    
   """
    while True:

        print("\n" + "=" * 40)
        print("        BACKUP & RESTORE")
        print("=" * 40)
        print("1. Create Backup")
        print("2. Restore Backup")
        print("3. Back to Main Menu")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-3): "
        ).strip()

        # ----------------------------------------
        # 1. CREATE BACKUP
        # ----------------------------------------
        if choice == "1":

            create_backup()

        # ----------------------------------------
        # 2. RESTORE BACKUP
        # ----------------------------------------
        elif choice == "2":

            confirmation = input(
                "\nRestoring will overwrite current data.\n"
                "Continue? (y/n): "
            ).strip().lower()

            if confirmation != "y":
                print(
                    "\nRestore cancelled."
                )
                continue

            try:

                # Restore files from backup folder
                restore_backup()

                # ----------------------------------------
                # RELOAD EXPENSES
                # ----------------------------------------

                restored_expenses = load_expenses(
                    DATA_FILE
                )

                # Replace contents of existing list
                # instead of creating a new list.
                expenses.clear()
                expenses.extend(
                    restored_expenses
                )

                # ----------------------------------------
                # RELOAD BUDGETS
                # ----------------------------------------

                budget_manager.load(
                    BUDGETS_FILE
                )

                print(
                    "\n✅ Application data reloaded successfully."
                )

                print(
                    f"Expenses currently loaded: "
                    f"{len(expenses)}"
                )

                print(
                    f"Budgets currently loaded: "
                    f"{len(budget_manager.get_all_budgets())}"
                )

            except (
                OSError,
                ValueError,
                TypeError,
            ) as error:

                print(
                    "\n❌ Failed to reload restored data:"
                )

                print(
                    f"   {error}"
                )

        # ----------------------------------------
        # 3. BACK TO MAIN MENU
        # ----------------------------------------
        elif choice == "3":

            print(
                "\nReturning to Main Menu..."
            )

            break

        # ----------------------------------------
        # INVALID CHOICE
        # ----------------------------------------
        else:

            print(
                "\n❌ Invalid choice."
            )
                                  
def run_menu(expenses, budget_manager):

    """
    Run the main interactive menu until the user chooses Exit.
    """
    

    while True:

        print("\n" + "=" * 40)
        print("       PERSONAL FINANCE MANAGER")
        print("=" * 40)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Search Expenses")
        print("6. Reports & Analytics")
        print("7. Display Dashboard")
        print("8. Currency Settings")
        print("9. Budget Management")
        print("10. Charts")
        print("11. Export Data")
        print("12. Backup & Restore")
        print("13. Exit")
        print("=" * 40)

        choice = input(
            "Enter your choice (1-13): "
        ).strip()

        if choice == "1":

            add_expense(
                expenses,
                budget_manager,
            )

        elif choice == "2":

            view_expenses(expenses)

        elif choice == "3":

            edit_expense(expenses)

        elif choice == "4":

            delete_expense(expenses)

        elif choice == "5":

            search_expenses(expenses)

        elif choice == "6":

            reports_menu(
                expenses,
                budget_manager,
            )

        elif choice == "7":

             dashboard_menu(
        expenses,
        budget_manager,
             )
        elif choice =="8":
            choose_currency() 
        elif choice == "9":    

            budget_menu(
                expenses,
                budget_manager,
            )

        elif choice == "10":

            charts_menu(expenses)

        elif choice == "11":

            export_menu(expenses)

        elif choice == "12":

            backup_menu(
                expenses,
                budget_manager,
            )

        elif choice == "13":

            print(
                "\nThank you for using "
                "Personal Finance Manager!"
            )

            print("Goodbye! 👋")

            break

        else:

            print(
                "\n❌ Invalid choice. "
                "Please enter a number between 1 and 12."
            )