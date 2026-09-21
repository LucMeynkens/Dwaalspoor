# ============================================================
# SENSOR TOPICS
# ============================================================

def sensor_presence(sensor_id):

    return f"dwaalspoor/input/{sensor_id}/presence"


def sensor_position(sensor_id):

    return f"dwaalspoor/input/{sensor_id}/position"


# ============================================================
# ACTUATOR TOPICS
# ============================================================

def actuator_light(actuator_id):

    return f"dwaalspoor/output/{actuator_id}/light"


def actuator_audio(actuator_id):

    return f"dwaalspoor/output/{actuator_id}/audio"


# ============================================================
# AI TOPICS
# ============================================================

def ai_message(ai_id):

    return f"dwaalspoor/output/{ai_id}/message"


def ai_response(ai_id):

    return f"dwaalspoor/input/{ai_id}/response"


# ============================================================
# STATUS TOPICS
# ============================================================

def sensor_status(sensor_id):

    return f"dwaalspoor/status/{sensor_id}/sensor"


def actuator_status(actuator_id):

    return f"dwaalspoor/status/{actuator_id}/actuator"


def ai_status(ai_id):

    return f"dwaalspoor/status/{ai_id}/ai"


# ============================================================
# SUBSCRIPTIONS
# ============================================================

ALL_SENSOR_PRESENCE = \
    "dwaalspoor/input/+/presence"


ALL_SENSOR_POSITION = \
    "dwaalspoor/input/+/position"


ALL_AI_RESPONSES = \
    "dwaalspoor/input/+/response"


ALL_LIGHT_COMMANDS = \
    "dwaalspoor/output/+/light"


ALL_AUDIO_COMMANDS = \
    "dwaalspoor/output/+/audio"


ALL_AI_MESSAGES = \
    "dwaalspoor/output/+/message"
