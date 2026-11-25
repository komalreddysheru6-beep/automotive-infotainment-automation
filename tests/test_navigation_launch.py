import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait


def test_navigation_launch():

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

        # Launch Google Maps
        driver.activate_app(maps_package)

        # Verify Google Maps is in the foreground
        WebDriverWait(driver, 20).until(
            lambda d: d.current_package == maps_package
        )

        print("\nCurrent package:", driver.current_package)
        print("Current activity:", driver.current_activity)

        assert driver.current_package == maps_package

        print("Google Maps launched successfully!")
        print("Navigation launch test PASSED!")

    finally:
        if driver is not None:
            driver.quit()
