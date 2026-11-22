
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the infotainment home screen."""

    MEDIA_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Media"
    )

    NAVIGATION_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Navigation"
    )

    BLUETOOTH_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Bluetooth"
    )

    SETTINGS_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Settings"
    )

    def open_media(self):
        self.click(self.MEDIA_BUTTON)

    def open_navigation(self):
        self.click(self.NAVIGATION_BUTTON)

    def open_bluetooth(self):
        self.click(self.BLUETOOTH_BUTTON)

    def open_settings(self):
        self.click(self.SETTINGS_BUTTON)
