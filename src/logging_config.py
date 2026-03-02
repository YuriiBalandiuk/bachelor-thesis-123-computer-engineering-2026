import logging
import logging.config


def setup_logging(name: str) -> None:
    """
    Configure Python logging with a standard stdout formatter.

    Initializes the root logger to output INFO-level and higher
    messages to standard output. Log messages include timestamp,
    log level, logger name, and message content.

    Args:
        name: Name of the logger (currently not used but reserved
            for future named logger configuration).

    Notes:
        - The formatter uses the pattern:
          "%(asctime)s: %(levelname)s - {%(name)s} - %(message)s:"
        - Existing loggers are preserved and not disabled.
        - The handler writes to standard output stream.
    """
    logging.config.dictConfig(
        {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s: %(levelname)s - {%(name)s} - %(message)s:"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["stdout"],
        },
    }
)
