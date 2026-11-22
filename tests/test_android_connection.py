
import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture
def android_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]
    options.no_reset = True

    options.set_capability("appium:ignoreHiddenApiPolicyError", True)
    options.set_capability("appium:autoGrantPermissions", False)

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    try:
        yield driver
    finally:
        driver.quit()


def test_android_connection(android_driver):
    assert android_driver.session_id is not None

    print("Appium session connected successfully")


def test_android_screenshot(android_driver):
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)

    screenshot_path = screenshot_dir / "poco_x3.png"

    assert android_driver.save_screenshot(
        str(screenshot_path)
    )

    assert screenshot_path.exists()
