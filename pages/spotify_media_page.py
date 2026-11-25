
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SpotifyMediaPage:
    """Page Object for Spotify's Android music player."""

    PACKAGE = "com.spotify.music"

    MINI_PLAYER = (
        By.ID,
        "com.spotify.music:id/now_playing_bar_layout"
    )

    PLAYER = (
        By.ID,
        "com.spotify.music:id/now_playing_container"
    )

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

    TRACK_TITLE = (
        By.ID,
        "com.spotify.music:id/track_info_view_title"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def launch(self):

        self.driver.activate_app(self.PACKAGE)

        self.wait.until(
            lambda d: d.current_package == self.PACKAGE
        )

        print("Spotify launched successfully")

    def open_player(self):

        self.launch()

        if self.driver.is_locked():
            raise AssertionError(
                "Unlock the tablet before running Spotify tests"
            )

        self.wait.until(
            lambda d: any(
                element.is_displayed()
                for locator in [self.PLAYER, self.MINI_PLAYER]
                for element in d.find_elements(*locator)
            ),
            message="Neither full player nor mini-player found"
        )

        players = self.driver.find_elements(*self.PLAYER)

        if any(element.is_displayed() for element in players):

            print("Full-screen player already open")

        else:

            mini_player = self.wait.until(
                EC.element_to_be_clickable(self.MINI_PLAYER)
            )

            mini_player.click()

            print("Mini-player clicked")

        self.wait.until(
            EC.visibility_of_element_located(self.PLAYER),
            message="Full-screen Spotify player not visible"
        )

        print("Full-screen player verified")

    def is_player_displayed(self):

        self.open_player()

        return self.driver.find_element(
            *self.PLAYER
        ).is_displayed()

    def get_playback_state(self):

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

        element = self.wait.until(
            EC.visibility_of_element_located(self.TRACK_TITLE)
        )

        return element.text.strip()
