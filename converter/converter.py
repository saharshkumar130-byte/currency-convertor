"""Module 1 - Core conversion logic."""
from dataclasses import dataclass, asdict
from datetime import datetime

from .config import SUPPORTED_CURRENCIES
from .logger import get_logger
from .rates import RateManager
from .validators import normalize_currency, parse_amount

log = get_logger()


@dataclass
class ConversionResult:
    amount: float
    source: str
    target: str
    rate: float
    result: float
    timestamp: str

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return f"{self.amount:g} {self.source} is equal to {self.result:.2f} {self.target}"


class CurrencyConverter:
    def __init__(self, rate_manager=None, currencies=SUPPORTED_CURRENCIES):
        self.rates = rate_manager or RateManager()
        self.currencies = tuple(currencies)

    def convert(self, amount, source, target):
        """Validate inputs, look up the rate and return a ConversionResult."""
        amount = parse_amount(amount)
        source = normalize_currency(source, self.currencies)
        target = normalize_currency(target, self.currencies)
        rate = self.rates.get_rate(source, target)
        result = ConversionResult(
            amount=amount, source=source, target=target, rate=rate,
            result=amount * rate,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )
        log.info("Converted %s %s -> %s %s", amount, source, result.result, target)
        return result
