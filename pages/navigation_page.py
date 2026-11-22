
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class NavigationPage(BasePage):
    """Page Object for infotainment navigation."""

    SEARCH_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Search"
    )

    DESTINATION_INPUT = (
        AppiumBy.ACCESSIBILITY_ID,
        "Destination"
    )

    START_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Start Navigation"
    )

    STOP_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Stop Navigation"
    )

    def open_search(self):
        self.click(self.SEARCH_BUTTON)

    def enter_destination(self, destination):
        self.enter_text(
            self.DESTINATION_INPUT,
            destination
        )

    def start_navigation(self):
        self.click(self.START_BUTTON)

    def stop_navigation(self):
        self.click(self.STOP_BUTTON)
