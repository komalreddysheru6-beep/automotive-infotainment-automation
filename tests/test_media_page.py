
from unittest.mock import patch
from pages.media_page import MediaPage


def test_play_music(mock_driver):
    page = MediaPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.play_music()

    mock_click.assert_called_once_with(
        MediaPage.PLAY_BUTTON
    )


def test_pause_music(mock_driver):
    page = MediaPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.pause_music()

    mock_click.assert_called_once_with(
        MediaPage.PAUSE_BUTTON
    )


def test_next_track(mock_driver):
    page = MediaPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.next_track()

    mock_click.assert_called_once_with(
        MediaPage.NEXT_TRACK_BUTTON
    )


def test_previous_track(mock_driver):
    page = MediaPage(mock_driver)

    with patch.object(page, "click") as mock_click:
        page.previous_track()

    mock_click.assert_called_once_with(
        MediaPage.PREVIOUS_TRACK_BUTTON
    )
