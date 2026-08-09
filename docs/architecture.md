# Architecture

## 1. Overview

Personal Finance Manager is a modular, menu-driven command-line application written in Python.

The application separates user interaction, expense and budget management, persistence, reporting, visualization, configuration, export, and backup responsibilities into independent modules.

The application uses local file-based persistence:

- `data/expenses.csv` stores expense records.
- `data/budgets.json` stores monthly budgets.
- `data/settings.json` stores application settings such as currency.
- `backup/` stores backup copies of application data.
- `reports/` stores generated reports, exports, and chart images.

The main application flow begins at `main.py`, which starts the menu system implemented in `menu.py`.

---

## 2. High-Level Architecture

The application follows a modular architecture in which the user interacts with the command-line menu and the menu delegates operations to specialized modules.

The high-level flow is:

```text
User
  |
  v
main.py
  |
  v
menu.py
  |
  +--> Expense Management ----> utils.py --------> file_manager.py
  |                                                    |
  |                                                    v
  |                                             expenses.csv
  |
  +--> Budget Management ------> budget_manager.py
  |                                  |
  |                                  v
  |                           budget_file_manager.py
  |                                  |
  |                                  v
  |                              budgets.json
  |
  +--> Reports & Analytics ----> reports.py
  |
  +--> Dashboard -------------> dashboard.py
  |                                  |
  |                                  v
  |                              reports.py
  |
  +--> Charts -----------------> charts.py
  |                                  |
  |                                  v
  |                              reports.py
  |                                  |
  |                                  v
  |                            reports/*.png
  |
  +--> Export -----------------> export.py
  |                                  |
  |                                  v
  |                              reports/*
  |
  +--> Backup & Restore -------> backup.py
  |                                  |
  |                                  v
  |                               backup/
  |
  +--> Currency Settings ------> config.py
                                     |
                                     v
                                settings.json 
```
---
## 3. Architectural Layers

The project can be viewed as several logical layers.

### 3.1 Presentation Layer

The presentation layer handles interaction with the user.

Main components:

main.py
menu.py
dashboard.py

Responsibilities include:

Starting the application.
Displaying menus.
Receiving user input.
Calling appropriate application functionality.
Displaying results and errors.

### 3.2 Domain Layer

The domain layer contains the application's core financial objects and business logic.

Main components:

expense.py
budget.py
budget_manager.py

Responsibilities include:

Representing expenses.
Representing budgets.
Validating domain data.
Managing collections of budgets.
Calculating budget status.

### 3.3 Validation Layer

The validation logic is centralized in:

utils.py

It validates:

expense amounts
dates
categories
descriptions

Validation is applied both when users enter data and when persisted records are loaded.

### 3.4 Persistence Layer

The application uses local files instead of a database.

Main components:

file_manager.py
budget_file_manager.py
config.py

Storage formats:

Data	File	Format
Expenses	data/expenses.csv	CSV
Budgets	data/budgets.json	JSON
Settings	data/settings.json	JSON

This approach keeps the application simple, portable, and easy to inspect.

### 3.5 Reporting and Visualization Layer

Reporting and visualization are handled by:

reports.py
dashboard.py
charts.py

reports.py performs calculations on expense data.

dashboard.py combines important financial information into a consolidated view.

charts.py uses Matplotlib to generate visual representations of financial data.

### 3.6 Export Layer

export.py provides functionality for exporting financial information.

Supported formats include:

CSV
JSON
text reports

Generated files are stored under the reports/ directory.

### 3.7 Backup Layer

backup.py manages backup and restoration of application data.

Backup files are stored under:

backup/

The restore functionality can replace current application data with previously backed-up data after user confirmation.

## 4. Module Responsibilities

Module	Responsibility

main.py               	Application entry point and application startup/shutdown flow
menu.py	                Interactive command-line menus and user workflows
expense.py      	      Expense domain model
budget.py	              Budget domain model and budget validation
budget_manager.py	      Budget collection management and budget-status calculations
file_manager.py	        CSV persistence for expenses
budget_file_manager.py	JSON persistence for budgets
utils.py              	Validation of amounts, dates, categories, and descriptions
reports.py	            Financial calculations and summaries
dashboard.py           	Consolidated financial dashboard
charts.py	              Generation of financial charts using Matplotlib
export.py              	Export of financial data and reports
backup.py             	Backup and restoration of application data
config.py             	Currency and application settings management

## 5. Core Data Models
### 5.1 Expense

The Expense class represents an individual financial expense.

It contains:

amount
category
date
description

The amount is represented using Python's Decimal type and is rounded to two decimal places.

Categories are normalized to the application's standard capitalization.

Example categories include:

Food
Transport
Entertainment
Shopping
Other

### 5.2 Budget

The Budget class represents a monthly spending budget.

It contains:

month
year
amount

The class validates the month, year, and amount before accepting the values.

### 5.3 BudgetManager

BudgetManager maintains a collection of budgets.

Its responsibilities include:

Adding budgets.
Removing budgets.
Looking up budgets.
Listing budgets.
Saving budgets.
Loading budgets.
Calculating budget status.

Budget status is determined by comparing the selected monthly budget with actual spending.

## 6. Validation

Validation is centralized in utils.py.

