# code voor gedetecteerde personen
class Person:

    def __init__(self, person_id):
        self.person_id = person_id
        self.huidige_zone = None
        self.vorige_zone = None
        self.laatste_detectie = None
        self.bewegingen = []

    def update_location(self, zone, timestamp):
        self.vorige_zone = self.huidige_zone
        self.huidige_zone = zone
        self.laatste_detectie = timestamp

        self.bewegingen.append({
            "zone": zone,
            "timestamp": timestamp
        })

    def status(self):
        if self.huidige_zone is None:
            return "geen locatie"

        return f"aanwezig in {self.huidige_zone}"

    def laatste_beweging(self):
        if not self.bewegingen:
            return None

        return self.bewegingen[-1]