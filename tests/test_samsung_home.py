
from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_samsung_home_button():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "R52Y705H82J"

    options.set_capability("appium:noReset", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        # Android KEYCODE_HOME = 3
        driver.press_keycode(3)

        print("Home button pressed successfully!")

        assert driver.current_package is not None

    finally:
        if driver is not None:
            driver.quit()
