from pathlib import Path
import os
import sys
import subprocess
import matplotlib.pyplot as plt

from src.reports import (
    category_summary,
    monthly_summary,
)

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


def open_chart(file_path):
    """
    Open a generated chart using the default image viewer.
    """

    try:

        file_path = str(file_path)

        if sys.platform.startswith("win"):

            os.startfile(file_path)

        elif sys.platform == "darwin":

            subprocess.call(["open", file_path])

        else:

            subprocess.call(["xdg-open", file_path])

    except Exception:

        print("\nℹ️ Chart generated successfully.")

        print("Open it manually from:")

        print(file_path)


def generate_category_pie_chart(expenses):
    """
    Generate and save a pie chart showing spending by category.
    """

    summary = category_summary(expenses)

    if not summary:
        print("❌ No expense data available.")
        return

    labels = []
    amounts = []

    for category, data in summary.items():
        labels.append(category)
        amounts.append(float(data["total"]))

    plt.figure(figsize=(7, 7))

    plt.pie(
        amounts,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.axis("equal")
    plt.title("Category-wise Spending")

    output_file = REPORTS_DIR / "category_pie_chart.png"

    plt.tight_layout()
    plt.savefig(output_file)

    plt.close()
    open_chart(output_file)
    print(f"\n✅ Pie chart saved to:\n{output_file}")


def generate_monthly_bar_chart(expenses, year):
    """
    Generate and save a monthly spending bar chart.
    """

    month_numbers = list(range(1, 13))

    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    totals = []

    for month in month_numbers:

        report = monthly_summary(
            expenses,
            year,
            month,
        )

        totals.append(float(report["total"]))

    plt.figure(figsize=(10, 5))

    plt.bar(month_numbers, totals)

    plt.title(f"Monthly Spending ({year})")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")

    plt.xticks(
        month_numbers,
        month_names,
    )

    plt.tight_layout()

    output_file = REPORTS_DIR / "monthly_bar_chart.png"

    plt.savefig(output_file)

    plt.close()
    open_chart(output_file)
    print(f"\n✅ Monthly chart saved to:\n{output_file}")
