import os

import subprocess
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.samsung_phone_page import SamsungPhonePage


DEVICE_ID = os.environ["ANDROID_UDID"]


@pytest.fixture(scope="module")
def phone():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = DEVICE_ID

    options.set_capability("appium:noReset", True)
    options.set_capability(
        "appium:skipDeviceInitialization", True
    )

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    page = SamsungPhonePage(driver)

    try:

        subprocess.run(
            [
                "adb", "-s", DEVICE_ID,
                "shell", "am", "start",
                "-a", "android.intent.action.DIAL",
                "-p", page.PACKAGE
            ],
            check=True,
            timeout=30
        )

        page.launch()

        yield page

    finally:

        try:
            page.clear_number()
        finally:
            driver.quit()


def test_phone_launch(phone):

    assert phone.driver.current_package == phone.PACKAGE

    print("Phone application launch: PASSED")


def test_keypad_visibility(phone):

    assert phone.is_keypad_visible()

    print("Keypad visibility: PASSED")


def test_all_number_keys(phone):

    assert phone.verify_number_keys()

    print("All ten number keys: PASSED")


def test_phone_number_entry(phone):

    phone.clear_number()

    test_number = "0123456789"

    phone.enter_number(test_number)

    assert phone.get_entered_number() == test_number

    print("Number entry: PASSED")


def test_delete_digit(phone):

    phone.clear_number()
    phone.enter_number("12345")

    phone.delete_digit()

    assert phone.get_entered_number() == "1234"

    print("Delete digit: PASSED")


def test_clear_number(phone):

    phone.clear_number()
    phone.enter_number("12345")

    phone.clear_number()

    assert phone.get_entered_number() == ""

    print("Clear number: PASSED")


def test_call_button(phone):

    phone.clear_number()
    phone.enter_number("0123456789")

    assert phone.is_call_button_visible()

    print(
        "Call button enabled:",
        phone.is_call_button_enabled()
    )

    print("Call button visibility: PASSED")
    print("Actual call intentionally not initiated")

    phone.clear_number()



def test_sim_status():

    result = subprocess.run(
        [
            "adb", "-s", DEVICE_ID,
            "shell", "getprop", "gsm.sim.state"
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=15
    )

    status = result.stdout.strip()

    print(f"SIM status: {status}")

    if not status:
        pytest.skip("SIM status property unavailable")

    states = [
        state.strip()
        for state in status.upper().split(",")
    ]

    expected_states = {"ABSENT", "NOT_READY"}

    assert all(
        state in expected_states
        for state in states
    ), f"Unexpected SIM state: {status}"

    print("No ready SIM detected: PASSED")
    print("SIM environment validation: PASSED")


def test_phone_screenshot(phone):

    folder = Path("reports/screenshots")
    folder.mkdir(parents=True, exist_ok=True)

    phone.clear_number()

    assert phone.driver.save_screenshot(
        str(folder / "phone_integration.png")
    )

    print("Phone screenshot: Saved")