The following validation functions are provided:

validate_amount()

Validates expense amounts and converts valid values into Decimal values rounded to two decimal places.

Invalid values such as:

non-numeric input
zero
negative values

are rejected.

validate_date()

Validates dates using the YYYY-MM-DD representation.

Invalid formats and invalid calendar dates are rejected.

validate_category()

Validates expense categories against the application's allowed category list.

Category matching is case-insensitive and valid categories are normalized to standard capitalization.

validate_description()

Ensures that descriptions are non-empty after removing surrounding whitespace.

## 7. Persistence
## 7.1 Expense Persistence

Expenses are stored in:

data/expenses.csv

The application uses Python's standard csv module for persistence.

When expenses are loaded from the CSV file, they are reconstructed as Expense objects. This means validation is also applied to persisted records.

## 7.2 Budget Persistence

Budgets are stored in:

data/budgets.json

The budget file manager handles serialization and deserialization of budget information.

Loaded records are reconstructed as Budget objects.

### 7.3 Settings Persistence

Application settings are stored in:

data/settings.json

The settings system supports configured currencies including:

INR
USD
EUR
GBP

## 8. Reporting and Analytics

The reporting layer operates on the application's in-memory expense collection.

Implemented calculations include:

Total spending.
Average expense.
Category-wise expense count.
Category-wise spending total.
Category-wise average.
Monthly spending.
Highest expense.
Lowest expense.

Monthly calculations use the validated YYYY-MM-DD expense date representation.

## 9. Budget Status

BudgetManager.calculate_budget_status() compares monthly spending with the configured monthly budget.

The resulting status can represent:

Safe or normal spending.
WARNING when 80% or more of the budget has been used.
EXCEEDED when spending is greater than the budget.

Budget status information is exposed through the dashboard and reporting functionality.

## 10. Dashboard

dashboard.py provides a consolidated financial overview.

The dashboard uses information produced by the reporting layer and presents important financial metrics to the user.

This allows the user to view financial information without manually calculating totals or summaries.

## 11. Visualization

charts.py uses Matplotlib to generate financial visualizations.

The application supports charts such as:

Category-wise spending pie charts.
Monthly spending bar charts.

Generated chart files are stored in:

reports/

The charting module uses the reporting functionality to obtain the required financial summaries.

## 12. Export

export.py provides data and report export functionality.

Supported export formats include:

CSV

Used for structured tabular expense data.

JSON

Used for structured machine-readable expense data.

Text

Used for human-readable financial reports.

Exported files are stored in the reports/ directory.

## 13. Backup and Restore

The backup system is implemented in backup.py.

Application data can be copied into:

backup/

The restore process can restore backed-up application data to the active data directory.

Restoration overwrites the current data after user confirmation.

After restoration, the application reloads the relevant expense and budget data.

## 14. Error Handling

The application includes input validation and error handling for user-provided data.

Examples include:

Invalid expense amounts.
Negative or zero amounts.
Invalid dates.
Invalid categories.
Empty descriptions.
Invalid budget values.
Invalid menu selections.
File-related errors.

Validation errors are handled before invalid data is accepted into the application's core data structures.

## 15. Complexity

The application primarily uses in-memory lists and local file-based storage.

The dominant operations are generally linear in the number of expense records.

Operation	Complexity
Add expense to collection	O(1)
View expenses	O(n)
Search expenses	O(n)
Edit expense	O(n)
Delete expense	O(n)
Category summary	O(n)
Monthly summary	O(n)
Export	O(n)

Here, n represents the number of expense records.

The architecture is appropriate for a personal finance application with small-to-medium local datasets.

For substantially larger datasets, database-backed storage and indexed queries would be more appropriate.

## 16. Design Rationale

The project deliberately uses simple local file-based persistence instead of a database.

This provides several advantages for the project's intended use:

Simple setup.
No external database server.
Portable application data.
Transparent data storage.
Easy inspection and debugging.
Suitable for a coursework and portfolio project.

The modular architecture separates responsibilities between components.

For example:

Validation is centralized in utils.py.
Expense persistence is handled by file_manager.py.
Budget persistence is handled by budget_file_manager.py.
Financial calculations are handled by reports.py.
Visualization is handled by charts.py.
Backup functionality is isolated in backup.py.

This separation makes individual modules easier to test and maintain.

It also provides a foundation for future migration to database-backed storage, a graphical user interface, or an API without requiring the entire application to be rewritten.

## 17. Architecture Diagram

The visual architecture diagram for this documentation is maintained separately as a Mermaid file:

docs/
└── diagrams/
    └── architecture.mmd

The .mmd file contains the Mermaid source used to render the architecture diagram.

The Markdown document describes the architecture, while the .mmd file provides its graphical representation.

## 18. Related Documentation

Additional project documentation is available in:

docs/user-guide.md — instructions for using the application.
docs/developer-guide.md — development and contribution information.
docs/testing.md — testing strategy and test execution.
docs/diagrams/architecture.mmd — high-level architecture diagram.
docs/diagrams/class-diagram.mmd — class relationships.
docs/diagrams/dfd.mmd — data flow diagram.
docs/diagrams/sequence-diagram.mmd — application interaction sequence.