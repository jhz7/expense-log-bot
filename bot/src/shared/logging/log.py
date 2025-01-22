import logging

format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logging.basicConfig(format=format, level=logging.DEBUG)


def Logger(module) -> logging.Logger:
    return logging.getLogger(module)
