# communication/mqtt_manager.py

import paho.mqtt.client as mqtt


class MQTTManager:

    def __init__(self, broker="localhost", port=1883):

        self.broker = broker
        self.port = port

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.callbacks = []

        self.client.on_message = self._on_message

    # --------------------------------------------------------
    # Verbinden met MQTT-broker
    # --------------------------------------------------------

    def connect(self):

        print(f"Verbinden met MQTT-broker {self.broker}:{self.port}")

        self.client.connect(
            self.broker,
            self.port
        )

        print("MQTT verbonden.")

    # --------------------------------------------------------
    # Bericht publiceren
    # --------------------------------------------------------

    def publish(self, topic, message):

        print(f"MQTT → {topic}")

        self.client.publish(
            topic,
            message
        )

    # --------------------------------------------------------
    # Abonneren op een topic
    # --------------------------------------------------------

    def subscribe(self, topic, callback):

        print(f"MQTT ← {topic}")

        self.client.subscribe(topic)

        self.callbacks.append(
            (topic, callback)
        )

    # --------------------------------------------------------
    # Ontvangen MQTT-bericht verwerken
    # --------------------------------------------------------

    def _on_message(self, client, userdata, message):

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

    # --------------------------------------------------------
    # MQTT-lus starten
    # --------------------------------------------------------

    def loop_forever(self):

        print("MQTT-lus gestart.")

        self.client.loop_forever()
