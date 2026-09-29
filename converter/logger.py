"""Logging setup (rotating file)."""
import logging
from logging.handlers import RotatingFileHandler

from .config import LOG_DIR, LOG_FILE


def get_logger(name="currency_converter"):
    logger = logging.getLogger(name)
    if logger.handlers:          # already configured
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(LOG_FILE, maxBytes=200_000, backupCount=2, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except OSError:              # read-only disk etc. - app must still run
        logger.addHandler(logging.NullHandler())
    return logger
