import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import Mock, patch

from communication.mqtt_manager import MQTTManager


class MQTTManagerCallbackErrorTests(unittest.TestCase):
    def test_callback_failure_is_logged_and_dispatch_continues(self):
        client = Mock()
        failing_callback = Mock(side_effect=RuntimeError("callback failed"))
        succeeding_callback = Mock()
        unmatched_callback = Mock()
        message = SimpleNamespace(topic="dwaalspoor/person/alice/presence")

        with patch("communication.mqtt_manager.mqtt.Client", return_value=client):
            manager = MQTTManager()

        manager.callbacks = [
            ("dwaalspoor/person/+/presence", failing_callback),
            ("dwaalspoor/person/alice/#", succeeding_callback),
            ("dwaalspoor/zone/+/presence", unmatched_callback),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            manager._on_message(client, None, message)

        failing_callback.assert_called_once_with(client, None, message)
        succeeding_callback.assert_called_once_with(client, None, message)
        unmatched_callback.assert_not_called()
        self.assertIn(message.topic, output.getvalue())
        self.assertIn("callback failed", output.getvalue())

    def test_manager_processes_next_message_after_callback_failure(self):
        client = Mock()
        failing_callback = Mock(side_effect=RuntimeError("first message failed"))
        succeeding_callback = Mock()
        message1 = SimpleNamespace(topic="dwaalspoor/person/alice/presence")
        message2 = SimpleNamespace(topic="dwaalspoor/person/bob/presence")

        with patch("communication.mqtt_manager.mqtt.Client", return_value=client):
            manager = MQTTManager()

        manager.callbacks = [
            ("dwaalspoor/person/+/presence", failing_callback),
            ("dwaalspoor/person/+/presence", succeeding_callback),
        ]

        with redirect_stdout(io.StringIO()):
            manager._on_message(client, None, message1)
            manager._on_message(client, None, message2)

        self.assertEqual(failing_callback.call_count, 2)
        self.assertEqual(succeeding_callback.call_count, 2)
        succeeding_callback.assert_any_call(client, None, message1)
        succeeding_callback.assert_any_call(client, None, message2)


if __name__ == "__main__":
    unittest.main()
