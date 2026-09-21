import json
from datetime import datetime

from communication.topics import sensor_presence


class Sensor:

    def __init__(
        self,
        device_id,
        zone,
        mqtt
    ):

        self.device_id = device_id
        self.zone = zone
        self.mqtt = mqtt

    # ========================================================
    # AANWEZIGHEID DETECTEREN
    # ========================================================

    def detect_presence(self, aanwezig):

        bericht = {
            "device": self.device_id,
            "type": "presence",
            "zone": self.zone,
            "value": aanwezig,
            "timestamp": datetime.now().isoformat()
        }

        topic = sensor_presence(
            self.device_id
        )

        self.mqtt.publish(
            topic,
            json.dumps(bericht)
        )
