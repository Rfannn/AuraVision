import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_DOWNLOAD_URLS = {
    "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "en-large": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
    "en-gigaspeech": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip",
    "es": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
    "fa": "https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip",
    "fa-large": "https://alphacephei.com/vosk/models/vosk-model-fa-0.42.zip",
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


def detect_lang(model_name):
    name = model_name.lower()
    if "fa" in name or "farsi" in name or "persian" in name:
        return "fa"
    if "es" in name or "spanish" in name or "espanol" in name:
        return "es"
    if "en" in name or "english" in name:
        return "en"
    return "unknown"


def get_available_models():
    if not os.path.isdir(MODELS_DIR):
        return []

    models = []
    for entry in sorted(os.listdir(MODELS_DIR)):
        path = os.path.join(MODELS_DIR, entry)
        if os.path.isdir(path):
            lang = detect_lang(entry)
            models.append({"name": entry, "path": path, "lang": lang})
    return models
