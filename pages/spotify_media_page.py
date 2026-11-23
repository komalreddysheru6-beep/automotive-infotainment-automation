
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SpotifyMediaPage:
    """Page Object for Spotify's Android music player."""

    PLAY_PAUSE = (
        By.ID,
        "com.spotify.music:id/nowplaying_elements_playpause_button"
    )

    NEXT = (
        By.XPATH,
        '//*[@content-desc="Next"]'
    )

    PREVIOUS = (
        By.XPATH,
        '//*[@content-desc="Previous"]'
    )

    PLAYER = (
        By.ID,
        "com.spotify.music:id/now_playing_container")

    TRACK_TITLE = (
            By.ID,
            "com.spotify.music:id/track_info_view_title"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def is_player_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.PLAYER)
        ).is_displayed()

    def get_playback_state(self):
        """Return the Play/Pause button's accessibility label."""
        button = self.wait.until(
            EC.presence_of_element_located(self.PLAY_PAUSE)
        )
        return button.get_attribute("content-desc")

    def toggle_play_pause(self):
        self.wait.until(
            EC.element_to_be_clickable(self.PLAY_PAUSE)
        ).click()

    def next_track(self):
        self.wait.until(
            EC.element_to_be_clickable(self.NEXT)
        ).click()

    def previous_track(self):
        self.wait.until(
            EC.element_to_be_clickable(self.PREVIOUS)
        ).click()


    def get_track_title(self):
        """Return the currently displayed Spotify song title."""
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.TRACK_TITLE
            )
        )
        return element.text.strip()
