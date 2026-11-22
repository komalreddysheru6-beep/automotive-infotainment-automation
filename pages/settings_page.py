
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SettingsPage(BasePage):
    """Page Object for infotainment settings."""

    WIFI_TOGGLE = (
        AppiumBy.ACCESSIBILITY_ID,
        "WiFi Toggle"
    )

    DISPLAY_SETTINGS = (
        AppiumBy.ACCESSIBILITY_ID,
        "Display Settings"
    )

    SOUND_SETTINGS = (
        AppiumBy.ACCESSIBILITY_ID,
        "Sound Settings"
    )

    BRIGHTNESS_SLIDER = (
        AppiumBy.ACCESSIBILITY_ID,
        "Brightness"
    )

    def toggle_wifi(self):
        self.click(self.WIFI_TOGGLE)

    def open_display_settings(self):
        self.click(self.DISPLAY_SETTINGS)

    def open_sound_settings(self):
        self.click(self.SOUND_SETTINGS)

    def set_brightness(self, value):
        """Set brightness slider position (0 to 100)."""
        if not 0 <= value <= 100:
            raise ValueError(
                "Brightness must be between 0 and 100"
            )

        slider = self.wait.until(
            lambda driver: driver.find_element(
                *self.BRIGHTNESS_SLIDER
            )
        )

        # Placeholder until a real slider is inspected.
        # No brightness adjustment is performed yet.
        raise NotImplementedError(
            "Brightness slider interaction is not implemented"
        )
