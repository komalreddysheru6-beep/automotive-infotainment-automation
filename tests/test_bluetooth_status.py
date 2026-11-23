
import subprocess


DEVICE_ID = "R52Y705H82J"


def test_bluetooth_enabled():
    result = subprocess.run(
        [
            "adb",
            "-s",
            DEVICE_ID,
            "shell",
            "dumpsys",
            "bluetooth_manager"
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=15
    )

    output = result.stdout

    assert "enabled: true" in output
    assert "state: ON" in output

    print("Bluetooth adapter is enabled!")
    print("Bluetooth state: ON")
    print("Automotive Bluetooth status test PASSED!")
