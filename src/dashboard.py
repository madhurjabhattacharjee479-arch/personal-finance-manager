from datetime import datetime, timezone

from src.charts import (
    generate_category_pie_chart,
    generate_monthly_bar_chart,
)
from src.config import format_money
from src.reports import (
    calculate_total,
    category_summary,
    find_highest_expense,
    find_lowest_expense,
)


def dashboard_menu(expenses, budget_manager):
    """
    Display the finance dashboard menu.
    """

    while True:
        print("\n" + "=" * 50)
        print("         FINANCE DASHBOARD")
        print("=" * 50)
        print("1. View Dashboard")
        print("2. Generate Category Pie Chart")
        print("3. Generate Monthly Bar Chart")
        print("4. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            display_dashboard(
                expenses,
                budget_manager,
            )

        elif choice == "2":
            generate_category_pie_chart(expenses)

        elif choice == "3":
            try:
                year = int(input("Enter year (YYYY): ").strip())

                generate_monthly_bar_chart(
                    expenses,
                    year,
                )

            except ValueError:
                print("\n❌ Please enter a valid year.")

        elif choice == "4":
            print("\nReturning to Main Menu...")
            break

        else:
            print("\n❌ Invalid choice.")


def get_dashboard(expenses, budget_manager):
    """
    Generate dashboard statistics.
    """

    dashboard = {}

    dashboard["total_expenses"] = len(expenses)
    dashboard["total_spent"] = calculate_total(expenses)

    if expenses:
        dashboard["average_expense"] = (
            dashboard["total_spent"] / dashboard["total_expenses"]
        )
    else:
        dashboard["average_expense"] = 0

    dashboard["highest"] = find_highest_expense(expenses)
    dashboard["lowest"] = find_lowest_expense(expenses)

    summary = category_summary(expenses)

    dashboard["category_count"] = len(summary)

    if summary:
        top_category = max(
            summary.items(),
            key=lambda item: item[1]["total"],
        )

        dashboard["top_category"] = {
            "name": top_category[0],
            "amount": top_category[1]["total"],
        }

    else:
        dashboard["top_category"] = None

    dashboard["budgets"] = len(budget_manager.get_all_budgets())

    return dashboard


def display_dashboard(expenses, budget_manager):
    """
    Display dashboard statistics.
    """

    dashboard = get_dashboard(
        expenses,
        budget_manager,
    )

    print("\n" + "=" * 50)
    print("             FINANCE DASHBOARD")
    print("=" * 50)

    print(f"Total Expenses : {dashboard['total_expenses']}")
    print(f"Total Spent    : {format_money(dashboard['total_spent'])}")
    print(f"Average Expense: {format_money(dashboard['average_expense'])}")
    print(f"Categories     : {dashboard['category_count']}")
    print(f"Budgets Set    : {dashboard['budgets']}")

    print("-" * 50)

    if dashboard["highest"]:
        print("Highest Expense")
        print(f"   {dashboard['highest']}")

        print()

        print("Lowest Expense")
        print(f"   {dashboard['lowest']}")

    else:
        print("No expenses available.")

    print("-" * 50)

    if dashboard["top_category"]:
        print("Top Spending Category")
        print(f"   {dashboard['top_category']['name']}")
        print(f"   Amount : {format_money(dashboard['top_category']['amount'])}")

    else:
        print("No category data.")

    print("-" * 50)

    today = datetime.now(timezone.utc).date()

    status = budget_manager.calculate_budget_status(
        expenses,
        today.month,
        today.year,
    )

    if status:
        print("CURRENT MONTH BUDGET")
        print(f"Budget      : {format_money(status['budget'])}")
        print(f"Spent       : {format_money(status['spent'])}")
        print(f"Remaining   : {format_money(status['remaining'])}")
        print(f"Utilisation : {status['utilisation']:.2f}%")

        if status["status"] == "OK":
            print("Status      : ✅ Within Budget")

        elif status["status"] == "WARNING":
            print("Status      : ⚠ Near Budget Limit")

        elif status["status"] == "EXCEEDED":
            print("Status      : 🚨 Budget Exceeded")

        else:
            print(f"Status      : {status['status']}")

    else:
        print("No budget set for the current month.")

    print("=" * 50)
