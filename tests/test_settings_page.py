
import pytest
from unittest.mock import MagicMock, patch

from pages.settings_page import SettingsPage


def test_toggle_wifi():
    page = SettingsPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.toggle_wifi()

    mock_click.assert_called_once_with(
        SettingsPage.WIFI_TOGGLE
    )


def test_open_display_settings():
    page = SettingsPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.open_display_settings()

    mock_click.assert_called_once_with(
        SettingsPage.DISPLAY_SETTINGS
    )


def test_open_sound_settings():
    page = SettingsPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.open_sound_settings()

    mock_click.assert_called_once_with(
        SettingsPage.SOUND_SETTINGS
    )


def test_valid_brightness_not_implemented():
    page = SettingsPage(MagicMock())

    with pytest.raises(NotImplementedError):
        page.set_brightness(50)


def test_invalid_brightness():
    page = SettingsPage(MagicMock())

    with pytest.raises(ValueError):
        page.set_brightness(150)
