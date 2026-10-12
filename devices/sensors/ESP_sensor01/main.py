from machine import Pin
import network
import time
from umqtt.simple import MQTTClient


# ==========================================
# DwaalSpoor - ESP32 drukknop MQTT test
# ==========================================

WIFI_SSID = "SSid_van_het_netwerk"
WIFI_PASSWORD = "paswoord"

MQTT_BROKER = "IP_adres_van_de_MQTT_broker"
MQTT_PORT = 1883

DEVICE_ID = "sensor01"
MQTT_TOPIC = b"dwaalspoor/input/sensor01/event"

BUTTON_PIN = 4


# ------------------------------------------
# WiFi verbinden
# ------------------------------------------

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Verbinden met WiFi...")

wifi.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi.isconnected():
    time.sleep(0.5)
    print(".", end="")

print()
print("WiFi verbonden")
print("IP-adres:", wifi.ifconfig()[0])


# ------------------------------------------
# MQTT verbinden
# ------------------------------------------

print("Verbinden met MQTT broker...")

client = MQTTClient(
    DEVICE_ID,
    MQTT_BROKER,
    port=MQTT_PORT
)

client.connect()

print("MQTT verbonden")


# ------------------------------------------
# Drukknop
# ------------------------------------------

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

vorige_status = button.value()

print("DwaalSpoor sensor gestart")
print("Wachten op drukknop...")


# ------------------------------------------
# Hoofdprogramma
# ------------------------------------------

while True:

    huidige_status = button.value()

    if huidige_status != vorige_status:

        if huidige_status == 0:

            bericht = (
                '{"device":"sensor01",'
                '"event":"button_pressed"}'
            )

            client.publish(
                MQTT_TOPIC,
                bericht
            )

            print("KNOP INGEDRUKT")
            print("MQTT:", bericht)

        else:

            bericht = (
                '{"device":"sensor01",'
                '"event":"button_released"}'
            )

            client.publish(
                MQTT_TOPIC,
                bericht
            )

            print("KNOP LOSGELATEN")
            print("MQTT:", bericht)

        vorige_status = huidige_status

    time.sleep(0.02)