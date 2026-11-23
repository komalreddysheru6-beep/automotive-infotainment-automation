import pytest
from unittest.mock import MagicMock
from simulator.infotainment import InfotainmentSystem


@pytest.fixture
def infotainment():
    system = InfotainmentSystem()
    system.start_system()
    return system

@pytest.fixture
def mock_driver():
    """Reusable mock Appium driver for POM unit tests."""
    return MagicMock()



from utils.logger import get_logger

logger = get_logger("PyTest")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Log test failures automatically."""

    outcome = yield
    report = outcome.get_result()

    if report.failed:
        logger.error(
            "Test failed: %s | Phase: %s",
            item.nodeid,
            report.when
        )
        logger.error(
            "Failure details: %s",
            report.longreprtext
        )
