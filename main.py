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
    MODEL_PATHS,
    MODEL_DOWNLOAD_URLS,
    AUDIO_RATE,
    AUDIO_CHANNELS,
    AUDIO_FORMAT,
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


def check_model(lang):
    from os.path import isdir

    model_path = MODEL_PATHS.get(lang)
    if not model_path:
        return None

    if isdir(model_path):
        return model_path

    url = MODEL_DOWNLOAD_URLS.get(lang)
    if not url:
        return None

    print(Fore.YELLOW + f"Model not found at: {model_path}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Download it from: {url}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Extract to: {MODEL_PATHS.get(lang, 'models/<model-name>')}" + Style.RESET_ALL)
    return None


def main():
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "  AuraVision - Real-Time Speech-to-Text" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print()
    print("Available languages: en, es, fa")
    lang = input("Choose language: ").strip().lower()

    if lang not in MODEL_PATHS:
        print(Fore.RED + "Invalid language. Choose en, es, or fa." + Style.RESET_ALL)
        sys.exit(1)

    model_path = check_model(lang)
    if not model_path:
        sys.exit(1)

    print(Fore.GREEN + f"Loading {lang} model..." + Style.RESET_ALL)
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
