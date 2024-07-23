from vosk import Model, KaldiRecognizer
import pyaudio
from deep_translator import GoogleTranslator
import colorama
from colorama import Fore, Style
import threading

# Initialize Colorama
colorama.init()

# Function to display text with colorama
def display_text(original, lang):
    if lang == 'fa':
        original = original[::-1]
    print(Fore.CYAN + Style.BRIGHT + "Input: " + Style.RESET_ALL + Fore.YELLOW + original)
    print(Style.RESET_ALL)

# Function to process audio
def process_audio(recognizer, stream, lang):
    while True:
        data = stream.read(4096)
        
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            original_text = result[14:-3]
            # Uncomment the following lines if you want translation
            # if lang != 'fa':
            #     translated_text = GoogleTranslator(source='en', target='fa').translate(original_text)
            #     display_text(translated_text, lang)
            display_text(original_text, lang)

# Prompt user to choose language
print("Choose language (en, es, fa):")
lang = input().strip().lower()

# Set the model path and other configurations based on the chosen language
if lang == 'en':
    model_path = "F:\\stt\\en"
elif lang == 'es':
    model_path = "F:\\stt\\es"
elif lang == 'fa':
    model_path = "F:\\stt\\fa"
else:
    print("Invalid language choice. Exiting...")
    exit()

# Initialize Vosk Model
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Initialize Microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Run the audio processing in a separate thread
audio_thread = threading.Thread(target=process_audio, args=(recognizer, stream, lang))
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
