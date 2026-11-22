
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class BluetoothPage(BasePage):
    """Page Object for infotainment Bluetooth controls."""

    BLUETOOTH_TOGGLE = (
        AppiumBy.ACCESSIBILITY_ID,
        "Bluetooth Toggle"
    )

    SEARCH_DEVICES_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Search Devices"
    )

    CONNECT_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Connect"
    )

    DISCONNECT_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Disconnect"
    )

    def toggle_bluetooth(self):
        self.click(self.BLUETOOTH_TOGGLE)

    def search_devices(self):
        self.click(self.SEARCH_DEVICES_BUTTON)

    def connect_device(self):
        self.click(self.CONNECT_BUTTON)

    def disconnect_device(self):
        self.click(self.DISCONNECT_BUTTON)
