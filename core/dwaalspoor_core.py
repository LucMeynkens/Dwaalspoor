import json
from datetime import datetime

from communication.topics import (
    ALL_SENSOR_PRESENCE,
    ALL_SENSOR_POSITION,
    actuator_light
)

from models.zone import Zone
from models.person import Person
from models.context import Context

from core.decision_engine import DecisionEngine


class DwaalSpoorCore:

    def __init__(self, mqtt):

        self.mqtt = mqtt

        # ----------------------------------------------------
        # SYSTEEMOBJECTEN
        # ----------------------------------------------------

        self.zones = {}
        self.personen = {}

        self.context = Context()

        self.decision_engine = DecisionEngine()

        self._presence_callback_registered = False
        self._position_callback_registered = False

    # ========================================================
    # STARTEN
    # ========================================================

    def start(self):

        print("DwaalSpoor Core gestart.")

        # Sensoren die aanwezigheid melden
        if not self._presence_callback_registered:
            self.mqtt.subscribe(
                ALL_SENSOR_PRESENCE,
                self.on_presence
            )
            self._presence_callback_registered = True

        # Sensoren die positie melden
        if not self._position_callback_registered:
            self.mqtt.subscribe(
                ALL_SENSOR_POSITION,
                self.on_position
            )
            self._position_callback_registered = True

    # ========================================================
    # AANWEZIGHEID ONTVANGEN
    # ========================================================

    def on_presence(
        self,
        client,
        userdata,
        message
    ):

        data = self._validated_mqtt_data(
            message,
            "presence"
        )

        if data is None:
            return

        print()
        print("================================")
        print("CORE - AANWEZIGHEID")
        print("================================")

        print(data)

        # ------------------------------------------------
        # DATA UIT MQTT-BERICHT HALEN
        # ------------------------------------------------

        sensor = data.get("device")
        zone_naam = data.get("zone")
        aanwezig = data.get("value")
        timestamp = data.get("timestamp")

        # ------------------------------------------------
        # ZONE AANMAKEN ALS DIE NOG NIET BESTAAT
        # ------------------------------------------------

        if zone_naam not in self.zones:

            self.zones[zone_naam] = Zone(
                zone_naam
            )

        zone = self.zones[zone_naam]

        # ------------------------------------------------
        # ZONE BIJWERKEN
        # ------------------------------------------------

        zone.update_presence(
            sensor,
            aanwezig,
            timestamp
        )

        print(
            f"Sensor      : {sensor}"
        )

        print(
            f"Zone        : {zone_naam}"
        )

        print(
            f"Aanwezig    : {aanwezig}"
        )

        print(
            f"Tijdstip    : {timestamp}"
        )

        # ------------------------------------------------
        # CONTEXT ALLEEN VERWERKEN BIJ AANWEZIGHEID
        # ------------------------------------------------

        if aanwezig is True:

            self.verwerk_context(
                zone_naam,
                timestamp
            )

    # ========================================================
    # POSITIE ONTVANGEN
    # ========================================================

    def on_position(
        self,
        client,
        userdata,
        message
    ):

        data = self._validated_mqtt_data(
            message,
            "position"
        )

        if data is None:
            return

        print()
        print("================================")
        print("CORE - POSITIE")
        print("================================")

        print(data)

        sensor = data.get("device")
        zone = data.get("zone")

        x = data.get("x")
        y = data.get("y")

        timestamp = data.get("timestamp")

        print(
            f"Sensor      : {sensor}"
        )

        print(
            f"Zone        : {zone}"
        )

        print(
            f"Positie     : x={x}, y={y}"
        )

        print(
            f"Tijdstip    : {timestamp}"
        )


    # ========================================================
    # MQTT-INPUT VALIDEREN
    # ========================================================

    @staticmethod
    def _validated_mqtt_data(message, expected_type):

        def reject_json_constant(value):
            raise ValueError(
                f"Invalid JSON constant: {value}"
            )

        try:
            data = json.loads(
                message.payload.decode(),
                parse_constant=reject_json_constant
            )
        except (ValueError, UnicodeDecodeError):
            print(
                f"Invalid MQTT {expected_type} message: invalid JSON."
            )
            return None

        if not isinstance(data, dict):
            print(
                f"Invalid MQTT {expected_type} message: expected a JSON object."
            )
            return None

        required_fields = [
            "device",
            "type",
            "zone",
            "timestamp"
        ]
        if expected_type == "presence":
            required_fields.append("value")
        else:
            required_fields.extend(("x", "y"))

        for field in required_fields:
            if field not in data:
                print(
                    f"Invalid MQTT {expected_type} message: "
                    f"missing field '{field}'."
                )
                return None

        for field in ("device", "zone"):
            if not isinstance(data[field], str) or not data[field].strip():
                print(
                    f"Invalid MQTT {expected_type} message: "
                    f"field '{field}' must be a non-empty string."
                )
                return None

        if data["type"] != expected_type:
            print(
                f"Invalid MQTT {expected_type} message: "
                f"field 'type' must be '{expected_type}'."
            )
            return None

        if expected_type == "presence":
            if type(data["value"]) is not bool:
                print(
                    "Invalid MQTT presence message: "
                    "field 'value' must be a JSON boolean."
                )
                return None
        else:
            for field in ("x", "y"):
                if isinstance(data[field], bool) or not isinstance(
                    data[field], (int, float)
                ):
                    print(
                        f"Invalid MQTT position message: "
                        f"field '{field}' must be numeric."
                    )
                    return None

        timestamp = data["timestamp"]
        if (
            not isinstance(timestamp, str)
            or not any(separator in timestamp for separator in ("T", "t", " "))
        ):
            print(
                f"Invalid MQTT {expected_type} message: "
                "field 'timestamp' must be an ISO-8601 datetime."
            )
            return None

        try:
            datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except ValueError:
            print(
                f"Invalid MQTT {expected_type} message: "
                "field 'timestamp' must be an ISO-8601 datetime."
            )
            return None

        return data

    # ========================================================
    # CONTEXT VERWERKEN
    # ========================================================

    def verwerk_context(
        self,
        zone,
        timestamp
    ):

        # ----------------------------------------------------
        # Voorlopig gebruiken we één persoon.
        # ----------------------------------------------------

        person_id = "persoon01"

        if person_id not in self.personen:

            self.personen[person_id] = Person(
                person_id
            )

        persoon = self.personen[person_id]

        # ----------------------------------------------------
        # Locatie van persoon bijwerken
        # ----------------------------------------------------

        persoon.update_location(
            zone,
            timestamp
        )

        # ----------------------------------------------------
        # Context bijwerken
        # ----------------------------------------------------

        self.context.update(
            persoon
        )

        print()
        print("=== CONTEXT ===")

        print(
            f"Vorige zone : "
            f"{self.context.vorige_zone}"
        )

        print(
            f"Huidige zone: "
            f"{self.context.huidige_zone}"
        )

        print(
            f"Nacht       : "
            f"{self.context.nacht}"
        )

        print(
            f"Beweging    : "
            f"{self.context.bewegend()}"
        )

        # ----------------------------------------------------
        # BESLISSING VRAGEN
        # ----------------------------------------------------

        actie = self.decision_engine.bepaal_actie(
            self.context
        )

        print()
        print(
            f"Beslissing: {actie}"
        )

        # ----------------------------------------------------
        # ACTIE UITVOEREN
        # ----------------------------------------------------

        self.verwerk_actie(
            actie
        )

    # ========================================================
    # ACTIE VERWERKEN
    # ========================================================

    def verwerk_actie(
        self,
        actie
    ):

        if actie == "GEEN_ACTIE":

            print(
                "Geen actie nodig."
            )

        elif actie == "OPVOLGEN":

            print(
                "Persoon wordt opgevolgd."
            )

            self.stuur_licht(
                actuator_id="actuator01",
                actie="on",
                zone=self.context.huidige_zone
            )

        else:

            print(
                f"Onbekende actie: {actie}"
            )

    # ========================================================
    # LICHT AANSTUREN
    # ========================================================

    def stuur_licht(
        self,
        actuator_id,
        actie,
        zone
    ):

        bericht = {
            "action": actie,
            "zone": zone
        }

        topic = actuator_light(
            actuator_id
        )

        self.mqtt.publish(
            topic,
            json.dumps(bericht)
        )

        print()
        print("=== ACTUATOR COMMANDO ===")

        print(
            f"Actuator: {actuator_id}"
        )

        print(
            f"Actie   : {actie}"
        )

        print(
            f"Zone    : {zone}"
        )

