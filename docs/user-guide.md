# User Guide

## 1. Starting the Application

From the project root:

```bash
python main.py
```

The application loads saved expenses, budgets, and currency settings before displaying the main menu.

## 2. Main Menu

The application provides these options:

1. Add New Expense
2. View All Expenses
3. Edit Expense
4. Delete Expense
5. Search Expenses
6. Reports & Analytics
7. Display Dashboard
8. Currency Settings
9. Budget Management
10. Charts
11. Export Data
12. Backup & Restore
13. Exit

Enter the corresponding menu number.

## 3. Adding an Expense

Select **1. Add New Expense** and provide:

- Amount
- Category
- Date
- Description

Supported categories are:

- Food
- Transport
- Entertainment
- Shopping
- Other

Dates must use:

```text
YYYY-MM-DD
```

The application rejects invalid, zero, or negative amounts, invalid dates, unsupported categories, and empty descriptions.

## 4. Viewing Expenses

Select **2. View All Expenses** to display the stored expense records.

## 5. Editing an Expense

Select **3. Edit Expense**, choose an expense by its displayed number, and enter the new validated values.

## 6. Deleting an Expense

Select **4. Delete Expense**.

The application asks for the expense number and requires confirmation before deleting the selected record.

## 7. Searching Expenses

Select **5. Search Expenses** and follow the prompts to search stored records using the available search criteria.

## 8. Reports & Analytics

Select **6. Reports & Analytics**.

Available reports include:

- Total and average spending
- Category-wise summary
- Monthly report
- Highest and lowest expense
- Budget status

The monthly report requires a year and month.

## 9. Dashboard

Select **7. Display Dashboard** to view consolidated spending information.

The dashboard uses the reporting layer to display information such as total spending, average expense, category statistics, budget information, and highest/lowest expenses.

## 10. Currency Settings

Select **8. Currency Settings**.

The configuration module supports the currencies configured by the application, including:

- INR
- USD
- EUR
- GBP

The selected currency is saved in `data/settings.json`.

## 11. Budget Management

Select **9. Budget Management**.

Available operations:

- Set monthly budget
- View budget status
- View all budgets
- Delete budget

Budget status reports:

- budget amount
- total spent
- remaining amount
- utilization percentage

A warning is shown at 80% or higher utilization, while spending beyond the budget is reported as `EXCEEDED`.

## 12. Charts

Select **10. Charts**.

The application can generate:

- Category-wise pie chart
- Monthly spending bar chart

Generated charts are stored under `reports/`.

## 13. Exporting Data

Select **11. Export Data**.

Available exports:

- CSV
- JSON
- Finance report
- Everything

Generated exports are stored under `reports/`.

## 14. Backup and Restore

Select **12. Backup & Restore**.

### Create Backup

The application copies the relevant local data files to the `backup/` directory.

### Restore Backup

Restore requires confirmation because current data will be overwritten.

After restoration, the application reloads expenses and budgets so the running session reflects the restored data.

## 15. Exiting

Select **13. Exit**.

Before exiting, `main.py` saves the current expenses and budgets back to the configured data files.

# Troubleshooting

## `ModuleNotFoundError`

Install the project dependencies:

```bash
pip install -r requirements.txt
```

For development and testing tools:

```bash
pip install -r requirements-dev.txt
```

## Application Does Not Start

Make sure the command is executed from the project root:

```bash
python main.py
```

Also verify that Python 3.13 or a compatible Python 3 version is installed.

## Invalid Amount

Amounts must be numeric and greater than zero.

Examples:

```text
45.50
100
```

Invalid examples include:

```text
abc
0
-25
```

## Invalid Date

Dates must use `YYYY-MM-DD` and must be real calendar dates.

Valid:

```text
2026-07-26
```

Invalid:

```text
26-07-2026
2026-02-30
```

## Invalid Category

Use one of:

```text
Food
Transport
Entertainment
Shopping
Other
```

Category matching is case-insensitive.

## Empty Description

Descriptions cannot be empty or contain only whitespace.

## CSV/Data File Problems

If a data file is missing, the application can initialize an empty collection in the relevant loading path. If a file contains invalid records or missing required columns, the application reports the loading error.

Do not manually alter the CSV structure unless you understand the required fields.

## Restore Accidentally Overwrites Data

Restore is intentionally destructive to the current data files. Always confirm that the backup contains the desired state before restoring.

## Tests Fail

Run:

```bash
pytest
```

The repository's current test suite collects 75 tests.

For development checks:

```bash
ruff check .
black --check .
```

Fix any reported issues before committing changes.
