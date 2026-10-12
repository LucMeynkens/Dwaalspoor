import contextlib
import io
import json
import unittest
from unittest.mock import Mock

from core.dwaalspoor_core import DwaalSpoorCore
from models.person import Person
from models.zone import Zone


class FakeMQTT:
    def __init__(self):
        self.published = []

    def publish(self, topic, message):
        self.published.append((topic, message))


class FakeMessage:
    def __init__(self, payload):
        self.payload = payload


def make_core():
    core = DwaalSpoorCore(FakeMQTT())

    zone = Zone("held")
    zone.update_presence(
        "sensor-old",
        True,
        "2026-09-18T20:00:00"
    )
    core.zones["held"] = zone

    person = Person("persoon-test")
    person.update_location(
        "held",
        "2026-09-18T20:00:00"
    )
    core.personen[person.person_id] = person
    core.context.update(person)

    core.decision_engine.bepaal_actie = Mock(
        wraps=core.decision_engine.bepaal_actie
    )
    return core


def presence_message(**overrides):
    data = {
        "device": "sensor01",
        "type": "presence",
        "zone": "gang_01",
        "value": True,
        "timestamp": "2026-09-18T23:30:00"
    }
    data.update(overrides)
    return data


def position_message(**overrides):
    data = {
        "device": "sensor02",
        "type": "position",
        "zone": "gang_01",
        "x": 3.2,
        "y": 1.5,
        "timestamp": "2026-09-18T23:31:12"
    }
    data.update(overrides)
    return data


def invoke(core, event_type, payload):
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")

    handler = getattr(core, f"on_{event_type}")
    handler(None, None, FakeMessage(payload))


def core_state(core):
    zones = {
        name: (zone.naam, zone.device, zone.aanwezig, zone.timestamp)
        for name, zone in core.zones.items()
    }
    persons = {
        person_id: (
            person.person_id,
            person.huidige_zone,
            person.vorige_zone,
            person.laatste_detectie,
            list(person.bewegingen)
        )
        for person_id, person in core.personen.items()
    }
    return (
        zones,
        persons,
        dict(core.context.__dict__),
        core.decision_engine.bepaal_actie.call_count,
        list(core.mqtt.published)
    )


