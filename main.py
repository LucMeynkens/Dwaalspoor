# applicatie starten

from communication.mqtt_manager import MQTTManager
from core.dwaalspoor_core import DwaalSpoorCore


mqtt = MQTTManager()

mqtt.connect()

core = DwaalSpoorCore(
    mqtt
)

core.start()

mqtt.loop_forever()
