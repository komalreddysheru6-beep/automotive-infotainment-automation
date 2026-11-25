
import os
import re
import shlex
import subprocess
from pathlib import Path
from urllib.parse import quote

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.navigation_routes_page import NavigationRoutesPage


MODES = {
    "1": ("Driving", "Driving mode"),
    "2": ("Two-wheeler", "wheeler mode"),
    "3": ("Public transport", "Public transport mode"),
    "4": ("Walking", "Walking mode")
}


def test_navigation_custom():

    if os.getenv("CUSTOM_NAVIGATION") != "1":
        pytest.skip("Interactive navigation not requested")

    print("\n========== INFOTAINMENT NAVIGATION ==========")

    destination = input("\nEnter destination: ").strip()

    while not destination:
        destination = input("Enter a valid destination: ").strip()

    device_id = os.environ["ANDROID_UDID"]
    package = "com.google.android.apps.maps"

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = device_id

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:skipDeviceInitialization", True)
    options.set_capability("appium:newCommandTimeout", 300)

    driver = None

    report_dir = Path("reports/screenshots")
    report_dir.mkdir(parents=True, exist_ok=True)

    def open_maps_uri(uri):

        command = (
            "am start -W "
            "-a android.intent.action.VIEW "
            f"-d {shlex.quote(uri)} "
            f"-p {package}"
        )

        subprocess.run(
            ["adb", "-s", device_id, "shell", command],
            check=True,
            timeout=30
        )

    try:

        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        wait = WebDriverWait(driver, 60)

        driver.terminate_app(package)

        print(f"\nSearching for: {destination}")

        encoded_destination = quote(destination, safe="")

        open_maps_uri(
            "geo:0,0?q=" + encoded_destination
        )

        wait.until(
            lambda d: d.current_package == package
        )

        directions_locator = (
            By.XPATH,
            '//*[@content-desc="Directions"]'
        )

        results_locator = (
            By.ID,
            package + ":id/search_list_layout"
        )

        mode_tabs = (
            By.ID,
            package + ":id/directions_mode_tabs"
        )

        def visible(d, locator):

            return any(
                e.is_displayed()
                for e in d.find_elements(*locator)
            )

        def detect_screen(d):

            if visible(d, mode_tabs):
                return "route"

            if visible(d, results_locator):
                return "results"

            if visible(d, directions_locator):
                return "single"

            return False

        # Detect the destination screen
        try:

            screen = WebDriverWait(
                driver, 20
            ).until(detect_screen)

        except TimeoutException:

            print("\nSearch screen not recognised.")
            print("Trying direct Directions fallback...")

            driver.save_screenshot(
                str(report_dir / "navigation_search_fallback.png")
            )

            driver.terminate_app(package)

            open_maps_uri(
                "https://www.google.com/maps/dir/?api=1"
                "&destination=" + encoded_destination
            )

            screen = wait.until(
                detect_screen,
                message="Unable to recognise destination screen"
            )

        # Handle multiple destinations
        if screen == "results":

            print("\nSearch results detected.")

            buttons = [
                e for e in driver.find_elements(
                    *directions_locator
                ) if e.is_displayed()
            ]

            print(f"Visible Directions buttons: {len(buttons)}")

            driver.save_screenshot(
                str(report_dir / "navigation_suggestions.png")
            )

            print("\nSelect the correct destination on the tablet.")
            print("Tap Directions. Do not tap Start.")

            input("\nPress Enter after opening Directions: ")

        # Handle single destination
        elif screen == "single":

            print("\nSingle destination detected.")

            wait.until(
                EC.element_to_be_clickable(
                    directions_locator
                )
            ).click()

        # Handle direct Directions screen
        elif screen == "route":

            print("\nDirections screen opened directly.")

        wait.until(
            EC.visibility_of_element_located(mode_tabs)
        )

        print("Directions screen verified")

        # Verify destination
        destination_locator = (
            By.XPATH,
            '//*[starts-with(@content-desc, "Destination,")]'
        )

        destination_element = wait.until(
            EC.visibility_of_element_located(
                destination_locator
            )
        )

        resolved_destination = destination_element.get_attribute(
            "content-desc"
        ).split(",", 1)[1].strip()

        assert resolved_destination

        print(f"\nRequested destination: {destination}")
        print(f"Resolved destination: {resolved_destination}")

        confirmation = input(
            "\nIs this the correct destination? (y/n): "
        ).strip().lower()

        assert confirmation == "y", "Destination not confirmed"

        # Transport mode selection
        print("\n========== TRANSPORT MODES ==========")

        for key, value in MODES.items():
            print(f"{key}. {value[0]}")

        choice = input("\nEnter your choice: ").strip()

        while choice not in MODES:

            print("Invalid choice.")

            choice = input(
                "Select between 1 and 4: "
            ).strip()

        mode_name, mode_description = MODES[choice]

        mode_locator = (
            By.XPATH,
            f'//*[contains(@content-desc, "{mode_description}")]'
        )

        mode_element = wait.until(
            EC.visibility_of_element_located(mode_locator)
        )

        print(f"\nSelecting {mode_name} mode...")

        if mode_element.get_attribute("selected") != "true":

            rect = mode_element.rect

            driver.execute_script(
                "mobile: clickGesture",
                {
                    "x": int(rect["x"] + rect["width"] / 2),
                    "y": int(rect["y"] + rect["height"] / 2)
                }
            )

        wait.until(
            lambda d: d.find_element(
                *mode_locator
            ).get_attribute("selected") == "true"
        )

        print("Transport mode verified")

        # Verify travel duration
        def get_route_duration(d):

            element = d.find_element(*mode_locator)

            description = element.get_attribute(
                "content-desc"
            ) or ""

            if element.get_attribute("selected") != "true":
                return False

            if re.search(
                r"\d+\s*(days?|hours?|minutes?|hrs?|mins?)\b",
                description,
                re.IGNORECASE
            ):
                return description

            return False

        route_information = wait.until(
            get_route_duration,
            message="No calculated travel duration found"
        )

        print(f"Travel information: {route_information}")

        # Dynamic alternate route selection
        navigation_routes = NavigationRoutesPage(driver)

        route_details = navigation_routes.choose_route()

        if route_details:

            route_information = wait.until(
                get_route_duration
            )

            route_status = "PASSED"

        else:

            route_status = "NOT VALIDATED"

            print(
                "No accessible route suggestions "
                "for this layout."
            )

        # Recheck destination after route selection
        final_destination = wait.until(
            EC.visibility_of_element_located(
                destination_locator
            )
        ).get_attribute("content-desc").split(",", 1)[1].strip()

        assert final_destination == resolved_destination

        # Save test evidence
        assert driver.save_screenshot(
            str(report_dir / "navigation_custom.png")
        )

        Path("reports/navigation_custom.xml").write_text(
            driver.page_source,
            encoding="utf-8"
        )

        print("\n========== TEST SUMMARY ==========")
        print(f"Requested destination: {destination}")
        print(f"Resolved destination: {resolved_destination}")
        print(f"Transport mode: {mode_name}")
        print(f"Travel information: {route_information}")

        if route_details:
            print(f"Selected route: {route_details}")

        print("Destination confirmation: PASSED")
        print("Transport mode: PASSED")
        print("Travel duration: PASSED")
        print(f"Route selection: {route_status}")
        print("Screenshot: Saved")
        print("XML evidence: Saved")
        print("CUSTOM NAVIGATION TEST PASSED!")
        print("==================================")

    except Exception:

        if driver is not None:

            driver.save_screenshot(
                str(report_dir / "navigation_custom_failure.png")
            )

            Path("reports/navigation_custom_failure.xml").write_text(
                driver.page_source,
                encoding="utf-8"
            )

        raise

    finally:

        if driver is not None:
            driver.quit()
