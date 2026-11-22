
from unittest.mock import MagicMock, patch
from pages.bluetooth_page import BluetoothPage


def test_toggle_bluetooth():
    page = BluetoothPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.toggle_bluetooth()

    mock_click.assert_called_once_with(
        BluetoothPage.BLUETOOTH_TOGGLE
    )


def test_search_devices():
    page = BluetoothPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.search_devices()

    mock_click.assert_called_once_with(
        BluetoothPage.SEARCH_DEVICES_BUTTON
    )


def test_connect_device():
    page = BluetoothPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.connect_device()

    mock_click.assert_called_once_with(
        BluetoothPage.CONNECT_BUTTON
    )


def test_disconnect_device():
    page = BluetoothPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.disconnect_device()

    mock_click.assert_called_once_with(
        BluetoothPage.DISCONNECT_BUTTON
    )