class CoreMQTTValidationTests(unittest.TestCase):
    def setUp(self):
        self.output_buffer = io.StringIO()
        self.output_redirect = contextlib.redirect_stdout(self.output_buffer)
        self.output_redirect.__enter__()

    def tearDown(self):
        self.output_redirect.__exit__(None, None, None)

    def test_valid_presence_matrix(self):
        cases = [
            ("true value", presence_message(value=True)),
            ("false value", presence_message(value=False)),
            ("ISO timestamp", presence_message()),
            ("extra field", presence_message(extra="iets")),
            ("unknown device", presence_message(device="sensor99")),
            ("unknown zone", presence_message(zone="gang_99"))
        ]

        for label, data in cases:
            with self.subTest(case=label):
                core = make_core()
                previous_persons = core_state(core)[1]
                previous_context = dict(core.context.__dict__)

                invoke(core, "presence", data)

                zone = core.zones[data["zone"]]
                self.assertEqual(zone.device, data["device"])
                self.assertIs(zone.aanwezig, data["value"])
                self.assertEqual(zone.timestamp, data["timestamp"])

                if data["value"] is False:
                    self.assertEqual(core_state(core)[1], previous_persons)
                    self.assertEqual(core.context.__dict__, previous_context)
                    core.decision_engine.bepaal_actie.assert_not_called()
                else:
                    core.decision_engine.bepaal_actie.assert_called_once()

    def test_invalid_presence_matrix_has_no_state_effect(self):
        cases = [
            ("invalid JSON", b"{ dit is geen json"),
            ("JSON array", ["sensor01", "gang_01", True])
        ]
        for field in ("device", "type", "zone", "value", "timestamp"):
            missing = presence_message()
            del missing[field]
            cases.append((f"missing {field}", missing))

        cases.extend([
            ("empty device", presence_message(device="")),
            ("empty zone", presence_message(zone="")),
            ("wrong type", presence_message(type="presence2")),
            ("string true", presence_message(value="true")),
            ("string false", presence_message(value="false")),
            ("integer one", presence_message(value=1)),
            ("integer zero", presence_message(value=0)),
            ("null value", presence_message(value=None)),
            ("invalid timestamp", presence_message(timestamp="gisterenavond")),
            ("time only", presence_message(timestamp="23:30"))
        ])

        for label, payload in cases:
            with self.subTest(case=label):
                core = make_core()
                before = core_state(core)
                self.output_buffer.seek(0)
                self.output_buffer.truncate(0)
                invoke(core, "presence", payload)
                self.assertEqual(core_state(core), before)
                self.assertIn(
                    "Invalid MQTT presence message",
                    self.output_buffer.getvalue()
                )

    def test_valid_position_matrix_has_no_state_effect(self):
        cases = [
            ("decimal coordinates", position_message()),
            ("integer coordinates", position_message(x=3, y=1)),
            ("negative coordinates", position_message(x=-3.2, y=-1)),
            ("extra field", position_message(extra="iets")),
            ("unknown device", position_message(device="sensor99")),
            ("unknown zone", position_message(zone="gang_99"))
        ]

        for label, data in cases:
            with self.subTest(case=label):
                core = make_core()
                before = core_state(core)
                self.output_buffer.seek(0)
                self.output_buffer.truncate(0)
                invoke(core, "position", data)
                self.assertEqual(core_state(core), before)
                self.assertIn("CORE - POSITIE", self.output_buffer.getvalue())

    def test_invalid_position_matrix_has_no_state_effect(self):
        cases = [
            ("invalid JSON", b"{ dit is geen json"),
            ("JSON array", ["sensor02", "gang_01", 3.2, 1.5])
        ]
        for field in ("device", "type", "zone", "x", "y", "timestamp"):
            missing = position_message()
            del missing[field]
            cases.append((f"missing {field}", missing))

        cases.extend([
            ("empty device", position_message(device="")),
            ("empty zone", position_message(zone="")),
            ("wrong type", position_message(type="position2")),
            ("string x", position_message(x="3.2")),
            ("string y", position_message(y="1.5")),
            ("null x", position_message(x=None)),
            ("null y", position_message(y=None)),
            ("invalid timestamp", position_message(timestamp="gisterenavond"))
        ])

        for label, payload in cases:
            with self.subTest(case=label):
                core = make_core()
                before = core_state(core)
                self.output_buffer.seek(0)
                self.output_buffer.truncate(0)
                invoke(core, "position", payload)
                self.assertEqual(core_state(core), before)
                self.assertIn(
                    "Invalid MQTT position message",
                    self.output_buffer.getvalue()
                )

    def test_nonstandard_json_constants_are_rejected_without_state_effect(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                core = make_core()
                payload = (
                    '{"device":"sensor99","type":"position",'
                    f'"zone":"probe","x":{constant},"y":1,'
                    '"timestamp":"2026-09-18T23:30:00"}'
                ).encode("utf-8")

                before = core_state(core)
                self.output_buffer.seek(0)
                self.output_buffer.truncate(0)
                invoke(core, "position", payload)
                self.assertEqual(core_state(core), before)
                self.assertIn(
                    "Invalid MQTT position message",
                    self.output_buffer.getvalue()
                )

                next_zone = f"after_{constant.replace('-', 'minus')}"
                self.output_buffer.seek(0)
                self.output_buffer.truncate(0)
                invoke(
                    core,
                    "presence",
                    presence_message(value=False, zone=next_zone)
                )
                self.assertIn(next_zone, core.zones)
                self.assertIs(core.zones[next_zone].aanwezig, False)
                core.decision_engine.bepaal_actie.assert_not_called()
                self.assertEqual(core.mqtt.published, [])


if __name__ == "__main__":
    unittest.main()
