import sys
import logging

LOG_FMT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def init_logging(level=logging.INFO, stream=sys.stdout):
    logging.basicConfig(level=level, format=LOG_FMT, stream=stream)
    logging.info("logging initialized, level: %s", level)
