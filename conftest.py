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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Log failures and capture screenshots when possible."""

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

        # Capture screenshots only during test execution.
        if report.when != "call":
            return

        # Use only a real driver fixture, not mock_driver.
        driver = item.funcargs.get("driver")

        if driver is None:
            logger.info(
                "Screenshot skipped: no real driver available"
            )
            return

        try:
            from pathlib import Path
            import re

            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            safe_name = re.sub(
                r"[^a-zA-Z0-9_-]",
                "_",
                item.nodeid
            )

            screenshot_path = (
                screenshot_dir / f"{safe_name}.png"
            )

            success = driver.save_screenshot(
                str(screenshot_path)
            )

            if success:
                logger.info(
                    "Screenshot saved: %s",
                    screenshot_path
                )
            else:
                logger.warning(
                    "Driver did not save screenshot"
                )

        except Exception:
            logger.exception(
                "Screenshot capture failed"
            )
