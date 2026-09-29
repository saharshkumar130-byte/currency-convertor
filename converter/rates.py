"""Module 2 - Exchange-rate management (view / update / persist)."""
import copy
import json

from .config import DEFAULT_RATES, RATES_FILE, SUPPORTED_CURRENCIES
from .exceptions import RateNotFoundError
from .logger import get_logger
from .validators import normalize_currency, parse_rate

log = get_logger()


class RateManager:
    """Stores rates in a JSON file; falls back to defaults if it is missing/corrupt."""

    def __init__(self, path=RATES_FILE, defaults=None, currencies=SUPPORTED_CURRENCIES):
        self.path = path
        self.currencies = tuple(currencies)
        self._defaults = defaults or DEFAULT_RATES
        self._rates = self._load()

    # ---------- persistence ----------
    def _load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("rates file must contain an object")
            return data
        except FileNotFoundError:
            log.info("Rates file not found; creating with defaults")
        except (ValueError, OSError) as exc:
            log.warning("Could not read rates file (%s); using defaults", exc)
        rates = copy.deepcopy(self._defaults)
        self._save(rates)
        return rates

    def _save(self, rates=None):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(rates if rates is not None else self._rates, f, indent=2)
        except OSError as exc:
            log.error("Could not save rates: %s", exc)

    # ---------- operations ----------
    def get_rate(self, source, target):
        if source == target:
            return 1.0
        try:
            return float(self._rates[source][target])
        except (KeyError, TypeError, ValueError):
            raise RateNotFoundError(f"No rate for {source} -> {target}") from None

    def set_rate(self, source, target, new_rate):
        source = normalize_currency(source, self.currencies)
        target = normalize_currency(target, self.currencies)
        rate = parse_rate(new_rate)
        self._rates.setdefault(source, {})[target] = rate
        self._save()
        log.info("Rate updated %s->%s = %s", source, target, rate)
        return rate

    def reset_to_defaults(self):
        self._rates = copy.deepcopy(self._defaults)
        self._save()
        log.info("Rates reset to defaults")

    def all_rates(self):
        return copy.deepcopy(self._rates)
