import tempfile
import unittest
from pathlib import Path

from converter.converter import CurrencyConverter
from converter.exceptions import InvalidAmountError, RateNotFoundError, UnsupportedCurrencyError
from converter.rates import RateManager


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conv = CurrencyConverter(RateManager(Path(self.tmp.name) / "rates.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_usd_to_eur(self):
        self.assertAlmostEqual(self.conv.convert(100, "USD", "EUR").result, 85.0)

    def test_same_currency(self):
        self.assertEqual(self.conv.convert(50, "cad", "CAD").result, 50)

    def test_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.conv.convert("abc", "USD", "EUR")

    def test_unsupported_currency(self):
        with self.assertRaises(UnsupportedCurrencyError):
            self.conv.convert(10, "USD", "JPY")

    def test_missing_rate(self):
        self.conv.rates._rates["USD"].pop("EUR")
        with self.assertRaises(RateNotFoundError):
            self.conv.convert(10, "USD", "EUR")


if __name__ == "__main__":
    unittest.main()
