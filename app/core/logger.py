import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.request_context import (
    get_request_id,
)

LOG_DIR = Path("logs")

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("circle-wallet-manager")

logger.propagate = False

# logger.setLevel(logging.INFO)
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

logger.setLevel(LOG_LEVEL)

class RequestIdFilter(logging.Filter):

    def filter(
        self,
        record,
    ):

        record.request_id = (
            get_request_id()
        )

        return True

formatter = logging.Formatter(
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(request_id)s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

file_handler = RotatingFileHandler(

    LOG_FILE,

    maxBytes=1_000_000,

    backupCount=5,

    encoding="utf-8",
)

file_handler.addFilter(
    RequestIdFilter()
)

file_handler.setFormatter(
    formatter
)

if not logger.handlers:

    logger.addHandler(
        file_handler
    )

    console_handler = logging.StreamHandler()

    console_handler.addFilter(
        RequestIdFilter()
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

logger.info(

    "event=logger_initialized "

    f"log_level={LOG_LEVEL}"
)