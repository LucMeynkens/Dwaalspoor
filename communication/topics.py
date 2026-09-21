# communication/topics.py

# ============================================================
# INPUT
# Berichten van apparaten naar de DwaalSpoor-Core
# ============================================================

INPUT_PRESENCE = "dwaalspoor/input/+/presence"
INPUT_POSITION = "dwaalspoor/input/+/position"
INPUT_AI_RESPONSE = "dwaalspoor/input/+/response"


# ============================================================
# OUTPUT
# Commando's van de Core naar apparaten
# ============================================================

OUTPUT_LIGHT = "dwaalspoor/output/+/light"
OUTPUT_AUDIO = "dwaalspoor/output/+/audio"
OUTPUT_AI_MESSAGE = "dwaalspoor/output/+/message"


# ============================================================
# STATUS
# Toestand van apparaten
# ============================================================

STATUS_SENSOR = "dwaalspoor/status/+/sensor"
STATUS_ACTUATOR = "dwaalspoor/status/+/actuator"
STATUS_AI = "dwaalspoor/status/+/ai"
