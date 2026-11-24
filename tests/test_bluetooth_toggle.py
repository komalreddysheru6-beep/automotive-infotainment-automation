
import subprocess
import time

DEVICE_ID = "R52Y705H82J"


def adb_command(*args):
    result = subprocess.run(
        ["adb", "-s", DEVICE_ID, "shell", *args],
        capture_output=True,
        text=True,
        check=True,
        timeout=15
    )
    return result.stdout.strip()


def get_bluetooth_status():
    output = adb_command("dumpsys", "bluetooth_manager")

    for line in output.splitlines():
        line = line.strip()

        if line == "enabled: true":
            return True

        if line == "enabled: false":
            return False

    raise RuntimeError("Unable to detect Bluetooth status")


def wait_for_bluetooth(expected, timeout=20):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:

        if get_bluetooth_status() == expected:
            return True

        time.sleep(1)

    return False


def test_bluetooth_toggle():

    original_state = get_bluetooth_status()

    print("\nOriginal Bluetooth state:", original_state)

    try:
        # Disable Bluetooth
        adb_command("svc", "bluetooth", "disable")

        assert wait_for_bluetooth(False), \
            "Bluetooth failed to disable"

        print("Bluetooth OFF verified")

        # Enable Bluetooth
        adb_command("svc", "bluetooth", "enable")

        assert wait_for_bluetooth(True), \
            "Bluetooth failed to enable"

        print("Bluetooth ON verified")

    finally:
        # Restore original Bluetooth state
        action = "enable" if original_state else "disable"

        adb_command("svc", "bluetooth", action)

        assert wait_for_bluetooth(original_state), \
            "Failed to restore original Bluetooth state"

        print("Original Bluetooth state restored")

    print("Bluetooth toggle test PASSED!")
