import logging
import sys
from tasque.constants import TASQUE_LOGGING_LEVEL


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(TASQUE_LOGGING_LEVEL)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.debug(f"Created logger '${name}'.")
    return logger
