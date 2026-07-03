import json
import sys
import threading
import signal
import logging
from typing import Any, Optional

import pyaudio
from vosk import Model, KaldiRecognizer
import colorama
from colorama import Fore, Style
import requests

from config import (
    MODELS_DIR,
    AUTH_TOKEN,
    get_available_models,
    AUDIO_RATE,
    AUDIO_CHANNELS,
    FRAMES_PER_BUFFER,
    FLASK_PORT,
    LOG_LEVEL,
)

colorama.init()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.ERROR),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("auravision.main")

FLASK_SERVER_URL = f"http://localhost:{FLASK_PORT}/update"

stop_event = threading.Event()


def get_headers() -> dict[str, str]:
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        headers["X-Auth-Token"] = AUTH_TOKEN
    return headers


def send_text(text: str, lang: str, partial: bool = False) -> None:
    tag = "..." if partial else ">>>"
    print(Fore.CYAN + Style.BRIGHT + f"  {tag} " + Style.RESET_ALL + Fore.YELLOW + text)
    print(Style.RESET_ALL, end="")

    try:
        resp = requests.post(
            FLASK_SERVER_URL,
            json={"text": text, "lang": lang, "partial": partial},
            headers=get_headers(),
            timeout=2,
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Cannot connect to server. Is app.py running?" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to send text: {e}" + Style.RESET_ALL)


def process_audio(recognizer: KaldiRecognizer, stream: pyaudio.Stream, lang: str) -> None:
    last_final = ""
    while not stop_event.is_set():
        try:
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text and text != last_final:
                    last_final = text
                    send_text(text, lang, partial=False)
            else:
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "").strip()
                if partial_text and partial_text != last_final:
                    send_text(partial_text, lang, partial=True)
        except OSError as e:
            print(Fore.RED + f"Audio stream error: {e}" + Style.RESET_ALL)
            break


def choose_model() -> dict[str, str]:
    models = get_available_models()

    if not models:
        print(Fore.RED + "No models found in models/ directory." + Style.RESET_ALL)
        print()
        print("Download Vosk models from: https://alphacephei.com/vosk/models")
        print(f"Extract them into: {MODELS_DIR}")
        sys.exit(1)

    print(Fore.CYAN + "Available models:" + Style.RESET_ALL)
    print()
    for i, m in enumerate(models, 1):
        lang_label = f"[{m['lang'].upper()}]" if m["lang"] != "unknown" else "[?]"
        print(f"  {Fore.GREEN}{i}{Style.RESET_ALL}. {m['name']}  {Fore.YELLOW}{lang_label}{Style.RESET_ALL}")
    print()

    while True:
        choice = input(f"Choose model (1-{len(models)}): ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(models):
                return models[idx - 1]
        except ValueError:
            pass
        print(Fore.RED + f"Invalid choice. Enter a number between 1 and {len(models)}." + Style.RESET_ALL)


def get_default_mic() -> Optional[int]:
    pa = pyaudio.PyAudio()
    try:
        idx = pa.get_default_input_device_info()["index"]
        name = pa.get_device_info_by_index(idx)["name"]
        print(Fore.CYAN + f"  Microphone: {name}" + Style.RESET_ALL)
        return idx
    except OSError:
        print(Fore.YELLOW + "  No default microphone found" + Style.RESET_ALL)
        return None
    finally:
        pa.terminate()


def main() -> None:
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "  AuraVision - Real-Time Speech-to-Text" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print()

    selected = choose_model()
    model_path = selected["path"]
    lang = selected["lang"]

    mic_index = get_default_mic()

    print()
    print(Fore.GREEN + f"Loading: {selected['name']}..." + Style.RESET_ALL)
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, AUDIO_RATE)
    print(Fore.GREEN + "Model loaded." + Style.RESET_ALL)

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
        input_device_index=mic_index,
    )
    stream.start_stream()

    print(Fore.GREEN + "Listening... Press Ctrl+C to stop.\n" + Style.RESET_ALL)

    audio_thread = threading.Thread(
        target=process_audio, args=(recognizer, stream, lang), daemon=True
    )
    audio_thread.start()

    def shutdown(sig: int, frame: object) -> None:
        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
        stop_event.set()
        stream.stop_stream()
        stream.close()
        mic.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    stop_event.wait()


if __name__ == "__main__":
    main()
