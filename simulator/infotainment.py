class InfotainmentSystem:

    def __init__(self):
        self.power = "OFF"
        self.bluetooth = "DISABLED"
        self.media = "STOPPED"

    def start_system(self):
        self.power = "ON"

    def enable_bluetooth(self):
        if self.power != "ON":
            raise RuntimeError("System must be ON")
        self.bluetooth = "ENABLED"

    def play_media(self):
        if self.power != "ON":
            raise RuntimeError("System must be ON")
        self.media = "PLAYING"
