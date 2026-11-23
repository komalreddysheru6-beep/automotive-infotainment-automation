
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_samsung_screenshot():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Samsung Galaxy Tab S10 FE+"
    options.udid = "R52Y705H82J"

    options.set_capability("appium:noReset", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        screenshot_path = (
            screenshot_dir / "samsung_real_device.png"
        )

        assert driver.save_screenshot(
            str(screenshot_path)
        )

        assert screenshot_path.is_file()

        print("Screenshot saved:", screenshot_path)

    finally:
        if driver is not None:
            driver.quit()
