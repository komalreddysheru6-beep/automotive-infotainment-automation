import os

from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_samsung_ui_elements():
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

        driver.press_keycode(3)

        xml = driver.page_source

        assert "<hierarchy" in xml

        with open(
            "reports/samsung_home_ui.xml",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(xml)

        print("Samsung Home UI hierarchy saved!")

    finally:
        if driver is not None:
            driver.quit()
