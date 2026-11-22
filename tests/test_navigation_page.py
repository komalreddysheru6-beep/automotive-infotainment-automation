
from unittest.mock import MagicMock, patch
from pages.navigation_page import NavigationPage


def test_open_search():
    page = NavigationPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.open_search()

    mock_click.assert_called_once_with(
        NavigationPage.SEARCH_BUTTON
    )


def test_enter_destination():
    page = NavigationPage(MagicMock())

    with patch.object(page, "enter_text") as mock_enter:
        page.enter_destination("Hyderabad")

    mock_enter.assert_called_once_with(
        NavigationPage.DESTINATION_INPUT,
        "Hyderabad"
    )


def test_start_navigation():
    page = NavigationPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.start_navigation()

    mock_click.assert_called_once_with(
        NavigationPage.START_BUTTON
    )


def test_stop_navigation():
    page = NavigationPage(MagicMock())

    with patch.object(page, "click") as mock_click:
        page.stop_navigation()

    mock_click.assert_called_once_with(
        NavigationPage.STOP_BUTTON
    )
