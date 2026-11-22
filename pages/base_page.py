
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Common methods for Android infotainment page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        """Wait for an element and click it."""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        """Clear an input field and enter text."""
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return the visible text of an element."""
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def is_displayed(self, locator):
        """Check whether an element is visible."""
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.is_displayed()
