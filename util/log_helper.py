import logging

import colorama

LEVEL = logging.DEBUG


class ProjectLogFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith("businessman.")


class ColorFormatter(logging.Formatter):
    WHITE = "\033[97m"
    SLIGHTLY_DARKER_WHITE = "\033[38;5;250m"
    YELLOW = "\033[93m"
    ORANGE = "\033[33m"
    RED = "\033[91m"
    DARK_RED = "\033[31m"
    RESET = "\033[0m"

    COLORS = {
        logging.INFO: SLIGHTLY_DARKER_WHITE,
        logging.DEBUG: ORANGE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: DARK_RED,
        "DEFAULT": WHITE,
    }

    def __init__(self, fmt="%(message)s", datefmt="%I:%M:%S %p", style="%"):
        super().__init__(fmt, datefmt, style)
        colorama.init()

    def format(self, record):
        log = super().format(record)
        color = self.COLORS.get(record.levelno, self.COLORS["DEFAULT"])
        return f"{color}{log}{self.RESET}"


def get_logger(name):
    global LEVEL
    logger = logging.getLogger(f"businessman.{name}")
    logger.setLevel(LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LEVEL)
    handler.setFormatter(
        ColorFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s AT %(lineno)d -> %(message)s"
        )
    )
    handler.addFilter(ProjectLogFilter())
    logger.addHandler(handler)
    return logger
