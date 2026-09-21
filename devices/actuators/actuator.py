import json

from communication.topics import actuator_light


class Actuator:

    def __init__(
        self,
        device_id,
        mqtt
    ):

        self.device_id = device_id
        self.mqtt = mqtt

    # ========================================================
    # STARTEN
    # ========================================================

    def start(self):

        topic = actuator_light(
            self.device_id
        )

        self.mqtt.subscribe(
            topic,
            self.on_message
        )

    # ========================================================
    # BERICHT ONTVANGEN
    # ========================================================

    def on_message(
        self,
        client,
        userdata,
        message
    ):

        try:

            data = json.loads(
                message.payload.decode()
            )

            print()
            print("=== ACTUATOR ===")
            print("Bericht ontvangen:")
            print(data)

            action = data.get("action")

            if action == "on":

                self.turn_on()

            elif action == "off":

                self.turn_off()

            else:

                print(
                    f"Onbekende actie: {action}"
                )

        except json.JSONDecodeError:

            print(
                "Fout: ontvangen bericht "
                "is geen geldige JSON."
            )

    # ========================================================
    # LICHT AAN
    # ========================================================

    def turn_on(self):

        print(
            f"💡 {self.device_id}: LICHT AAN"
        )

    # ========================================================
    # LICHT UIT
    # ========================================================

    def turn_off(self):

        print(
            f"💡 {self.device_id}: LICHT UIT"
        )
