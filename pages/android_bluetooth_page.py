
import subprocess


class AndroidBluetoothPage:
    """Real Android Bluetooth status verification using ADB."""


    # Samsung Bluetooth Settings UI locators
    BLUETOOTH_SWITCH = (
        "com.android.settings:id/sesl_switchbar_container"
    )

    PAIRED_DEVICES = (
        "com.android.settings:id/paired_device_category"
    )

    AVAILABLE_DEVICES = (
        "com.android.settings:id/available_device_category"
    )

    SCAN_BUTTON_XPATH = (
        '//android.widget.Button[@text="Scan"]'
    )


    def __init__(self, device_id):
        self.device_id = device_id

    def get_bluetooth_status(self):
        result = subprocess.run(
            [
                "adb",
                "-s",
                self.device_id,
                "shell",
                "dumpsys",
                "bluetooth_manager"
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )

        return result.stdout

    def is_bluetooth_enabled(self):
        output = self.get_bluetooth_status()

        return (
            "enabled: true" in output
            and "state: ON" in output
        )
