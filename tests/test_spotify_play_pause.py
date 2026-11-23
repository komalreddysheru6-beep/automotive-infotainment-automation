
from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.spotify_media_page import SpotifyMediaPage


def test_spotify_play_pause():
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

        initial_state = media_page.get_playback_state()
        print("Initial playback state:", initial_state)

        assert initial_state in ("Play", "Pause")

        media_page.toggle_play_pause()

        expected_state = (
            "Play" if initial_state == "Pause" else "Pause"
        )

        from selenium.webdriver.support.ui import WebDriverWait

        WebDriverWait(driver, 10).until(
            lambda d: media_page.get_playback_state()
            == expected_state
        )

        print("Playback state changed to:", expected_state)
        print("Spotify Play/Pause automation passed!")

    finally:
        if driver is not None:
            driver.quit()
