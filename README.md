# AuraVision (AV)

Real-time speech-to-text tool for the deaf and hard-of-hearing community. Converts spoken words to text and displays them live in a browser.

## Features

- **Real-time speech recognition** powered by Vosk
- **Multi-language support** — English, Spanish, Farsi
- **RTL support** — proper right-to-left rendering for Farsi
- **Web interface** — live text display with fade-in animation via WebSocket
- **Cross-platform** — Windows, Linux, macOS
- **Configurable** — environment variables for port, debug, secret key, and logging

## Quick Start

### Prerequisites

- Python 3.8+
- Microphone access

### Installation

```bash
git clone https://github.com/Rfannn/AuraVision.git
cd AuraVision

# Linux/macOS
chmod +x init.sh
./init.sh

# Windows
init.bat
```

### Download Language Models

Download from [Vosk Models](https://alphacephei.com/vosk/models) and extract into the `models/` directory:

| Language | Model | Size |
|----------|-------|------|
| English | [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) | 40 MB |
| English (large) | [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8 GB |
| Spanish | [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip) | 39 MB |
| Farsi | [vosk-model-small-fa-0.5](https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip) | 47 MB |

### Run

Start the web server and speech recognition in separate terminals:

```bash
# Terminal 1 - Web server
source venv/bin/activate   # or venv\Scripts\activate on Windows
python app.py

# Terminal 2 - Speech recognition
source venv/bin/activate
python main.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Configuration

Copy `.env.example` to `.env` and customize:

```env
AV_PORT=5000
AV_DEBUG=false
AV_SECRET_KEY=your-random-secret-key
AV_LOG_LEVEL=ERROR
```

## Project Structure

```
AuraVision/
├── app.py              # Flask + SocketIO web server
├── main.py             # Microphone input + Vosk speech recognition
├── config.py           # Centralized configuration
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web UI with live text display
├── models/             # Vosk model files (gitignored)
├── init.sh             # Setup script (Linux/macOS)
├── init.bat            # Setup script (Windows)
├── .env.example        # Environment variable template
└── LICENSE             # MIT License
```

## Tech Stack

- **Speech recognition:** [Vosk](https://alphacephei.com/vosk/)
- **Web framework:** Flask + Flask-SocketIO
- **Audio:** PyAudio
- **Frontend:** Vanilla JS + Socket.IO client

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and milestones.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contact

- **Email:** tsmrfangg@gmail.com
- **Telegram:** @GNS_Rfan
- **Discord:** gnsrfan
