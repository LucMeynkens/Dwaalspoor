# code voor de verschillende zones
class Zone:

    def __init__(self, naam):
        self.naam = naam
        self.device = None
        self.aanwezig = False
        self.timestamp = None

    def update_presence(self, device, aanwezig, timestamp):
        self.device = device
        self.aanwezig = aanwezig
        self.timestamp = timestamp

    def status(self):
        if self.aanwezig:
            return "persoon aanwezig"

        return "vrij"