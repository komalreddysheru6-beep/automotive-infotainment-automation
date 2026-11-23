
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_bluetooth_ui_xml():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "R52Y705H82J"
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:forceAppLaunch", False)
    options.set_capability("appium:dontStopAppOnReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        driver.update_settings({
            "waitForIdleTimeout": 0
        })

        xml = driver.page_source

        output = Path("reports/bluetooth_ui.xml")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(xml, encoding="utf-8")

        assert xml.strip()
        print("Bluetooth UI hierarchy saved!")

    finally:
        if driver is not None:
            driver.quit()
