import pytest


@pytest.fixture
def debug_log():
    import logging
    from tls import util

    util.init_logging(level=logging.DEBUG)
