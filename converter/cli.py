"""Command-line interface: ties the three modules together."""
from .converter import CurrencyConverter
from .exceptions import CurrencyConverterError
from .history import HistoryManager
from .logger import get_logger
from .rates import RateManager

log = get_logger()

MENU = """
===== Currency Converter =====
1. Convert currency
2. View exchange rates
3. Update an exchange rate
4. View conversion history
5. Delete a history entry
6. History report
7. Clear history
0. Exit
"""


def ask(prompt):
    return input(prompt).strip()


def do_convert(conv, hist):
    amount = ask("Enter the amount: ")
    src = ask(f"Source currency ({'/'.join(conv.currencies)}): ")
    tgt = ask(f"Target currency ({'/'.join(conv.currencies)}): ")
    result = conv.convert(amount, src, tgt)
    hist.add(result)
    print(result)


def do_view_rates(conv, _hist):
    for src, targets in conv.rates.all_rates().items():
        for tgt, rate in targets.items():
            print(f"  1 {src} = {rate} {tgt}")


def do_update_rate(conv, _hist):
    src = ask("Source currency: ")
    tgt = ask("Target currency: ")
    rate = conv.rates.set_rate(src, tgt, ask("New rate: "))
    print(f"Updated: 1 {src.upper()} = {rate} {tgt.upper()}")


def do_view_history(_conv, hist):
    items = hist.list_all()
    if not items:
        print("No history yet.")
    for i, e in enumerate(items, 1):
        print(f"  {i}. [{e['timestamp']}] {e['amount']:g} {e['source']} -> "
              f"{e['result']:.2f} {e['target']}")


def do_delete_history(_conv, hist):
    try:
        idx = int(ask("Entry number to delete: "))
    except ValueError:
        print("Error: please enter a whole number.")
        return
    hist.delete(idx)
    print("Deleted.")


def do_report(_conv, hist):
    s = hist.summary()
    print(f"Total conversions: {s['count']}")
    if s["count"]:
        print(f"Most used pair:    {s['most_used']}")
        for pair, n in s["pairs"].items():
            print(f"  {pair}: {n}")
        for cur, tot in s["totals"].items():
            print(f"  Total converted from {cur}: {tot:g}")


def do_clear(_conv, hist):
    if ask("Really clear all history? (y/N): ").lower() == "y":
        hist.clear()
        print("History cleared.")


ACTIONS = {
    "1": do_convert, "2": do_view_rates, "3": do_update_rate,
    "4": do_view_history, "5": do_delete_history, "6": do_report, "7": do_clear,
}


def run():
    conv = CurrencyConverter(RateManager())
    hist = HistoryManager()
    log.info("Application started")
    while True:
        print(MENU)
        try:
            choice = ask("Choose an option: ")
            if choice == "0":
                print("Goodbye!")
                log.info("Application exited")
                return
            action = ACTIONS.get(choice)
            if action is None:
                print("Invalid option.")
                continue
            action(conv, hist)
        except CurrencyConverterError as exc:
            log.warning("User error: %s", exc)
            print(f"Error: {exc}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return
        except Exception:                      # last-resort safety net
            log.exception("Unexpected error")
            print("Unexpected error - see logs/app.log")
