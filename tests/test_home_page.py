
from unittest.mock import MagicMock, patch

from pages.home_page import HomePage


def test_open_media():
    mock_driver = MagicMock()

    with patch.object(HomePage, "click") as mock_click:
        home_page = HomePage(mock_driver)

        home_page.open_media()

        mock_click.assert_called_once_with(
            HomePage.MEDIA_BUTTON
        )
