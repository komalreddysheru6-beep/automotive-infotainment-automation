
from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_samsung_connection():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Samsung Galaxy Tab S10 FE+"
    options.udid = "R52Y705H82J"

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:newCommandTimeout", 120)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        print("Samsung tablet connected successfully!")
        print("Session ID:", driver.session_id)

        assert driver.session_id is not None

    finally:
        if driver is not None:
            driver.quit()
