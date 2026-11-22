def test_system_is_on(infotainment):
    assert infotainment.power == "ON"


def test_bluetooth_connection(infotainment):
    infotainment.enable_bluetooth()
    assert infotainment.bluetooth == "ENABLED"


def test_media_playback(infotainment):
    infotainment.play_media()
    assert infotainment.media == "PLAYING"
