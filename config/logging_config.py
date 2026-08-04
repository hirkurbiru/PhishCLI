"""
PhishCLI - Structured Logging Engine
Configures rotating file logs and clean console log handlers.
"""

import sys
import logging
from logging.handlers import RotatingFileHandler
from config.constants import LOGS_DIR
from config.settings import settings


def setup_logger(name: str = "phishcli") -> logging.Logger:
    """Creates and returns a configured logger instance with rotating file and console output."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Prevent duplicating handlers if already set up
    if logger.handlers:
        return logger

    # Log Formatter
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")

    # File Handler (Rotating log: 5 MB per file, keep 5 backups)
    log_file_path = LOGS_DIR / "phishcli.log"
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console Handler (Used primarily for errors in background tasks)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.ERROR if not settings.DEBUG else logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()