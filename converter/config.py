"""Central configuration: paths, supported currencies and default rates."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

RATES_FILE = DATA_DIR / "rates.json"
HISTORY_FILE = DATA_DIR / "history.json"
LOG_FILE = LOG_DIR / "app.log"

SUPPORTED_CURRENCIES = ("USD", "EUR", "CAD")

# Direct rates: DEFAULT_RATES[source][target]
DEFAULT_RATES = {
    "USD": {"EUR": 0.85, "CAD": 1.25},
    "EUR": {"USD": 1.18, "CAD": 1.47},
    "CAD": {"USD": 0.80, "EUR": 0.68},
}

MAX_HISTORY_ENTRIES = 500
