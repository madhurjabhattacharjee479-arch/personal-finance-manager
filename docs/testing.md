# Testing Documentation

## 1. Testing Strategy

The project uses **Pytest** for automated testing.

The test suite focuses on:

- domain-model validation
- file persistence
- budget calculations
- configuration management
- reporting calculations
- utility validation
- integration between budget management and persistence

## 2. Current Test Result

The project currently collects:

```text
75 tests
```

The current project snapshot was executed successfully with:

```text
75 passed in 0.16s
```

## 3. Test Distribution

| Test Module | Coverage Area | Collected Tests |
|---|---|---:|
| `test_budget.py` | Budget model validation | 6 |
| `test_budget_file_manager.py` | Budget JSON persistence | 2 |
| `test_budget_integration.py` | Budget persistence integration | 2 |
| `test_budget_manager.py` | Budget warning/exceeded status | 2 |
| `test_config.py` | Currency and settings | 12 |
| `test_expense.py` | Expense model and validation | 13 |
| `test_file_manager.py` | Expense CSV persistence | 10 |
| `test_reports.py` | Reports and analytics | 13 |
| `test_utils.py` | Utility validation | 15 |
| **Total** | | **75** |

> `test_expense_validation.py` is a standalone validation demonstration script rather than a Pytest test collection.

## 4. Expense Validation Tests

The expense tests verify:

- valid expense creation
- `Decimal` amount representation
- category normalization
- invalid text amounts
- zero amounts
- negative amounts
- invalid date format
- invalid calendar dates
- invalid categories
- empty categories
- empty descriptions
- whitespace-only descriptions
- string representation

## 5. File Persistence Tests

CSV persistence tests verify:

- CSV creation
- save/load round trips
- `Decimal` reconstruction
- missing files
- empty files
- header-only files
- missing required columns
- invalid amounts
- invalid categories
- multiple expense records

## 6. Budget Tests

Budget tests verify:

- valid budget creation
- invalid month/year/amount handling
- JSON save/load
- persistence through `BudgetManager`
- budget removal after loading
- warning status
- exceeded status

## 7. Configuration Tests

Configuration tests verify:

- money formatting for INR, USD, EUR, and GBP
- settings persistence
- valid settings loading
- missing settings files
- invalid currencies
- corrupted JSON
- configured currency validity
- interactive currency selection behaviour

## 8. Reporting Tests

Reporting tests cover:

- total spending
- empty totals
- average spending
- empty averages
- category summaries
- empty category summaries
- monthly summaries
- months with no matches
- highest expense
- lowest expense
- empty expense collections

## 9. Utility Tests

Utility tests cover:

- amount validation
- date validation
- category validation
- category normalization
- description validation
- empty/whitespace input rejection

## 10. Running the Tests

From the project root:

```bash
pytest
```

For a concise result:

```bash
pytest -q
```

## 11. Code Quality Verification

The project also uses:

```bash
ruff check .
black --check .
```

These checks are separate from the Pytest test suite and help maintain consistent, clean Python code.

## 12. Regression Testing

Whenever a feature is changed:

1. Run the relevant tests during development.
2. Run the full `pytest` suite.
3. Run Ruff.
4. Run Black in check mode.
5. Review the Git diff before committing.

This reduces the risk of introducing regressions into existing functionality.
