# Developer Guide

## 1. Prerequisites

Recommended environment:

- Python 3.13
- Git
- A terminal such as PowerShell, Command Prompt, or Bash

## 2. Clone the Repository

```bash
git clone https://github.com/madhurjabhattacharjee479-arch/personal-finance-manager.git
cd personal-finance-manager
```

## 3. Install Runtime Dependencies

```bash
pip install -r requirements.txt
```

The runtime requirements currently contain:

```text
matplotlib==3.11.1
```

## 4. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

This includes the runtime requirements plus:

- pytest
- ruff
- black

## 5. Run the Application

```bash
python main.py
```

## 6. Run Tests

```bash
pytest
```

The current project test suite collects 75 tests.

## 7. Code Quality Checks

Run Ruff:

```bash
ruff check .
```

Run Black in check mode:

```bash
black --check .
```

Both should pass before submitting a change.

## 8. Source Layout

```text
src/
├── backup.py
├── budget.py
├── budget_file_manager.py
├── budget_manager.py
├── charts.py
├── config.py
├── dashboard.py
├── expense.py
├── export.py
├── file_manager.py
├── menu.py
├── reports.py
└── utils.py
```

## 9. Testing Layout

```text
tests/
├── test_budget.py
├── test_budget_file_manager.py
├── test_budget_integration.py
├── test_budget_manager.py
├── test_config.py
├── test_expense.py
├── test_expense_validation.py
├── test_file_manager.py
├── test_reports.py
└── test_utils.py
```

## 10. Development Workflow

1. Create a feature branch.
2. Make a focused change.
3. Add or update tests.
4. Run `pytest`.
5. Run `ruff check .`.
6. Run `black --check .`.
7. Review the Git diff.
8. Commit with a descriptive message.
9. Push the branch and open a pull request.

## 11. Important Design Rules

### Validation

Keep validation centralized in `utils.py` rather than duplicating validation logic across menus and persistence code.

### Monetary Values

Use `Decimal` for expense and budget amounts to avoid inappropriate floating-point arithmetic for financial values.

### Persistence

Use the existing CSV/JSON persistence modules instead of writing ad-hoc file operations inside the menu layer.

### User Interface

`menu.py` is responsible for interaction and should delegate calculations and persistence to the relevant modules.

### Reports

Keep reporting calculations in `reports.py` so they can be reused by the dashboard, charts, and export functionality.

## 12. Adding a New Feature

A typical feature should follow this pattern:

```text
User interaction
      |
      v
menu.py
      |
      +--> domain/model logic
      |
      +--> persistence/reporting module
      |
      v
tests/
```

Avoid putting business logic directly into menu prompts when it can be represented as a reusable function or class method.

## 13. Data Files

The project uses:

```text
data/expenses.csv
data/budgets.json
data/settings.json
```

Generated outputs are placed in:

```text
reports/
```

Backups are stored in:

```text
backup/
```

## 14. Pull Requests

Before opening a pull request, verify:

```bash
pytest
ruff check .
black --check .
```

The change should include relevant tests and documentation updates where behaviour or usage changes.
