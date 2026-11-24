
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleMapsPage:

    PACKAGE = "com.google.android.apps.maps"

    SEARCH_BOX = (
        By.ID,
        PACKAGE + ":id/search_omnibox_text_box"
    )

    MAP_CONTAINER = (
        By.ID,
        PACKAGE + ":id/mainmap_container"
    )

    EXPLORE_TAB = (
        By.ID,
        PACKAGE + ":id/explore_tab_strip_button"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def launch(self):

        # Stop the existing Maps session
        self.driver.terminate_app(self.PACKAGE)

        # Relaunch Google Maps
        self.driver.activate_app(self.PACKAGE)

        self.wait.until(
            lambda d: d.current_package == self.PACKAGE
        )

        # Verify the home screen search box
        self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_BOX)
        )

        print("Google Maps home screen ready")

    def is_map_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MAP_CONTAINER)
        ).is_displayed()

    def is_search_box_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_BOX)
        ).is_displayed()

    def open_search(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BOX)
        ).click()

    def is_explore_tab_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.EXPLORE_TAB)
        ).is_displayed()
