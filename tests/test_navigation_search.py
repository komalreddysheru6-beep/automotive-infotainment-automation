import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.google_maps_page import GoogleMapsPage


def test_navigation_search():

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)

    driver = None
    destination = "Charminar Hyderabad"

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        maps = GoogleMapsPage(driver)
        maps.launch()

        assert maps.is_map_displayed()
        print("\nGoogle Maps displayed successfully")

        assert maps.is_search_box_displayed()
        print("Search box verified")

        maps.open_search()

        search_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "android.widget.EditText")
            )
        )

        search_field.clear()
        search_field.send_keys(destination)

        assert destination.lower() in search_field.text.lower()

        print("Destination entered:", destination)

        driver.press_keycode(66)

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[contains(@text, "Charminar")]'
                    '[@class!="android.widget.EditText"]'
                )
            )
        )

        print("Destination-related result displayed")
        print("Navigation search test PASSED!")

    finally:
        if driver is not None:
            driver.quit()
