import shutil
import csv
from pathlib import Path

DATA_FOLDER = Path("data")
BACKUP_FOLDER = Path("backup")


def create_backup():
    """
    Create a backup of all application data files.

    The backup includes:
    - expenses.csv
    - budgets.json
    - settings.json

    Also reports the number of expense records
    stored in the backed-up expenses.csv file.
    """

    BACKUP_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = [
        "expenses.csv",
        "budgets.json",
        "settings.json",
    ]

    copied = 0
    expense_count = 0

    for filename in files:

        source = DATA_FOLDER / filename
        destination = BACKUP_FOLDER / filename

        if source.exists():

            shutil.copy2(
                source,
                destination,
            )

            copied += 1

            # Count expense records
            if filename == "expenses.csv":

                try:
                    with open(
                        source,
                        "r",
                        newline="",
                        encoding="utf-8",
                    ) as file:

                        reader = csv.reader(file)

                        # Skip CSV header
                        next(reader, None)

                        expense_count = sum(1 for row in reader if row)

                except (
                    OSError,
                    csv.Error,
                ) as error:

                    print(f"\n⚠️ Unable to count " f"expenses: {error}")

    if copied == 0:

        print("\n❌ No data files found to back up.")

    else:

        print("\n✅ Backup completed successfully.")

        print(f"Files backed up: {copied}")

        print(f"Expenses backed up: " f"{expense_count}")

        print(f"Location: {BACKUP_FOLDER}")


def restore_backup():
    """
    Restore backed-up data.

    Restores:
    - expenses.csv
    - budgets.json
    - settings.json

    Also reports the number of expense records
    restored from the backup.
    """

    if not BACKUP_FOLDER.exists():

        print("\n❌ No backup folder found.")

        return

    DATA_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = [
        "expenses.csv",
        "budgets.json",
        "settings.json",
    ]

    restored = 0
    expense_count = 0

    for filename in files:

        source = BACKUP_FOLDER / filename
        destination = DATA_FOLDER / filename

        if source.exists():

            shutil.copy2(
                source,
                destination,
            )

            restored += 1

            # Count restored expenses
            if filename == "expenses.csv":

                try:
                    with open(
                        source,
                        "r",
                        newline="",
                        encoding="utf-8",
                    ) as file:

                        reader = csv.reader(file)

                        # Skip CSV header
                        next(reader, None)

                        expense_count = sum(1 for row in reader if row)

                except (
                    OSError,
                    csv.Error,
                ) as error:

                    print(f"\n⚠️ Unable to count " f"restored expenses: {error}")

    if restored == 0:

        print("\n❌ No backup files available.")

    else:

        print("\n✅ Backup restored successfully.")

        print(f"Files restored: {restored}")

        print(f"Expenses restored: " f"{expense_count}")
