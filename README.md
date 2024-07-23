# AuraVision (AV) 👁️‍🗨️

AuraVision (AV) is a real-time speech-to-text demo tool designed to assist the deaf and hard-of-hearing community. It converts spoken words into text and displays them in real time. This demo is intended for use on Windows, Linux, and Mac PCs and supports English, Spanish, and Farsi. The final version will be developed as a hardware product using Vosk and Raspberry Pi.

## Features 🌟

- **Real-Time Speech Recognition:** Converts spoken words to text instantly. 🎙️
- **Multi-Language Support:** English, Spanish, and Farsi. 🌎
- **Text Display Options:** Customizable text display, including reversing text for Farsi. 📝
- **Cross-Platform:** Runs on Windows, Linux, and Mac PCs. 💻

## Installation 🛠️

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Rfannn/AuraVision.git
   cd AuraVision
   ```

2. **Install Dependencies:**
   Ensure Python 3.x is installed, then install the required packages:
   ```bash
   pip install vosk pyaudio deep-translator colorama
   ```

3. **Download Language Models:**
   Download Vosk language models and place them in the `C:\\your-path\\` directory. [Vosk Models](https://alphacephei.com/vosk/models).

4. **Alternative Installation (Windows):**
   - Run `init.bat` to automatically set up the environment and install dependencies.
   - Note: Make sure you have administrative privileges to execute batch files.

5. **Alternative Installation (Linux/Mac):**
   - Run `init.sh` to set up the environment and install dependencies.
   - Remember to give execute permissions to the shell script:
     ```bash
     chmod +x init.sh
     ```

3. **Download Language Models:**
Download Vosk language models and place them in the `C:\\your-path\\` directory. [Vosk Models](https://alphacephei.com/vosk/models).

## Usage 🚀

1. **Run the Script:**
```bash
python aura_vision.py
```

2. **Choose Language:**
Enter the language code when prompted:
- `en` for English
- `es` for Spanish
- `fa` for Farsi
The script will load the appropriate model and start processing audio.

3. **View Text:**
Text will appear in the console. For Farsi, text will be reversed.

## Configuration ⚙️

Customize the model paths and other settings in the script as needed. Ensure the paths to language models are correct.

## Future Development 🌐

This demo is designed for PC platforms (Windows, Linux, Mac) and is a precursor to a hardware product that will use Vosk and Raspberry Pi. Stay tuned for updates on the hardware version of AuraVision! 🛠️

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or fixes. Open an issue on GitHub for questions or feature requests.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙌

- Vosk for speech recognition.
- Deep Translator for language translation.
- Colorama for colored text output.


## Contact 📬

Feel free to reach out to me via any of the following channels:

- **Email:** tsmrfangg@gmail.com or erfannasehitabar.bis@gmail.com
- **Telegram:** @GNS_Rfan
- **Discord:** gnsrfan
- **Instagram:** rfan__p

Looking forward to connecting with you! 😊👍
