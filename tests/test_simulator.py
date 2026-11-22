import pytest
from simulator.infotainment import InfotainmentSystem


@pytest.fixture
def system():
    return InfotainmentSystem()


def test_system_startup(system):
    system.start_system()
    assert system.power == "ON"


def test_bluetooth_enable(system):
    system.start_system()
    system.enable_bluetooth()
    assert system.bluetooth == "ENABLED"


def test_media_playback(system):
    system.start_system()
    system.play_media()
    assert system.media == "PLAYING"


def test_bluetooth_requires_power(system):
    with pytest.raises(RuntimeError):
        system.enable_bluetooth()
