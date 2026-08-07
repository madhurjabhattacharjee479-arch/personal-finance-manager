import json
from decimal import Decimal

from src import config

# ========================================
# FORMAT MONEY TESTS
# ========================================


def test_format_money_inr():
    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    result = config.format_money(Decimal("45.50"))

    assert result == "₹45.50"


def test_format_money_usd():
    config.CURRENT_CURRENCY["code"] = "USD"
    config.CURRENT_CURRENCY["symbol"] = "$"

    result = config.format_money(Decimal("100.00"))

    assert result == "$100.00"


def test_format_money_eur():
    config.CURRENT_CURRENCY["code"] = "EUR"
    config.CURRENT_CURRENCY["symbol"] = "€"

    result = config.format_money(Decimal("250.75"))

    assert result == "€250.75"


def test_format_money_gbp():
    config.CURRENT_CURRENCY["code"] = "GBP"
    config.CURRENT_CURRENCY["symbol"] = "£"

    result = config.format_money(Decimal("999.99"))

    assert result == "£999.99"


# ========================================
# SAVE SETTINGS TESTS
# ========================================


def test_save_settings(tmp_path, monkeypatch):
    settings_file = tmp_path / "settings.json"

    monkeypatch.setattr(
        config,
        "SETTINGS_FILE",
        settings_file,
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.save_settings()

    assert settings_file.exists()

    saved_data = json.loads(settings_file.read_text(encoding="utf-8"))

    assert saved_data == {
        "code": "INR",
        "symbol": "₹",
    }


# ========================================
# LOAD SETTINGS TESTS
# ========================================


def test_load_settings_valid_currency(
    tmp_path,
    monkeypatch,
):
    settings_file = tmp_path / "settings.json"

    settings_file.write_text(
        json.dumps(
            {
                "code": "USD",
                "symbol": "$",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config,
        "SETTINGS_FILE",
        settings_file,
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.load_settings()

    assert config.CURRENT_CURRENCY["code"] == "USD"
    assert config.CURRENT_CURRENCY["symbol"] == "$"


def test_load_settings_missing_file(
    tmp_path,
    monkeypatch,
):
    settings_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        config,
        "SETTINGS_FILE",
        settings_file,
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.load_settings()

    assert config.CURRENT_CURRENCY["code"] == "INR"
    assert config.CURRENT_CURRENCY["symbol"] == "₹"


def test_load_settings_invalid_currency(
    tmp_path,
    monkeypatch,
):
    settings_file = tmp_path / "invalid_currency.json"

    settings_file.write_text(
        json.dumps(
            {
                "code": "XYZ",
                "symbol": "¤",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config,
        "SETTINGS_FILE",
        settings_file,
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.load_settings()

    assert config.CURRENT_CURRENCY["code"] == "INR"
    assert config.CURRENT_CURRENCY["symbol"] == "₹"


def test_load_settings_corrupted_json(
    tmp_path,
    monkeypatch,
):
    settings_file = tmp_path / "corrupted.json"

    settings_file.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config,
        "SETTINGS_FILE",
        settings_file,
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.load_settings()

    assert config.CURRENT_CURRENCY["code"] == "INR"
    assert config.CURRENT_CURRENCY["symbol"] == "₹"


# ========================================
# CURRENCY VALIDATION TEST
# ========================================


def test_all_configured_currencies_are_valid():
    for code, symbol in config.CURRENCIES.values():
        assert isinstance(code, str)
        assert isinstance(symbol, str)
        assert code
        assert symbol


# ========================================
# CHOOSE CURRENCY TESTS
# ========================================


def test_choose_currency_changes_to_usd(
    monkeypatch,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.choose_currency()

    assert config.CURRENT_CURRENCY["code"] == "USD"
    assert config.CURRENT_CURRENCY["symbol"] == "$"


def test_choose_currency_back_does_not_change(
    monkeypatch,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "5",
    )

    config.CURRENT_CURRENCY["code"] = "INR"
    config.CURRENT_CURRENCY["symbol"] = "₹"

    config.choose_currency()

    assert config.CURRENT_CURRENCY["code"] == "INR"
    assert config.CURRENT_CURRENCY["symbol"] == "₹"
