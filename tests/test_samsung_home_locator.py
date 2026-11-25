import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_samsung_home_locator():
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

        # Navigate to Samsung Home screen
        driver.press_keycode(3)

        # Locate the actual Samsung Home screen element
        home_screen = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "com.sec.android.app.launcher:id/home_screen"
                )
            )
        )

        assert home_screen is not None

        print("Samsung Home screen located successfully!")

    finally:
        if driver is not None:
            driver.quit()
