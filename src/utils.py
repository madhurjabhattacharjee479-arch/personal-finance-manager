from datetime import date
from decimal import Decimal, InvalidOperation

ALLOWED_CATEGORIES = {
    "food": "Food",
    "transport": "Transport",
    "entertainment": "Entertainment",
    "shopping": "Shopping",
    "other": "Other",
}


def validate_amount(value):
    """
    Validate and convert an expense amount to Decimal.

    Args:
        value: The amount to validate (int, float, or numeric string).

    Returns:
        A Decimal value rounded to two decimal places.

    Raises:
        ValueError: If the value is non-numeric, zero, or negative.
    """
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError(
            f"Amount must be a valid number. Received: {value!r}"
        ) from error

    if amount <= 0:
        raise ValueError(f"Amount must be greater than zero. Received: {value!r}")

    return amount


def validate_date(value):
    """
    Validate a date string in YYYY-MM-DD format.

    Args:
        value: The date string to validate.

    Returns:
        The validated date as a string in YYYY-MM-DD format.

    Raises:
        TypeError: If value is not a string.
        ValueError: If the date format is invalid or the date does not exist.
    """
    if not isinstance(value, str):
        raise TypeError(
            f"Date must be a string in YYYY-MM-DD format. Received: {value!r}"
        )

    cleaned_date = value.strip()

    try:
        parsed_date = date.fromisoformat(cleaned_date)
    except ValueError as error:
        raise ValueError(
            f"Date must be a valid date in YYYY-MM-DD format. Received: {value!r}"
        ) from error

    return parsed_date.isoformat()


def validate_category(value):
    """
    Validate an expense category against the allowed list.

    Matching is case-insensitive, but the function returns the standard
    capitalization (e.g. "food" -> "Food").

    Args:
        value: The category string to validate.

    Returns:
        The validated category with standard capitalization.

    Raises:
        TypeError: If value is not a string.
        ValueError: If the category is empty or invalid.
    """
    if not isinstance(value, str):
        raise TypeError(f"Category must be a string. Received: {value!r}")

    cleaned_category = value.strip()

    if not cleaned_category:
        raise ValueError("Category cannot be empty.")

    normalized_category = ALLOWED_CATEGORIES.get(cleaned_category.lower())

    if normalized_category is None:
        allowed = ", ".join(ALLOWED_CATEGORIES.values())
        raise ValueError(f"Invalid category: {value!r}. Allowed categories: {allowed}")

    return normalized_category


def validate_description(value):
    """
    Validate an expense description.

    Args:
        value: The description string to validate.

    Returns:
        The cleaned description with leading and trailing whitespace removed.

    Raises:
        TypeError: If value is not a string.
        ValueError: If the description is empty.
    """
    if not isinstance(value, str):
        raise TypeError(f"Description must be a string. Received: {value!r}")

    cleaned_description = value.strip()

    if not cleaned_description:
        raise ValueError("Description cannot be empty.")

    return cleaned_description
