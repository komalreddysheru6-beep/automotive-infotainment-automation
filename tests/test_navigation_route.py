import os

from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.google_maps_page import GoogleMapsPage


def test_navigation_route():

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        maps = GoogleMapsPage(driver)
        maps.launch()

        wait = WebDriverWait(driver, 30)

        directions = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "Directions")
            )
        )

        assert directions.is_displayed()
        print("\nDirections button verified")

        directions.click()
        print("Directions button clicked")

        wait.until(
            lambda d: any(
                marker in d.page_source.lower()
                for marker in [
                    "choose starting point",
                    "your location",
                    "choose destination",
                    "route options"
                ]
            )
        )

        Path("reports").mkdir(exist_ok=True)

        Path("reports/navigation_route.xml").write_text(
            driver.page_source,
            encoding="utf-8"
        )

        print("Directions screen detected")
        print("Route UI captured successfully")
        print("Navigation route test PASSED!")

    finally:
        if driver is not None:
            driver.quit()
