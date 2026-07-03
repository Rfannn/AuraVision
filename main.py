import json
import sys
import threading
import signal
import logging
from typing import Any, Optional

import pyaudio
import socketio
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

FLASK_BASE_URL = f"http://localhost:{FLASK_PORT}"
FLASK_SERVER_URL = f"{FLASK_BASE_URL}/update"

stop_event = threading.Event()
mic_lock = threading.Lock()
current_stream: Optional[pyaudio.Stream] = None
current_mic: Optional[pyaudio.PyAudio] = None
current_mic_index: Optional[int] = None


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


def process_audio(recognizer: KaldiRecognizer, lang: str) -> None:
    global current_stream, current_mic

    last_final = ""
    while not stop_event.is_set():
        with mic_lock:
            stream = current_stream
            pa = current_mic

        if stream is None or pa is None:
            stop_event.wait(0.1)
            continue

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
        except OSError:
            stop_event.wait(0.1)
        except Exception as e:
            logger.error("Audio error: %s", e)
            stop_event.wait(0.1)


def switch_mic(new_index: int) -> None:
    global current_stream, current_mic, current_mic_index

    with mic_lock:
        if new_index == current_mic_index:
            return

        if current_stream:
            try:
                current_stream.stop_stream()
                current_stream.close()
            except Exception:
                pass

        if current_mic:
            try:
                current_mic.terminate()
            except Exception:
                pass

        try:
            pa = pyaudio.PyAudio()
            info = pa.get_device_info_by_index(new_index)
            name = info["name"]
            stream = pa.open(
                format=pyaudio.paInt16,
                channels=AUDIO_CHANNELS,
                rate=AUDIO_RATE,
                input=True,
                frames_per_buffer=FRAMES_PER_BUFFER,
                input_device_index=new_index,
            )
            stream.start_stream()
            current_mic = pa
            current_stream = stream
            current_mic_index = new_index
            print(Fore.GREEN + f"\n  Switched to: {name}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"\n  Failed to switch mic: {e}" + Style.RESET_ALL)


def start_mic(index: Optional[int]) -> None:
    global current_stream, current_mic, current_mic_index

    pa = pyaudio.PyAudio()

    if index is None:
        try:
            info = pa.get_default_input_device_info()
            index = info["index"]
        except OSError:
            print(Fore.RED + "No microphone found." + Style.RESET_ALL)
            pa.terminate()
            return

    try:
        info = pa.get_device_info_by_index(index)
        name = info["name"]
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            rate=AUDIO_RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            input_device_index=index,
        )
        stream.start_stream()
        current_mic = pa
        current_stream = stream
        current_mic_index = index
        print(Fore.CYAN + f"  Microphone: {name}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"  Failed to open mic: {e}" + Style.RESET_ALL)
        pa.terminate()


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


def main() -> None:
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
    print(Fore.GREEN + "Model loaded.\n" + Style.RESET_ALL)

    start_mic(None)

    sio = socketio.Client()

    @sio.on("set_mic")
    def on_set_mic(data: dict[str, Any]) -> None:
        idx = data.get("mic_index")
        if idx is not None:
            switch_mic(int(idx))

    @sio.on("connect")
    def on_connect() -> None:
        print(Fore.GREEN + "  Connected to server" + Style.RESET_ALL)

    @sio.on("disconnect")
    def on_disconnect() -> None:
        print(Fore.YELLOW + "  Disconnected from server" + Style.RESET_ALL)

    try:
        sio.connect(FLASK_BASE_URL)
    except Exception as e:
        print(Fore.YELLOW + f"  Could not connect to server: {e}" + Style.RESET_ALL)

    print(Fore.GREEN + "Listening... Press Ctrl+C to stop.\n" + Style.RESET_ALL)

    audio_thread = threading.Thread(target=process_audio, args=(recognizer, lang), daemon=True)
    audio_thread.start()

    def shutdown(sig: int, frame: object) -> None:
        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
        stop_event.set()
        with mic_lock:
            if current_stream:
                try:
                    current_stream.stop_stream()
                    current_stream.close()
                except Exception:
                    pass
            if current_mic:
                try:
                    current_mic.terminate()
                except Exception:
                    pass
        try:
            sio.disconnect()
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    stop_event.wait()


if __name__ == "__main__":
    main()
