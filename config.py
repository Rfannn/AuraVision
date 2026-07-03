import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

MODELS_DIR = BASE_DIR / "models"

MODEL_DOWNLOAD_URLS: dict[str, str] = {
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
FRAMES_PER_BUFFER = 4096

FLASK_HOST = os.getenv("AV_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("AV_PORT", "5000"))
FLASK_DEBUG = os.getenv("AV_DEBUG", "false").lower() == "true"

SECRET_KEY = os.getenv("AV_SECRET_KEY", os.urandom(24).hex())
AUTH_TOKEN = os.getenv("AV_AUTH_TOKEN", "")

LOG_LEVEL = os.getenv("AV_LOG_LEVEL", "ERROR")

KNOWN_LANGS = {"en", "es", "fa"}


def detect_lang(model_name: str) -> str:
    name = model_name.lower()
    if "fa" in name or "farsi" in name or "persian" in name:
        return "fa"
    if "es" in name or "spanish" in name or "espanol" in name:
        return "es"
    if "en" in name or "english" in name:
        return "en"
    return "unknown"


def get_available_models() -> list[dict[str, str]]:
    if not MODELS_DIR.is_dir():
        return []

    models = []
    for entry in sorted(MODELS_DIR.iterdir()):
        if entry.is_dir():
            lang = detect_lang(entry.name)
            models.append({"name": entry.name, "path": str(entry), "lang": lang})
    return models
