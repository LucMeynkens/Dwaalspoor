import paho.mqtt.client as mqtt


class MQTTManager:

    # ========================================================
    # DWAALSPOOR MQTT CONFIGURATIE
    # ========================================================

    BROKER = "192.168.1.50"
    PORT = 1883

    # ========================================================
    # INITIALISATIE
    # ========================================================

    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.callbacks = []

        self.client.on_message = self._on_message

    # ========================================================
    # VERBINDEN
    # ========================================================

    def connect(self):

        print(
            f"Verbinden met MQTT-broker "
            f"{self.BROKER}:{self.PORT}"
        )

        self.client.connect(
            self.BROKER,
            self.PORT
        )

        print("MQTT verbonden.")

    # ========================================================
    # BERICHT PUBLICEREN
    # ========================================================

    def publish(self, topic, message):

        print(f"MQTT → {topic}")

        self.client.publish(
            topic,
            message
        )

    # ========================================================
    # ABONNEREN
    # ========================================================

    def subscribe(self, topic, callback):

        print(f"MQTT ← {topic}")

        self.client.subscribe(topic)

        self.callbacks.append(
            (topic, callback)
        )

    # ========================================================
    # BERICHT ONTVANGEN
    # ========================================================

    def _on_message(
        self,
        client,
        userdata,
        message
    ):

        for topic, callback in self.callbacks:

            if mqtt.topic_matches_sub(
                topic,
                message.topic
            ):

                callback(
                    client,
                    userdata,
                    message
                )

    # ========================================================
    # MQTT-LUS
    # ========================================================

    def loop_forever(self):

        print("MQTT-lus gestart.")

        self.client.loop_forever()
