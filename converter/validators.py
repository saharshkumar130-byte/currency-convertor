"""Input validation helpers. All raise custom exceptions on bad input."""
import math

from .exceptions import InvalidAmountError, InvalidRateError, UnsupportedCurrencyError


def _to_positive_float(raw):
    value = float(str(raw).strip())          # ValueError on garbage
    if not math.isfinite(value) or value <= 0:
        raise ValueError("must be positive and finite")
    return value


def parse_amount(raw):
    """Return a positive float or raise InvalidAmountError."""
    try:
        return _to_positive_float(raw)
    except (ValueError, TypeError):
        raise InvalidAmountError(f"Invalid amount: {raw!r}") from None


def parse_rate(raw):
    """Return a positive float rate or raise InvalidRateError."""
    try:
        return _to_positive_float(raw)
    except (ValueError, TypeError):
        raise InvalidRateError(f"Invalid rate: {raw!r}") from None


def normalize_currency(raw, supported):
    """Uppercase/strip a currency code and check it is supported."""
    code = str(raw).strip().upper()
    if code not in supported:
        raise UnsupportedCurrencyError(
            f"Unsupported currency: {raw!r}. Choose from {', '.join(supported)}"
        )
    return code
