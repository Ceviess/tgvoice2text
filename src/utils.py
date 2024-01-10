"""
Utility functions for common tasks
"""

import logging


def get_logger(logger_name: str) -> logging.Logger:
    """
    Create and configure a logger with the specified name.

    :param logger_name: Name for the logger.
    :type logger_name: str
    :return: Configured logger instance.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler("log.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    return logger
