import logging
from logging import Logger

format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(format=format, level=logging.ERROR)
logging.basicConfig(format=format, level=logging.INFO)
logging.basicConfig(format=format, level=logging.DEBUG)


def Logger(module) -> Logger:
    return logging.getLogger(module)
