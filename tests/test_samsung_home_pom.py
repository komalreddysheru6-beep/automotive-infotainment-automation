import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.samsung_home_page import SamsungHomePage


def test_samsung_home_using_pom():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]

    options.set_capability("appium:noReset", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        home_page = SamsungHomePage(driver)

        home_page.open_home()

        assert home_page.is_home_displayed(), (
            "Samsung Home screen was not found"
        )

        print("Real Samsung Home POM test passed!")

    finally:
        if driver is not None:
            driver.quit()
