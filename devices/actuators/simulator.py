# code voor een gesimuleerde actuator

from communication.mqtt_manager import MQTTManager
from devices.actuators.actuator import Actuator


mqtt = MQTTManager()

mqtt.connect()


actuator = Actuator(
    device_id="actuator01",
    mqtt=mqtt
)

actuator.start()

mqtt.loop_forever()
