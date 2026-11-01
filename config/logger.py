"""
Centralized logging system for AI Backend Engineering Lab.

Features:
- Console logging
- File logging
- Log rotation
- Configurable log levels
- Duplicate handler prevention
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import get_settings


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

# Log file configuration
LOG_FILE = LOG_DIR / "app.log"

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5


def get_logger(name: str = "ai_backend") -> logging.Logger:
    """
    Create and return a configured application logger.

    Args:
        name: Logger name.

    Returns:
        Configured logging.Logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if getattr(logger, "_configured", False):
        return logger

    settings = get_settings()

    # Configure logging level
    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO
    )

    logger.setLevel(log_level)
    logger.propagate = False

    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Log format
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Mark logger as configured
    logger._configured = True

    return logger