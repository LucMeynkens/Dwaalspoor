import contextlib
import io
import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from communication.mqtt_manager import MQTTManager
from communication.topics import ALL_SENSOR_POSITION, ALL_SENSOR_PRESENCE
from core.dwaalspoor_core import DwaalSpoorCore


class CoreStartIdempotencyTests(unittest.TestCase):
    def make_core(self):
        client = Mock()
        with patch("communication.mqtt_manager.mqtt.Client", return_value=client):
            mqtt_manager = MQTTManager()
        return DwaalSpoorCore(mqtt_manager), client, mqtt_manager

    def test_single_start_registers_presence_and_position_once(self):
        core, client, mqtt_manager = self.make_core()

        with contextlib.redirect_stdout(io.StringIO()):
            core.start()

        self.assertEqual(client.subscribe.call_args_list, [
            unittest.mock.call(ALL_SENSOR_PRESENCE),
            unittest.mock.call(ALL_SENSOR_POSITION),
        ])
        self.assertEqual(mqtt_manager.callbacks, [
            (ALL_SENSOR_PRESENCE, core.on_presence),
            (ALL_SENSOR_POSITION, core.on_position),
        ])

    def test_three_starts_register_and_dispatch_each_callback_once(self):
        core, client, mqtt_manager = self.make_core()
        core.on_presence = Mock(wraps=core.on_presence)
        core.on_position = Mock(wraps=core.on_position)

        with contextlib.redirect_stdout(io.StringIO()):
            core.start()
            core.start()
            core.start()

        self.assertEqual(client.subscribe.call_count, 2)
        self.assertEqual(len(mqtt_manager.callbacks), 2)

        presence_message = SimpleNamespace(
            topic="dwaalspoor/input/sensor01/presence",
            payload=json.dumps({
                "device": "sensor01",
                "type": "presence",
                "zone": "gang_01",
                "value": False,
                "timestamp": "2026-09-18T23:30:00",
            }).encode("utf-8"),
        )
        position_message = SimpleNamespace(
            topic="dwaalspoor/input/sensor01/position",
            payload=json.dumps({
                "device": "sensor01",
                "type": "position",
                "zone": "gang_01",
                "x": 3.2,
                "y": 1.5,
                "timestamp": "2026-09-18T23:31:00",
            }).encode("utf-8"),
        )

        with contextlib.redirect_stdout(io.StringIO()):
            mqtt_manager._on_message(client, None, presence_message)
            mqtt_manager._on_message(client, None, position_message)

        core.on_presence.assert_called_once_with(client, None, presence_message)
        core.on_position.assert_called_once_with(client, None, position_message)

    def test_retry_after_partial_start_does_not_repeat_successful_registration(self):
        core, client, mqtt_manager = self.make_core()
        attempted_topics = []

        def subscribe(topic):
            attempted_topics.append(topic)
            if topic == ALL_SENSOR_POSITION and attempted_topics.count(topic) == 1:
                raise RuntimeError("simulated position subscription failure")

        client.subscribe.side_effect = subscribe

        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "simulated position"):
                core.start()
            core.start()
            core.start()

        self.assertEqual(
            attempted_topics,
            [ALL_SENSOR_PRESENCE, ALL_SENSOR_POSITION, ALL_SENSOR_POSITION],
        )
        self.assertEqual(len(mqtt_manager.callbacks), 2)
        self.assertEqual(mqtt_manager.callbacks[0][0], ALL_SENSOR_PRESENCE)
        self.assertEqual(mqtt_manager.callbacks[1][0], ALL_SENSOR_POSITION)


if __name__ == "__main__":
    unittest.main()
