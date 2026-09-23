# code voor de verschillende contexten
from datetime import datetime


class Context:

    def __init__(self):
        self.huidige_zone = None
        self.vorige_zone = None
        self.tijdstip = None
        self.nacht = False

    def update(self, persoon):
        self.huidige_zone = persoon.huidige_zone
        self.vorige_zone = persoon.vorige_zone
        self.tijdstip = persoon.laatste_detectie

        self.bepaal_dag_nacht()

    def bepaal_dag_nacht(self):

        tijd = datetime.fromisoformat(
            self.tijdstip
        )

        uur = tijd.hour

        self.nacht = (
            uur >= 22
            or uur < 7
        )

    def bewegend(self):

        return (
            self.vorige_zone is not None
            and self.huidige_zone != self.vorige_zone
        )