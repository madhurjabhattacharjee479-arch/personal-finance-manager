import csv
import json
from pathlib import Path

from src.reports import (
    calculate_total,
    calculate_average,
    category_summary,
)

EXPORT_FOLDER = Path("reports")

CSV_FILE = EXPORT_FOLDER / "expenses_export.csv"
JSON_FILE = EXPORT_FOLDER / "expenses_export.json"
TEXT_FILE = EXPORT_FOLDER / "finance_report.txt"


def export_to_csv(expenses):
    """
    Export all expenses to a CSV file.
    """

    EXPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Date",
                "Category",
                "Amount",
                "Description",
            ]
        )

        for expense in expenses:

            writer.writerow(
                [
                    expense.date,
                    expense.category,
                    expense.amount,
                    expense.description,
                ]
            )

    print(f"\n✅ CSV exported to:\n{CSV_FILE}")


def export_to_json(expenses):
    """
    Export expenses to JSON.
    """

    EXPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = []

    for expense in expenses:

        data.append(
            {
                "date": expense.date,
                "category": expense.category,
                "amount": str(expense.amount),
                "description": expense.description,
            }
        )

    with JSON_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
        )

    print(f"\n✅ JSON exported to:\n{JSON_FILE}")


def export_report(expenses):
    """
    Export a complete finance report.
    """

    EXPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = calculate_total(expenses)
    average = calculate_average(expenses)
    summary = category_summary(expenses)

    with TEXT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("PERSONAL FINANCE REPORT\n")

        file.write("=" * 35 + "\n\n")

        file.write(f"Total Spending : {total}\n")

        file.write(f"Average Expense : {average}\n\n")

        file.write("CATEGORY SUMMARY\n")

        file.write("-" * 35 + "\n")

        for category, data in summary.items():

            file.write(f"\n{category}\n")

            file.write(f"Count : {data['count']}\n")

            file.write(f"Total : {data['total']}\n")

            file.write(f"Average : {data['average']}\n")

    print(f"\n✅ Finance report exported to:\n{TEXT_FILE}")
