"""Custom exceptions so every failure has a clear, catchable type."""


class CurrencyConverterError(Exception):
    """Base class for all application errors."""


class InvalidAmountError(CurrencyConverterError):
    """Amount is not a positive, finite number."""


class UnsupportedCurrencyError(CurrencyConverterError):
    """Currency code is not in the supported list."""


class RateNotFoundError(CurrencyConverterError):
    """No exchange rate is stored for the requested currency pair."""


class InvalidRateError(CurrencyConverterError):
    """Exchange rate is not a positive, finite number."""


class HistoryError(CurrencyConverterError):
    """History entry could not be found or stored."""
