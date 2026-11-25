import os

import subprocess
import time

import pytest


DEVICE_ID = os.environ["ANDROID_UDID"]


def adb_shell(*args):

    result = subprocess.run(
        ["adb", "-s", DEVICE_ID, "shell", *args],
        capture_output=True,
        text=True,
        check=True,
        timeout=20
    )

    return result.stdout.strip()


def get_setting(namespace, key):

    return adb_shell(
        "settings", "get", namespace, key
    )


def set_setting(namespace, key, value):

    adb_shell(
        "settings", "put", namespace, key, str(value)
    )


def test_android_version():

    version = adb_shell(
        "getprop", "ro.build.version.release"
    )

    assert version

    print(f"Android version: {version}")


def test_device_model():

    model = adb_shell(
        "getprop", "ro.product.model"
    )

    assert model

    print(f"Device model: {model}")


def test_battery_status():

    output = adb_shell("dumpsys", "battery")

    values = {}

    for line in output.splitlines():

        if ":" in line:

            key, value = line.strip().split(":", 1)
            values[key.strip()] = value.strip()

    level = int(values["level"])

    assert 0 <= level <= 100

    print(f"Battery level: {level}%")
    print(f"Battery status: {values.get('status')}")


def test_wifi_status():

    status = get_setting(
        "global", "wifi_on"
    )

    assert status in {"0", "1", "2", "3"}

    print(f"Wi-Fi state value: {status}")


def test_airplane_mode_status():

    status = get_setting(
        "global", "airplane_mode_on"
    )

    assert status in {"0", "1"}

    print(
        "Airplane mode:",
        "ON" if status == "1" else "OFF"
    )


def test_screen_brightness():

    original = get_setting(
        "system", "screen_brightness"
    )

    if not original.isdigit():
        pytest.skip("Brightness setting unavailable")

    try:

        for brightness in [100, 180]:

            set_setting(
                "system",
                "screen_brightness",
                brightness
            )

            time.sleep(1)

            actual = get_setting(
                "system", "screen_brightness"
            )

            assert actual == str(brightness)

            print(f"Brightness setting verified: {actual}")

    finally:

        set_setting(
            "system", "screen_brightness", original
        )

        assert get_setting(
            "system", "screen_brightness"
        ) == original

        print("Original brightness setting restored")


def test_screen_timeout():

    original = get_setting(
        "system", "screen_off_timeout"
    )

    if not original.isdigit():
        pytest.skip("Screen timeout setting unavailable")

    try:

        set_setting(
            "system", "screen_off_timeout", 60000
        )

        actual = get_setting(
            "system", "screen_off_timeout"
        )

        assert actual == "60000"

        print("Screen timeout setting: 60 seconds")

    finally:

        set_setting(
            "system", "screen_off_timeout", original
        )

        assert get_setting(
            "system", "screen_off_timeout"
        ) == original

        print("Original screen timeout restored")


def test_system_settings_launch():

    adb_shell(
        "am", "start", "-W",
        "-a", "android.settings.SETTINGS"
    )

    output = adb_shell(
        "dumpsys", "activity", "activities"
    )

    resumed = [
        line for line in output.splitlines()
        if "resumedactivity" in line.lower()
    ]

    assert any(
        "com.android.settings" in line
        for line in resumed
    )

    print("System Settings launch: PASSED")
