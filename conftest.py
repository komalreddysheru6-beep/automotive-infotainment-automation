import pytest
from simulator.infotainment import InfotainmentSystem


@pytest.fixture
def infotainment():
    system = InfotainmentSystem()
    system.start_system()
    return system
