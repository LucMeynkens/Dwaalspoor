import network
import time
import json
from machine import Pin
import neopixel
from umqtt.simple import MQTTClient


# =========================
# INSTELLINGEN
# =========================

WIFI_SSID = "SSid_van_het_netwerk"
WIFI_PASSWORD = "paswoord"

MQTT_BROKER = "IP_adres_van_de_MQTT_broker"
MQTT_PORT = 1883

DEVICE_ID = "actuator01"

MQTT_TOPIC = b"dwaalspoor/output/actuator01/led"


# =========================
# RGB-LED
# =========================

rgb = neopixel.NeoPixel(Pin(48), 1)


def led_off():
    rgb[0] = (0, 0, 0)
    rgb.write()


def led_green():
    rgb[0] = (0, 255, 0)
    rgb.write()


# LED bij opstarten uit
led_off()


# =========================
# WIFI
# =========================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Verbinden met WiFi...")

wifi.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi.isconnected():
    time.sleep(0.5)

print("WiFi verbonden")
print("IP-adres:", wifi.ifconfig()[0])


# =========================
# MQTT CALLBACK
# =========================

def mqtt_callback(topic, msg):

    print()
    print("MQTT bericht ontvangen:")
    print(msg)

    try:
        data = json.loads(msg)
        command = data.get("command")

        if command == "led_on":

            led_green()
            print("RGB LED GROEN")

        elif command == "led_off":

            led_off()
            print("RGB LED UIT")

        else:

            print("Onbekend commando:", command)

    except Exception as e:

        print("Fout bij verwerken MQTT-bericht:")
        print(e)


# =========================
# MQTT
# =========================

print("Verbinden met MQTT broker...")

client = MQTTClient(
    DEVICE_ID,
    MQTT_BROKER,
    port=MQTT_PORT
)

client.set_callback(mqtt_callback)

client.connect()

print("MQTT verbonden")

client.subscribe(MQTT_TOPIC)

print("Geabonneerd op:")
print(MQTT_TOPIC)

print("Actuator01 klaar")


# =========================
# HOOFDLUS
# =========================

while True:

    client.check_msg()

    time.sleep(0.1)


# om de led te testen zonder MQTT
'''    
from machine import Pin
import neopixel
import time

rgb = neopixel.NeoPixel(Pin(48), 1)

while True:

    # rood
    rgb[0] = (255, 0, 0)
    rgb.write()
    print("ROOD")
    time.sleep(1)

    # groen
    rgb[0] = (0, 255, 0)
    rgb.write()
    print("GROEN")
    time.sleep(1)

    # blauw
    rgb[0] = (0, 0, 255)
    rgb.write()
    print("BLAUW")
    time.sleep(1)

    # uit
    rgb[0] = (0, 0, 0)
    rgb.write()
    print("UIT")
    time.sleep(1)'''