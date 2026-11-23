
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SamsungHomePage:

    HOME_SCREEN = (
        By.ID,
        "com.sec.android.app.launcher:id/home_screen"
    )

    def __init__(self, driver):
        self.driver = driver

    def open_home(self):
        """Navigate to Android Home screen."""
        self.driver.press_keycode(3)

    def is_home_displayed(self):
        """Verify Samsung Home screen is present."""
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    self.HOME_SCREEN
                )
            )
            return True
        except Exception:
            return False
