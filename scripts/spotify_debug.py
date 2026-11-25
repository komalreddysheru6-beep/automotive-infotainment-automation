import os

from pathlib import Path
import xml.etree.ElementTree as ET

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait


def test_spotify_debug():

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = os.environ["ANDROID_UDID"]
    options.set_capability("appium:noReset", True)

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    try:

        driver.update_settings({
            "waitForIdleTimeout": 0
        })

        driver.activate_app("com.spotify.music")

        WebDriverWait(driver, 15).until(
            lambda d: d.current_package == "com.spotify.music"
        )

        print("\nCurrent package:", driver.current_package)
        print("Current activity:", driver.current_activity)
        print("Device locked:", driver.is_locked())

        folder = Path("reports")
        folder.mkdir(exist_ok=True)

        driver.save_screenshot(
            str(folder / "spotify_debug.png")
        )

        xml = driver.page_source

        (folder / "spotify_debug.xml").write_text(
            xml, encoding="utf-8"
        )

        root = ET.fromstring(xml)

        spotify_nodes = 0

        for node in root.iter():

            rid = node.get("resource-id", "")
            desc = node.get("content-desc", "")
            text = node.get("text", "")
            package = node.get("package", "")

            if package == "com.spotify.music":
                spotify_nodes += 1

                if rid or desc or text:
                    print(
                        f"ID: {rid} | "
                        f"DESC: {desc} | "
                        f"TEXT: {text}"
                    )

        print("Spotify UI nodes:", spotify_nodes)

        assert not driver.is_locked(), "Device is locked"
        assert spotify_nodes > 0, "Spotify UI not detected"

    finally:
        driver.quit()
