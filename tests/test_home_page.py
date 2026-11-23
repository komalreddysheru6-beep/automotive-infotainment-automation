
from unittest.mock import patch
from pages.home_page import HomePage


def test_open_media(mock_driver):
    page = HomePage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.open_media()

    mock_click.assert_called_once_with(
        HomePage.MEDIA_BUTTON
    )


def test_open_navigation(mock_driver):
    page = HomePage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.open_navigation()

    mock_click.assert_called_once_with(
        HomePage.NAVIGATION_BUTTON
    )


def test_open_bluetooth(mock_driver):
    page = HomePage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.open_bluetooth()

    mock_click.assert_called_once_with(
        HomePage.BLUETOOTH_BUTTON
    )


def test_open_settings(mock_driver):
    page = HomePage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.open_settings()

    mock_click.assert_called_once_with(
        HomePage.SETTINGS_BUTTON
    )