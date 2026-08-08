# Architecture

## 1. Overview

Personal Finance Manager is a modular, menu-driven command-line application written in Python. The application separates user interaction, domain models, persistence, reporting, visualization, configuration, export, and backup responsibilities into independent modules.

The application uses local file-based persistence:

- `data/expenses.csv` stores expense records.
- `data/budgets.json` stores monthly budgets.
- `data/settings.json` stores the selected currency.
- `backup/` stores backup copies of the application data.
- `reports/` stores generated exports, reports, and chart images.

## 2. High-Level Architecture

```text
User
  |
  v
main.py
  |
  v
src.menu.run_menu()
  |
  +--> Expense Management ----> Expense + Validation ----> expenses.csv
  |
  +--> Budget Management ------> BudgetManager -----------> budgets.json
  |
  +--> Reports & Analytics ----> reports.py
  |
  +--> Dashboard -------------> dashboard.py
  |
  +--> Charts -----------------> charts.py ---------------> reports/*.png
  |
  +--> Export -----------------> export.py ---------------> reports/*
  |
  +--> Backup & Restore -------> backup.py --------------> backup/
  |
  +--> Currency Settings ------> config.py --------------> settings.json
```

## 3. Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Application entry point; loads data, starts the menu, and saves data on exit |
| `menu.py` | Interactive command-line menus and user workflows |
| `expense.py` | `Expense` domain model and expense validation integration |
| `budget.py` | `Budget` domain model and budget field validation |
| `budget_manager.py` | Budget collection management and budget-status calculations |
| `file_manager.py` | CSV persistence for expenses |
| `budget_file_manager.py` | JSON persistence for budgets |
| `utils.py` | Validation for amounts, dates, categories, and descriptions |
| `reports.py` | Spending totals, averages, category summaries, monthly summaries, highest/lowest expense |
| `dashboard.py` | Consolidated financial dashboard |
| `charts.py` | Matplotlib category and monthly charts |
| `export.py` | CSV, JSON, and text report exports |
| `backup.py` | Backup creation and restoration |
| `config.py` | Currency configuration and settings persistence |

## 4. Core Data Models

### Expense

The `Expense` class contains:

- `amount`
- `category`
- `date`
- `description`

Amounts are represented as `Decimal` values rounded to two decimal places. Categories are normalized to the application's standard capitalization.

### Budget

The `Budget` class contains:

- `month`
- `year`
- `amount`

The model validates month, year, and amount values before accepting them.

### BudgetManager

`BudgetManager` maintains the collection of budgets and provides:

- add
- remove
- lookup
- list
- save/load
- budget-status calculation

## 5. Persistence

### Expenses

Expenses are serialized to CSV using Python's standard `csv` module. Loading reconstructs `Expense` objects, so validation is applied to persisted records as well.

### Budgets

Budgets are stored as JSON and loaded into `Budget` objects.

### Settings

Currency settings are stored as JSON. The application supports configured currencies including INR, USD, EUR, and GBP.

## 6. Reporting and Analytics

The reporting layer operates on the in-memory list of `Expense` objects.

Implemented calculations include:

- total spending
- average expense
- category-wise count, total, and average
- monthly spending
- highest expense
- lowest expense

Monthly reports match the validated `YYYY-MM-DD` expense date representation.

## 7. Budget Status

`BudgetManager.calculate_budget_status()` compares monthly spending against the selected monthly budget.

The resulting status can represent:

- normal/safe spending
- `WARNING` when 80% or more of the budget has been used
- `EXCEEDED` when spending is greater than the budget

The dashboard and reports menus expose this information to the user.

## 8. Visualization

`charts.py` uses Matplotlib to generate:

- category-wise pie charts
- monthly spending bar charts

Generated chart files are written to the `reports/` directory.

## 9. Export

The export module supports:

- CSV expense export
- JSON expense export
- text finance report export
- exporting all supported formats from one menu option

## 10. Backup and Restore

The backup module copies the main application data files into `backup/`.

Restore operations overwrite the current data after user confirmation and reload expenses and budgets into the running application.

## 11. Complexity

The application uses in-memory lists and file-based storage. Dominant operations are generally linear in the number of expense records:

| Operation | Complexity |
|---|---|
| Add expense to collection | O(1) |
| View expenses | O(n) |
| Search expenses | O(n) |
| Edit expense | O(n) |
| Delete expense | O(n) |
| Category summary | O(n) |
| Monthly summary | O(n) |
| Export | O(n) |

This architecture is appropriate for a personal finance application with small-to-medium local datasets. A database and indexed queries would be more appropriate for substantially larger datasets.

## 12. Design Rationale

The project deliberately uses simple local persistence instead of a database. This keeps the application portable, transparent, and easy to inspect for a coursework/portfolio setting.

The modular structure also allows individual components to be tested independently and makes future migration to database-backed storage or a GUI/API easier.
