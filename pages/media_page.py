
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class MediaPage(BasePage):
    """Page Object for infotainment media controls."""

    PLAY_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Play"
    )

    PAUSE_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Pause"
    )

    NEXT_TRACK_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Next"
    )

    PREVIOUS_TRACK_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Previous"
    )

    def play_music(self):
        self.click(self.PLAY_BUTTON)

    def pause_music(self):
        self.click(self.PAUSE_BUTTON)

    def next_track(self):
        self.click(self.NEXT_TRACK_BUTTON)

    def previous_track(self):
        self.click(self.PREVIOUS_TRACK_BUTTON)
