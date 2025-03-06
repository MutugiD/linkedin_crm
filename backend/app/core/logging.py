import os
import sys
from datetime import datetime

from loguru import logger

from app.core.config import settings


def setup_logging():
    """
    Set up logging configuration using loguru.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure loguru
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": settings.LOG_LEVEL,
            },
            {
                "sink": settings.LOG_FILE,
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                "level": settings.LOG_LEVEL,
                "rotation": "500 MB",
                "retention": "10 days",
                "compression": "zip",
            },
        ],
    }

    # Remove default logger
    logger.remove()

    # Add configured handlers
    for handler in config["handlers"]:
        logger.add(**handler)

    logger.info(f"Logging configured with level {settings.LOG_LEVEL}")
    logger.info(f"Environment: {settings.APP_ENV}")

    return logger


# Initialize logger
logger = setup_logging()