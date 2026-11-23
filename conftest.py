import pytest
from unittest.mock import MagicMock
from simulator.infotainment import InfotainmentSystem


@pytest.fixture
def infotainment():
    system = InfotainmentSystem()
    system.start_system()
    return system

@pytest.fixture
def mock_driver():
    """Reusable mock Appium driver for POM unit tests."""
    return MagicMock()