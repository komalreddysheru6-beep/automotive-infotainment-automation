
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SamsungPhonePage:

    PACKAGE = "com.samsung.android.dialer"
    PREFIX = PACKAGE + ":id/"

    DIGITS = (By.ID, PREFIX + "digits")
    KEYPAD = (By.ID, PREFIX + "keypad_view")
    CALL_BUTTON = (By.ID, PREFIX + "dialButton")

    NUMBER_KEYS = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine"
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def launch(self):

        self.driver.activate_app(self.PACKAGE)

        self.wait.until(
            lambda d: d.current_package == self.PACKAGE
        )

    def is_keypad_visible(self):

        return self.wait.until(
            EC.visibility_of_element_located(self.KEYPAD)
        ).is_displayed()

    def verify_number_keys(self):

        for number, name in self.NUMBER_KEYS.items():

            element = self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, self.PREFIX + name)
                )
            )

            assert element.is_enabled()

            print(f"Key {number}: Available")

        return True

    def enter_number(self, number):

        for digit in number:

            locator = (
                By.ID,
                self.PREFIX + self.NUMBER_KEYS[digit]
            )

            self.wait.until(
                EC.element_to_be_clickable(locator)
            ).click()

    def get_entered_number(self):

        element = self.wait.until(
            EC.visibility_of_element_located(self.DIGITS)
        )

        return re.sub(r"\D", "", element.text or "")

    def delete_digit(self):

        self.driver.press_keycode(67)

    def clear_number(self):

        for _ in range(30):

            if not self.get_entered_number():
                return

            self.delete_digit()

        assert self.get_entered_number() == ""

    def is_call_button_visible(self):

        return self.wait.until(
            EC.visibility_of_element_located(
                self.CALL_BUTTON
            )
        ).is_displayed()

    def is_call_button_enabled(self):

        return self.driver.find_element(
            *self.CALL_BUTTON
        ).is_enabled()
