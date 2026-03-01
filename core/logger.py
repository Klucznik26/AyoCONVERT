import logging


def get_logger(name: str) -> logging.Logger:
    """Zwraca logger aplikacji w spójnym namespace."""
    return logging.getLogger(f"ayoconvert.{name}")
