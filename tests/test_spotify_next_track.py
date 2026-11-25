import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

from pages.spotify_media_page import SpotifyMediaPage


def test_spotify_next_track():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]
    options.set_capability("appium:noReset", True)

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        driver.update_settings({
            "waitForIdleTimeout": 0
        })

        media_page = SpotifyMediaPage(driver)

        assert media_page.is_player_displayed()

        # Read the currently displayed track information.
        before = driver.page_source

        # Click the actual Spotify Next button.
        media_page.next_track()

        # Wait for the displayed UI hierarchy to change.
        WebDriverWait(driver, 15).until(
            lambda d: d.page_source != before
        )

        print("Spotify Next button clicked!")
        print("Player UI changed successfully!")

    finally:
        if driver is not None:
            driver.quit()
