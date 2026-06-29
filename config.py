import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATHS = {
    "en": os.path.join(MODELS_DIR, "vosk-model-small-en-us-0.15"),
    "es": os.path.join(MODELS_DIR, "vosk-model-small-es-0.42"),
    "fa": os.path.join(MODELS_DIR, "vosk-model-small-fa-0.5"),
}

MODEL_DOWNLOAD_URLS = {
    "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "en-large": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
    "es": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
    "fa": "https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip",
}

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_FORMAT = "paInt16"
FRAMES_PER_BUFFER = 8192

FLASK_HOST = "0.0.0.0"
FLASK_PORT = int(os.environ.get("AV_PORT", 5000))
FLASK_DEBUG = os.environ.get("AV_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("AV_SECRET_KEY", os.urandom(24).hex())

LOG_LEVEL = os.environ.get("AV_LOG_LEVEL", "ERROR")
