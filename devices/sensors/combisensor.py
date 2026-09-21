#                 combisensor
#                    │
#          ┌─────────┴─────────┐
#          ▼                   ▼
#      presence             position
#          │                   │
#          ▼                   ▼
#dwaalspoor/input/       dwaalspoor/input/
#combisensor/presence    combisensor/position

# Gebruik
#sensor = CombiSensor(
#    device_id="sensor01",
#    zone="gang_01",
#    mqtt=mqtt
#)
#sensor.detect_presence(True)
#
#sensor.detect_position(
#    x=3.2,
#    y=1.5
#)



#Dan ontstaan twee MQTT-berichten.

#Presence
#dwaalspoor/input/sensor01/presence
#{
#    "device": "sensor01",
#    "type": "presence",
#    "zone": "gang_01",
#    "value": true
#}
#Position
#dwaalspoor/input/sensor01/position
#{
#    "device": "sensor01",
#    "type": "position",
#    "zone": "gang_01",
#    "x": 3.2,
#    "y": 1.5
#}




import json
from datetime import datetime

from communication.topics import (
    sensor_presence,
    sensor_position
)


class CombiSensor:

    def __init__(
        self,
        device_id,
        zone,
        mqtt
    ):

        self.device_id = device_id
        self.zone = zone
        self.mqtt = mqtt

    def detect_presence(self, aanwezig):

        bericht = {
            "device": self.device_id,
            "type": "presence",
            "zone": self.zone,
            "value": aanwezig,
            "timestamp": datetime.now().isoformat()
        }

        self.mqtt.publish(
            sensor_presence(self.device_id),
            json.dumps(bericht)
        )

    def detect_position(self, x, y):

        bericht = {
            "device": self.device_id,
            "type": "position",
            "zone": self.zone,
            "x": x,
            "y": y,
            "timestamp": datetime.now().isoformat()
        }

        self.mqtt.publish(
            sensor_position(self.device_id),
            json.dumps(bericht)
        )
