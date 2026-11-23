
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

from pages.spotify_media_page import SpotifyMediaPage


def test_spotify_previous_track():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "R52Y705H82J"
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

        # Read current song
        original_title = media_page.get_track_title()
        print("Original song:", original_title)

        # Move to next song
        media_page.next_track()

        WebDriverWait(driver, 20).until(
            lambda d: (
                media_page.get_track_title() != original_title
            )
        )

        next_title = media_page.get_track_title()
        print("Next song:", next_title)

        # Return to previous song
        media_page.previous_track()

        WebDriverWait(driver, 20).until(
            lambda d: (
                media_page.get_track_title() == original_title
            )
        )

        restored_title = media_page.get_track_title()
        print("After Previous:", restored_title)

        assert restored_title == original_title

        print("Spotify Previous Track automation PASSED!")

    finally:
        if driver is not None:
            driver.quit()
