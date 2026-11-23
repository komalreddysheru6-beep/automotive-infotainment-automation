
from unittest.mock import patch
from pages.bluetooth_page import BluetoothPage


def test_toggle_bluetooth(mock_driver):
    page = BluetoothPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.toggle_bluetooth()

    mock_click.assert_called_once_with(
        BluetoothPage.BLUETOOTH_TOGGLE
    )


def test_search_devices(mock_driver):
    page = BluetoothPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.search_devices()

    mock_click.assert_called_once_with(
        BluetoothPage.SEARCH_DEVICES_BUTTON
    )


def test_connect_device(mock_driver):
    page = BluetoothPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.connect_device()

    mock_click.assert_called_once_with(
        BluetoothPage.CONNECT_BUTTON
    )


def test_disconnect_device(mock_driver):
    page = BluetoothPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.disconnect_device()

    mock_click.assert_called_once_with(
        BluetoothPage.DISCONNECT_BUTTON
    )
