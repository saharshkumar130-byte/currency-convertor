import tempfile
import unittest
from pathlib import Path

from converter.exceptions import InvalidRateError
from converter.rates import RateManager


class TestRates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "rates.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_defaults_created(self):
        rm = RateManager(self.path)
        self.assertEqual(rm.get_rate("USD", "EUR"), 0.85)
        self.assertTrue(self.path.exists())

    def test_update_persists(self):
        RateManager(self.path).set_rate("usd", "eur", "0.9")
        self.assertEqual(RateManager(self.path).get_rate("USD", "EUR"), 0.9)

    def test_invalid_rate(self):
        with self.assertRaises(InvalidRateError):
            RateManager(self.path).set_rate("USD", "EUR", "-2")

    def test_corrupt_file_falls_back(self):
        self.path.write_text("{ not json")
        self.assertEqual(RateManager(self.path).get_rate("USD", "CAD"), 1.25)

    def test_reset(self):
        rm = RateManager(self.path)
        rm.set_rate("USD", "EUR", 2)
        rm.reset_to_defaults()
        self.assertEqual(rm.get_rate("USD", "EUR"), 0.85)


if __name__ == "__main__":
    unittest.main()
