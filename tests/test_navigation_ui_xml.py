import os

from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait


def test_navigation_ui_xml():

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)

    driver = None
    maps_package = "com.google.android.apps.maps"

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        driver.activate_app(maps_package)

        WebDriverWait(driver, 20).until(
            lambda d: d.current_package == maps_package
        )

        xml = driver.page_source

        Path("reports").mkdir(exist_ok=True)

        Path("reports/navigation_ui.xml").write_text(
            xml,
            encoding="utf-8"
        )

        assert maps_package in xml

        print("\nGoogle Maps UI captured successfully!")
        print("Saved: reports/navigation_ui.xml")

    finally:
        if driver is not None:
            driver.quit()
