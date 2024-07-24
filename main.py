import json
import threading
import pyaudio
from vosk import Model, KaldiRecognizer
import colorama
from colorama import Fore, Style
import requests
import logging

# Initialize Colorama
colorama.init()

# Configure logging to suppress Vosk API warnings
logging.basicConfig(level=logging.ERROR)

# Flask server URL
FLASK_SERVER_URL = 'http://localhost:5000/update'

# Display text with Colorama
def display_text(original, lang):
    if lang == 'fa':
        original = original[::-1]
    print(Fore.CYAN + Style.BRIGHT + "Input: " + Style.RESET_ALL + Fore.YELLOW + original)
    print(Style.RESET_ALL)

    # Send text to Flask server
    try:
        response = requests.post(FLASK_SERVER_URL, json={'text': original})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to send text to server: {e}" + Style.RESET_ALL)

# Process audio for Vosk
def process_audio_vosk(recognizer, stream, lang):
    while True:
        try:
            data = stream.read(1024, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                original_text = json.loads(result).get('text', '')
                display_text(original_text, lang)
        except OSError as e:
            print(Fore.RED + f"Error reading audio stream: {e}" + Style.RESET_ALL)
            break

def main():
    # Prompt user to choose language
    print("Choose language (en, es, fa):")
    lang = input().strip().lower()

    # Set the model path and other configurations based on the chosen language
    if lang == 'en':
        model_path = "F:\\AuraVision\\en3"
    elif lang == 'es':
        model_path = "F:\\AuraVision\\es"
    elif lang == 'fa':
        model_path = "F:\\AuraVision\\fa"
    else:
        print("Invalid language choice. Exiting...")
        return

    # Initialize Vosk Model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize Microphone
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    # Run the audio processing in a separate thread
    audio_thread = threading.Thread(target=process_audio_vosk, args=(recognizer, stream, lang))
    audio_thread.start()

    # Keep the main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(Fore.RED + "Exiting..." + Style.RESET_ALL)
        stream.stop_stream()
        stream.close()
        mic.terminate()

if __name__ == "__main__":
    main()
