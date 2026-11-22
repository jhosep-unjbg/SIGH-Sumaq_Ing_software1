import logging
import sys


REQUEST_ID_HEADER = "X-Request-ID"


def configure_operational_logging() -> logging.Logger:
    logger = logging.getLogger("sumaq.api")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s"
            )
        )
        logger.addHandler(handler)

    return logger
