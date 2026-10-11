```python
import json
from datetime import datetime

import paho.mqtt.client as mqtt


# ==========================================
# DWAALSPOOR MQTT-INSTELLINGEN
# ==========================================

# Vervang dit door het actuele IP-adres
# van de Raspberry Pi waarop Mosquitto draait.
MQTT_BROKER = "192.168.0.200"
MQTT_PORT = 1883

MQTT_CLIENT_ID = "dwaalspoor_core_test"

# Berichten van sensoren naar de Core
SENSOR_TOPIC = "dwaalspoor/input/sensor01/event"

# Commando's van de Core naar de actuator
ACTUATOR_TOPIC = "dwaalspoor/output/actuator01/led"

# Berichten van de Core naar de AI-assistant
AI_TOPIC = "dwaalspoor/output/ai01/message"


# ==========================================
# VERBINDING MET MQTT
# ==========================================

def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print()
        print("MQTT verbonden met DwaalSpoor-broker.")

        client.subscribe(SENSOR_TOPIC)

        print("Geabonneerd op:")
        print(SENSOR_TOPIC)

        print()
        print("DWAALSPOOR CORE TEST IS GESTART")
        print("Wachten op sensorberichten...")

    else:
        print("MQTT-verbinding mislukt:", reason_code)


# ==========================================
# BERICHTEN VERWERKEN
# ==========================================

def on_message(client, userdata, msg):

    ontvangen_tijd = datetime.now().strftime("%H:%M:%S")
    bericht = msg.payload.decode("utf-8", errors="replace")

    print()
    print("=" * 55)
    print("DWAALSPOOR CORE |", ontvangen_tijd)
    print("=" * 55)

    print("Topic:", msg.topic)
    print("Ontvangen bericht:", bericht)

    try:
        data = json.loads(bericht)
        event = data.get("event")

        # --------------------------------------
        # KNOP INGEDRUKT
        # --------------------------------------

        if event == "button_pressed":

            print("CORE BESLISSING: LED AAN")

            actuator_bericht = {
                "command": "led_on"
            }

            client.publish(
                ACTUATOR_TOPIC,
                json.dumps(actuator_bericht)
            )

            print("Commando naar actuator verstuurd.")

            # Bericht naar AI-assistant
            ai_bericht = {
                "action": "message",
                "message": (
                    "Er is een sensoractiviteit gedetecteerd. "
                    "De knop van sensor01 is ingedrukt. "
                    "De Core heeft beslist om de led van "
                    "actuator01 in te schakelen."
                ),
                "source": "dwaalspoor_core",
                "sensor": "sensor01",
                "event": event,
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

            client.publish(
                AI_TOPIC,
                json.dumps(ai_bericht, ensure_ascii=False)
            )

            print("Bericht naar AI-assistant ai01 verstuurd.")

        # --------------------------------------
        # KNOP LOSGELATEN
        # --------------------------------------

        elif event == "button_released":

            print("CORE BESLISSING: LED UIT")

            actuator_bericht = {
                "command": "led_off"
            }

            client.publish(
                ACTUATOR_TOPIC,
                json.dumps(actuator_bericht)
            )

            print("Commando naar actuator verstuurd.")

        # --------------------------------------
        # ONBEKEND SENSOR-EVENT
        # --------------------------------------

        else:
            print("Onbekend sensor-event:", event)

    except json.JSONDecodeError:
        print("Fout: het ontvangen bericht is geen geldige JSON.")

    except Exception as fout:
        print("Fout bij het verwerken van het bericht:", fout)

    print("=" * 55)


# ==========================================
# HOOFDPROGRAMMA
# ==========================================

def main():

    print("DWAALSPOOR CORE TEST")
    print("====================")

    print("Broker:", MQTT_BROKER)
    print("Poort:", MQTT_PORT)
    print("Sensor-topic:", SENSOR_TOPIC)
    print("Actuator-topic:", ACTUATOR_TOPIC)
    print("AI-topic:", AI_TOPIC)

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID,
        protocol=mqtt.MQTTv311
    )

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print()
        print("Verbinden met MQTT-broker...")

        client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            keepalive=60
        )

        client.loop_forever()

    except KeyboardInterrupt:
        print()
        print("DwaalSpoor Core wordt afgesloten.")

    except OSError as fout:
        print("Kan geen verbinding maken met MQTT-broker.")
        print("Fout:", fout)
        print("Controleer het IP-adres en de netwerkverbinding.")

    finally:
        client.disconnect()
        print("DwaalSpoor Core gestopt.")


# ==========================================
# STARTPUNT
# ==========================================

if __name__ == "__main__":
    main()
