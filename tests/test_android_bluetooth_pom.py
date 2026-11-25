import os

from pages.android_bluetooth_page import AndroidBluetoothPage


def test_bluetooth_enabled_using_pom():
    bluetooth_page = AndroidBluetoothPage(
        device_id=os.environ["ANDROID_UDID"]
    )

    assert bluetooth_page.is_bluetooth_enabled(), (
        "Bluetooth is OFF or the adapter state is not ON"
    )

    print("Bluetooth status verified using POM!")
    print("Automotive Bluetooth test PASSED!")
