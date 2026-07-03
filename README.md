# AuraVision (AV)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker)](Dockerfile)

> Real-time speech-to-text for the deaf and hard-of-hearing community.

AuraVision captures microphone audio, runs it through [Vosk](https://alphacephei.com/vosk/) speech recognition, and displays the text live in your browser. Supports English, Spanish, and Farsi with proper RTL rendering.

## Highlights

- **Real-time transcription** — text appears as you speak
- **Multi-language** — English, Spanish, Farsi (auto-detected from model)
- **RTL support** — Farsi text renders right-to-left with Noto Sans Arabic font
- **Dark UI** — audio visualizer, transcript history, mobile-responsive
- **Docker ready** — one-command setup for the web server
- **Auto-detect models** — drop any Vosk model in `models/` and pick it at startup

## Getting Started

### 1. Clone & Install

```bash
git clone https://github.com/Rfannn/AuraVision.git
cd AuraVision

# Linux / macOS
chmod +x init.sh
./init.sh

# Windows
init.bat
```

### 2. Download Models

Grab Vosk models from [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) and extract into `models/`:

```bash
curl -O https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip
unzip vosk-model-small-fa-0.5.zip -d models/
```

| Language | Model | Size |
|----------|-------|------|
| English | [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) | 40 MB |
| English (large) | [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8 GB |
| Spanish | [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip) | 39 MB |
| Farsi | [vosk-model-small-fa-0.5](https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip) | 47 MB |

Any Vosk model works — the app scans `models/` and lets you choose.

### 3. Run

Two terminals needed:

```bash
# Terminal 1 — Web server
source venv/bin/activate   # Windows: venv\Scripts\activate
python app.py

# Terminal 2 — Speech recognition
source venv/bin/activate
python main.py
```

Open [http://localhost:5000](http://localhost:5000).

### Docker (web server only)

```bash
docker compose up --build
```

The `models/` directory is mounted as a volume. `main.py` must run on the host (needs microphone).

## Configuration

Copy `.env.example` to `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `AV_PORT` | `5000` | Web server port |
| `AV_DEBUG` | `false` | Flask debug mode |
| `AV_SECRET_KEY` | random | Flask session secret |
| `AV_LOG_LEVEL` | `ERROR` | Logging level |

## Architecture

```
Browser ──WebSocket──▶ app.py (Flask + SocketIO) ◀──HTTP POST── main.py ──▶ PyAudio ──▶ Vosk
```

- **`main.py`** — captures microphone audio, runs Vosk recognition, POSTs text to `app.py`
- **`app.py`** — receives text, pushes it to all connected browsers via Socket.IO
- **`config.py`** — shared configuration (paths, audio settings, Flask config)
- **`templates/index.html`** — single-page web UI with live transcript display

## Project Structure

```
AuraVision/
├── app.py              # Flask + SocketIO web server
├── main.py             # Microphone + Vosk speech recognition
├── config.py           # Centralized configuration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container image
├── docker-compose.yml  # Docker Compose config
├── templates/
│   └── index.html      # Web UI
├── models/             # Vosk models (gitignored)
├── init.sh / init.bat  # Setup scripts
├── .env.example        # Env var template
├── CONTRIBUTING.md     # How to contribute
├── ROADMAP.md          # Feature roadmap
└── LICENSE             # MIT
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Speech recognition | [Vosk](https://alphacephei.com/vosk/) |
| Backend | Flask + Flask-SocketIO |
| Audio capture | PyAudio |
| Frontend | Vanilla JS + Socket.IO |
| Fonts | Inter, [Noto Sans Arabic](https://fonts.google.com/noto/specimen/Noto+Sans+Arabic) |
| Container | Docker + Docker Compose |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features.

## License

MIT — see [LICENSE](LICENSE).

## Contact

- **Email:** tsmrfangg@gmail.com
- **Telegram:** @GNS_Rfan
- **Discord:** gnsrfan
