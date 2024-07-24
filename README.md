
# AuraVision (AV) 👁️‍🗨️

AuraVision (AV) is a real-time speech-to-text demo tool designed to assist the deaf and hard-of-hearing community. It converts spoken words into text and displays them in real time. This demo is intended for use on Windows, Linux, and Mac PCs and supports English, Spanish, and Farsi. The final version will be developed as a hardware product using Vosk and Raspberry Pi.

## Features 🌟

- **Real-Time Speech Recognition:** Converts spoken words to text instantly. 🎙️
- **Multi-Language Support:** English, Spanish, and Farsi. 🌎
- **Text Display Options:** Customizable text display, including reversing text for Farsi. 📝
- **Cross-Platform:** Runs on Windows, Linux, and Mac PCs. 💻
- **Flask Web Interface:** Displays real-time text updates in a web browser with a simple fade-in animation. 🌐

## Installation 🛠️

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Rfannn/AuraVision.git
   cd AuraVision
   ```

2. **Install Dependencies:**
   Ensure Python 3.x is installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Language Models:**
Download Vosk language models and place them in your desired directory. [Vosk Models](https://alphacephei.com/vosk/models).

4. **Set Up Paths:**
Make sure to set the correct paths for the Vosk models in the code:
```python
if lang == 'en':
    model_path = "your-path-to-english-model"
elif lang == 'es':
    model_path = "your-path-to-spanish-model"
elif lang == 'fa':
    model_path = "your-path-to-farsi-model"
```

4. **Alternative Installation (Windows):**
   - Run `init.bat` to automatically set up the environment and install dependencies.
   - Note: Make sure you have administrative privileges to execute batch files.

5. **Alternative Installation (Linux/Mac):**
   - Run `init.sh` to set up the environment and install dependencies.
   - Remember to give execute permissions to the shell script:
     ```bash
     chmod +x init.sh
     ```

## Usage 🚀

1. **Run the Flask Server:**
```bash
python app.py
```
2. **Run the Speech Recognition Script:**
```bash
python main.py
```

3. **Choose Language:**
Enter the language code when prompted:
- `en` for [English(40mb)](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) / [English Large(1.8gb)](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)
- `es` for [Spanish(39mb)](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip)
- `fa` for [Farsi(47mb)](https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip)

The script will load the appropriate model and start processing audio.

3. **View Text:**
Text will appear in the console. For Farsi, text will be reversed.
Or you could open your web browser and navigate to http://localhost:5000 to see the real-time text updates with a simple fade-in animation.

## Configuration ⚙️

Customize the model paths and other settings in the script as needed. Ensure the paths to language models are correct.

## Future Development 🌐

This demo is designed for PC platforms (Windows, Linux, Mac) and is a precursor to a hardware product that will use Vosk and Raspberry Pi. Stay tuned for updates on the hardware version of AuraVision! 🛠️

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or fixes. Open an issue on GitHub for questions or feature requests.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Rfannn/AuraVision/blob/main/LICENSE) file for details.

## Acknowledgements 🙌

- Vosk for speech recognition.
- Deep Translator for language translation.
- Colorama for colored text output.
- Flask for displaying text output on external devices.


## Contact 📬

Feel free to reach out to me via any of the following channels:

- **Email:** tsmrfangg@gmail.com or erfannasehitabar.bis@gmail.com
- **Telegram:** @GNS_Rfan
- **Discord:** gnsrfan
- **Instagram:** @rfan__p

Looking forward to connecting with you! 😊👍
