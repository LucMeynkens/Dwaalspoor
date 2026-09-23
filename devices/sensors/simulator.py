import time

from communication.mqtt_manager import MQTTManager
from devices.sensors.sensor import Sensor


mqtt = MQTTManager()

mqtt.connect()


sensor01 = Sensor(
    device_id="sensor01",
    zone="gang_01",
    mqtt=mqtt
)

sensor02 = Sensor(
    device_id="sensor02",
    zone="gang_02",
    mqtt=mqtt
)


print()
print("================================")
print("DWAALSPOOR SENSOR SIMULATOR")
print("================================")


# ------------------------------------------------------------
# SIMULATIETIJD
# ------------------------------------------------------------

simulatie_tijd = "23:30:00"

print()
print(f"Simulatietijd: {simulatie_tijd}")


# ------------------------------------------------------------
# PERSOON KOMT IN GANG 01
# ------------------------------------------------------------

print()
print("Persoon gedetecteerd in gang_01")

sensor01.detect_presence(
    True,
    simulatie_tijd
)


time.sleep(3)


# ------------------------------------------------------------
# PERSOON GAAT NAAR GANG 02
# ------------------------------------------------------------

print()
print("Persoon beweegt naar gang_02")

sensor02.detect_presence(
    True,
    simulatie_tijd
)


print()
print("Simulator beëindigd.")