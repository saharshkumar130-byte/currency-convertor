import tempfile
import unittest
from pathlib import Path

from converter.converter import CurrencyConverter
from converter.exceptions import HistoryError
from converter.history import HistoryManager
from converter.rates import RateManager


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.conv = CurrencyConverter(RateManager(d / "rates.json"))
        self.path = d / "history.json"
        self.hist = HistoryManager(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def _add(self, amt, s, t):
        self.hist.add(self.conv.convert(amt, s, t))

    def test_add_and_persist(self):
        self._add(10, "USD", "EUR")
        self.assertEqual(len(HistoryManager(self.path).list_all()), 1)

    def test_delete(self):
        self._add(10, "USD", "EUR")
        self.hist.delete(1)
        self.assertEqual(self.hist.list_all(), [])

    def test_bad_index(self):
        with self.assertRaises(HistoryError):
            self.hist.delete(3)

    def test_summary(self):
        self._add(10, "USD", "EUR")
        self._add(20, "USD", "EUR")
        self._add(5, "EUR", "CAD")
        s = self.hist.summary()
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["most_used"], "USD->EUR")
        self.assertEqual(s["totals"]["USD"], 30)

    def test_max_entries(self):
        h = HistoryManager(self.path, max_entries=2)
        for _ in range(4):
            h.add(self.conv.convert(1, "USD", "EUR"))
        self.assertEqual(len(h.list_all()), 2)

    def test_clear(self):
        self._add(1, "USD", "EUR")
        self.hist.clear()
        self.assertEqual(self.hist.summary()["count"], 0)


if __name__ == "__main__":
    unittest.main()
