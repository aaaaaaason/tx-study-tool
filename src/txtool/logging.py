"""Provide logging utility"""
import logging


def _get_logging_level(level: str) -> int:
    """Returns logging level for Python logging module from str.

    Args:
      level: a string which is expected to get from environment variables.
    Returns:
      Corrsponding logging level defined in Python logging module.
    """
    mapping = {
        "FATAL": logging.FATAL,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR,
    }
    return mapping.get(level, logging.INFO)


def setup(level: str = "INFO", fmt: str = None):
    """Setup default logger

    Args:
      level: Logging level, which may be read from environment variables.
      fmt: Message format for logging.
    """
    if not fmt:
        fmt = "%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s"

    logging.basicConfig(format=fmt,
                        level=_get_logging_level(level),
                        force=True)
