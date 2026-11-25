import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

from pages.spotify_media_page import SpotifyMediaPage


def test_spotify_next_track_title():
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

        # Read the current song title
        before_title = media_page.get_track_title()
        print("Before Next:", before_title)

        assert before_title, "Current song title is empty"

        # Click Next
        media_page.next_track()

        # Wait until the song title changes
        WebDriverWait(driver, 20).until(
            lambda d: (
                media_page.get_track_title() != before_title
            )
        )

        after_title = media_page.get_track_title()
        print("After Next:", after_title)

        assert after_title != before_title

        print("Spotify Next Track verification PASSED!")

    finally:
        if driver is not None:
            driver.quit()
