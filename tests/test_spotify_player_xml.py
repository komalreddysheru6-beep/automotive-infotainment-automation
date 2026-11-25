import os

from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_spotify_player_xml():
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

        # Allow UI hierarchy extraction without waiting
        # for Spotify's animated interface to become idle.
        driver.update_settings({
            "waitForIdleTimeout": 0
        })

        xml = driver.page_source

        output = Path("reports/spotify_player.xml")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(xml, encoding="utf-8")

        assert xml.strip()
        print("Spotify player XML saved successfully!")

    finally:
        if driver is not None:
            driver.quit()
