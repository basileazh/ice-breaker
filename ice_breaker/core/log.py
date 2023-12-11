import logging
from datetime import datetime
from typing import Optional

from ice_breaker.core.settings import get_settings

LOG_FILE_PATH = get_settings("log_file_path")


def compute_log_file_path(log_file_path: Optional[str] = LOG_FILE_PATH):
    """
    Compute the log file path, including an hour timestamp at the end
    :param log_file_path: The name of the file to log to.
    :return: The log file path.
    """
    if log_file_path:
        return log_file_path.replace(
            "[DATETIME_PLACEHOLDER]",
            f"_{datetime.now().strftime(get_settings('log_file_path_datetime_format'))}",
        )
    else:
        return None


def create_logger(log_file_path: Optional[str] = LOG_FILE_PATH):
    """
    Create a logger.
    :param log_file_path: The name of the file to log to.
    :return: A logger.
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    c_format = logging.Formatter(get_settings("log_format"))

    # Add formatters to handlers
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    # Add file handler if log_file_path is provided
    if log_file_path:
        log_file_path_ts = compute_log_file_path(log_file_path)
        f_handler = logging.FileHandler(log_file_path_ts, mode="a+", encoding="utf-8")
        f_format = logging.Formatter(get_settings("log_format"))
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger


logger = create_logger(LOG_FILE_PATH)
