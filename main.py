import json
import sys
import threading
import signal

import pyaudio
from vosk import Model, KaldiRecognizer
import colorama
from colorama import Fore, Style
import requests
import logging

from config import (
    MODELS_DIR,
    get_available_models,
    AUDIO_RATE,
    AUDIO_CHANNELS,
    FRAMES_PER_BUFFER,
    FLASK_PORT,
    LOG_LEVEL,
)

colorama.init()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.ERROR))
logger = logging.getLogger(__name__)

FLASK_SERVER_URL = f"http://localhost:{FLASK_PORT}/update"

stop_event = threading.Event()


def display_text(text, lang):
    display = text[::-1] if lang == "fa" else text
    print(Fore.CYAN + Style.BRIGHT + "Input: " + Style.RESET_ALL + Fore.YELLOW + display)
    print(Style.RESET_ALL)

    try:
        resp = requests.post(FLASK_SERVER_URL, json={"text": display}, timeout=2)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to send text to server: {e}" + Style.RESET_ALL)


def process_audio(recognizer, stream, lang):
    while not stop_event.is_set():
        try:
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    display_text(text, lang)
        except OSError as e:
            print(Fore.RED + f"Audio stream error: {e}" + Style.RESET_ALL)
            break


def choose_model():
    models = get_available_models()

    if not models:
        print(Fore.RED + "No models found in models/ directory." + Style.RESET_ALL)
        print()
        print("Download Vosk models from: https://alphacephei.com/vosk/models")
        print(f"Extract them into: {MODELS_DIR}")
        print()
        print("Example:")
        print("  1. Download vosk-model-small-fa-0.5.zip")
        print("  2. Extract so you have models/vosk-model-small-fa-0.5/")
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


def main():
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "  AuraVision - Real-Time Speech-to-Text" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print()

    selected = choose_model()
    model_path = selected["path"]
    lang = selected["lang"]

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
    )
    stream.start_stream()

    print(Fore.GREEN + "Listening... Press Ctrl+C to stop." + Style.RESET_ALL)

    audio_thread = threading.Thread(target=process_audio, args=(recognizer, stream, lang), daemon=True)
    audio_thread.start()

    def shutdown(sig, frame):
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
