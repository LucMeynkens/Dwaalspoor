# code voor een gesimuleerde sensor

from communication.mqtt_manager import MQTTManager
from devices.sensors.sensor import Sensor


mqtt = MQTTManager()

mqtt.connect()


sensor = Sensor(
    device_id="sensor01",
    zone="gang_01",
    mqtt=mqtt
)


sensor.detect_presence(True)
