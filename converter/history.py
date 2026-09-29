"""Module 3 - Conversion history (CRUD) and analytics report."""
import json
from collections import Counter

from .config import HISTORY_FILE, MAX_HISTORY_ENTRIES
from .exceptions import HistoryError
from .logger import get_logger

log = get_logger()


class HistoryManager:
    def __init__(self, path=HISTORY_FILE, max_entries=MAX_HISTORY_ENTRIES):
        self.path = path
        self.max_entries = max_entries
        self._items = self._load()

    def _load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except (ValueError, OSError) as exc:
            log.warning("Could not read history (%s); starting empty", exc)
            return []

    def _save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._items, f, indent=2)
        except OSError as exc:
            log.error("Could not save history: %s", exc)

    # ---------- CRUD ----------
    def add(self, result):
        self._items.append(result.to_dict())
        self._items = self._items[-self.max_entries:]     # bounded size
        self._save()

    def list_all(self):
        return list(self._items)

    def get(self, index):
        """1-based index."""
        if not 1 <= index <= len(self._items):
            raise HistoryError(f"No history entry #{index}")
        return self._items[index - 1]

    def delete(self, index):
        entry = self.get(index)
        del self._items[index - 1]
        self._save()
        log.info("Deleted history entry #%s", index)
        return entry

    def clear(self):
        self._items = []
        self._save()
        log.info("History cleared")

    # ---------- analytics ----------
    def summary(self):
        if not self._items:
            return {"count": 0, "pairs": {}, "most_used": None, "totals": {}}
        pairs = Counter(f"{e['source']}->{e['target']}" for e in self._items)
        totals = Counter()
        for e in self._items:
            totals[e["source"]] += e["amount"]
        return {
            "count": len(self._items),
            "pairs": dict(pairs),
            "most_used": pairs.most_common(1)[0][0],
            "totals": dict(totals),
        }
