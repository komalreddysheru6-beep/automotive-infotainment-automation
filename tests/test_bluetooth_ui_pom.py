import os

import subprocess

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.android_bluetooth_page import AndroidBluetoothPage


def test_bluetooth_ui_elements():

    # Step 1: Configure Samsung Android tablet
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:forceAppLaunch", False)
    options.set_capability("appium:dontStopAppOnReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)

    driver = None

    try:
        # Step 2: Connect to Appium
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        driver.update_settings({"waitForIdleTimeout": 0})

        # Step 3: Open Bluetooth Settings
        subprocess.run(
            [
                "adb", "-s", os.environ["ANDROID_UDID"],
                "shell", "am", "start",
                "-a", "android.settings.BLUETOOTH_SETTINGS"
            ],
            check=True,
            timeout=15
        )

        # Step 4: Initialize Bluetooth Page Object
        bluetooth = AndroidBluetoothPage(os.environ["ANDROID_UDID"])

        # Step 5: Inspect current Android activity
        print("Current activity:", driver.current_activity)

        # Step 6: Inspect Bluetooth UI hierarchy
        xml = driver.page_source

        print(
            "Bluetooth switch locator present:",
            bluetooth.BLUETOOTH_SWITCH in xml
        )

        print(
            "Bluetooth page visible:",
            'text="Bluetooth"' in xml
        )

        # Step 7: Wait for Bluetooth UI elements
        wait = WebDriverWait(driver, 15)

        switch = wait.until(
            lambda d: d.find_element(
                By.ID, bluetooth.BLUETOOTH_SWITCH
            )
        )

        assert switch.is_displayed()

        paired = wait.until(
            lambda d: d.find_element(
                By.ID, bluetooth.PAIRED_DEVICES
            )
        )

        assert paired.is_displayed()

        available = wait.until(
            lambda d: d.find_element(
                By.ID, bluetooth.AVAILABLE_DEVICES
            )
        )

        assert available.is_displayed()

        print("Bluetooth Settings UI verified!")
        print("Paired and available device sections detected!")
        print("Automotive Bluetooth UI test PASSED!")

    finally:
        if driver is not None:
            driver.quit()
