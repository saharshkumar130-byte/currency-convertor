import unittest

from converter.exceptions import InvalidAmountError, InvalidRateError, UnsupportedCurrencyError
from converter.validators import normalize_currency, parse_amount, parse_rate

CUR = ("USD", "EUR", "CAD")


class TestValidators(unittest.TestCase):
    def test_valid_amount(self):
        self.assertEqual(parse_amount("100.5"), 100.5)

    def test_bad_amounts(self):
        for bad in ("abc", "", "0", "-5", "nan", "inf", None):
            with self.assertRaises(InvalidAmountError, msg=repr(bad)):
                parse_amount(bad)

    def test_bad_rate(self):
        with self.assertRaises(InvalidRateError):
            parse_rate("-1")

    def test_currency_normalised(self):
        self.assertEqual(normalize_currency(" usd ", CUR), "USD")

    def test_unsupported_currency(self):
        with self.assertRaises(UnsupportedCurrencyError):
            normalize_currency("JPY", CUR)


if __name__ == "__main__":
    unittest.main()
