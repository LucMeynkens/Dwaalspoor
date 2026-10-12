import json
from datetime import datetime

import paho.mqtt.client as mqtt


# ==========================================
# DWAALSPOOR MQTT-INSTELLINGEN
# ==========================================

# Vervang dit door het actuele IP-adres
# van de Raspberry Pi waarop Mosquitto draait.
MQTT_BROKER = "IP_adres_van_de_MQTT_broker"
MQTT_PORT = 1883

MQTT_CLIENT_ID = "ai01_terminal"

# Berichten van DwaalSpoor Core naar de AI-assistant
INPUT_TOPIC = "dwaalspoor/output/ai01/message"


# ==========================================
# VERBINDING MET MQTT
# ==========================================

def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print()
        print("MQTT verbonden met DwaalSpoor-broker.")

        client.subscribe(INPUT_TOPIC)

        print("Geabonneerd op:")
        print(INPUT_TOPIC)

        print()
        print("AI-assistant ai01 is gestart.")
        print("Wachten op berichten van DwaalSpoor Core...")

    else:
        print("MQTT-verbinding mislukt:", reason_code)


# ==========================================
# BERICHT ONTVANGEN
# ==========================================

def on_message(client, userdata, msg):

    ontvangen_tijd = datetime.now().strftime("%H:%M:%S")

    bericht = msg.payload.decode(
        "utf-8",
        errors="replace"
    )

    print()
    print("=" * 55)
    print("DWAALSPOOR AI-ASSISTANT |", ontvangen_tijd)
    print("=" * 55)

    print("Topic:", msg.topic)
    print("Ontvangen bericht:", bericht)

    try:
        data = json.loads(bericht)

        actie = data.get("action", "message")
        boodschap = data.get("message", bericht)

        print("Actie:", actie)
        print("Boodschap voor de assistant:", boodschap)

    except json.JSONDecodeError:
        print("Het bericht bevat geen geldige JSON.")

    print("=" * 55)


# ==========================================
# HOOFDPROGRAMMA
# ==========================================

def main():

    print("DWAALSPOOR AI-ASSISTANT")
    print("=======================")

    print("Broker:", MQTT_BROKER)
    print("Poort:", MQTT_PORT)
    print("Topic:", INPUT_TOPIC)

    # MQTT-client aanmaken
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID,
        protocol=mqtt.MQTTv311
    )

    # Functies koppelen aan MQTT-gebeurtenissen
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

        # Berichten blijven ontvangen
        client.loop_forever()

    except KeyboardInterrupt:
        print()
        print("AI-assistant wordt afgesloten.")

    except OSError as fout:
        print("Kan geen verbinding maken met MQTT-broker.")
        print("Fout:", fout)
        print("Controleer het IP-adres en de netwerkverbinding.")

    finally:
        client.disconnect()
        print("AI-assistant gestopt.")


# ==========================================
# STARTPUNT
# ==========================================

if __name__ == "__main__":
    main()