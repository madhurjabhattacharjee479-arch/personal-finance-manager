import json
from pathlib import Path

# File used to store user settings
SETTINGS_FILE = Path("data/settings.json")


# Available currencies
CURRENCIES = {
    "1": ("INR", "₹"),
    "2": ("USD", "$"),
    "3": ("EUR", "€"),
    "4": ("GBP", "£"),
}


# Default currency
CURRENT_CURRENCY = {
    "code": "INR",
    "symbol": "₹",
}


def format_money(amount):
    """
    Format a monetary amount using the currently selected currency.
    """
    return f"{CURRENT_CURRENCY['symbol']}{amount:.2f}"


def save_settings():
    """
    Save the current currency settings to the settings file.
    """
    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

        with SETTINGS_FILE.open("w", encoding="utf-8") as file:
            json.dump(CURRENT_CURRENCY, file, indent=4)

    except OSError as error:
        print(f"❌ Unable to save settings: {error}")


def load_settings():
    """
    Load saved currency settings from the settings file.

    If the file does not exist or contains invalid data,
    the default currency (INR) is used.
    """
    if not SETTINGS_FILE.exists():
        return

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            saved_settings = json.load(file)

        code = saved_settings.get("code")
        symbol = saved_settings.get("symbol")

        # Validate saved currency before applying it
        valid_currency = any(
            currency_code == code and currency_symbol == symbol
            for currency_code, currency_symbol in CURRENCIES.values()
        )

        if valid_currency:
            CURRENT_CURRENCY["code"] = code
            CURRENT_CURRENCY["symbol"] = symbol

    except (OSError, json.JSONDecodeError):
        print("⚠️ Unable to load saved settings. " "Using default currency: INR (₹).")


def choose_currency():
    """
    Display available currencies and allow the user
    to select a currency.
    """
    while True:
        print("\n=== CURRENCY SETTINGS ===")

        print(
            f"Current currency: "
            f"{CURRENT_CURRENCY['code']} "
            f"({CURRENT_CURRENCY['symbol']})"
        )

        print("\nAvailable currencies:")
        print("1. INR (₹)")
        print("2. USD ($)")
        print("3. EUR (€)")
        print("4. GBP (£)")
        print("5. Back to Main Menu")

        choice = input("\nSelect currency (1-5): ").strip()

        if choice in CURRENCIES:
            code, symbol = CURRENCIES[choice]

            CURRENT_CURRENCY["code"] = code
            CURRENT_CURRENCY["symbol"] = symbol

            # Save the new currency immediately
            save_settings()

            print(f"\n✅ Currency changed to " f"{code} ({symbol})")

            print("✅ Currency preference saved.")

            return

        elif choice == "5":
            return

        else:
            print("\n❌ Invalid choice. " "Please select 1-5.")
