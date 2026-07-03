# AuraVision (AV)

[![CI](https://github.com/Rfannn/AuraVision/actions/workflows/ci.yml/badge.svg)](https://github.com/Rfannn/AuraVision/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker)](Dockerfile)

> Real-time speech-to-text for the deaf and hard-of-hearing community.

AuraVision captures microphone audio, runs it through [Vosk](https://alphacephei.com/vosk/) speech recognition, and displays the text live in your browser. Supports English, Spanish, and Farsi with proper RTL rendering.

## Highlights

- **Real-time transcription** — text appears as you speak, with interim results
- **Multi-language** — English, Spanish, Farsi (auto-detected from model)
- **RTL support** — Farsi text renders right-to-left with Noto Sans Arabic font
- **Microphone picker** — choose input device, see real-time audio levels
- **Dark UI** — audio visualizer, transcript history, export to text file
- **Docker ready** — one-command production setup with gunicorn
- **Auto-detect models** — drop any Vosk model in `models/` and pick it at startup
- **Auth token** — optional `AV_AUTH_TOKEN` for network deployments

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

| Language | Model | Size | Notes |
|----------|-------|------|-------|
| English | [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) | 40 MB | Fast, good for low-end devices |
| English | [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8 GB | Better accuracy |
| English | [vosk-model-en-us-0.42-gigaspeech](https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip) | 2.4 GB | Best accuracy, needs 4GB+ RAM |
| Spanish | [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip) | 39 MB | |
| Farsi | [vosk-model-small-fa-0.5](https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip) | 47 MB | Fast, good for low-end devices |
| Farsi | [vosk-model-fa-0.42](https://alphacephei.com/vosk/models/vosk-model-fa-0.42.zip) | 1.9 GB | Best accuracy, needs 4GB+ RAM |

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

Open [http://localhost:5000](http://localhost:5000). Select your microphone from the dropdown and start speaking.

### Docker (production)

```bash
docker compose up --build
```

The web server runs via gunicorn in the container. `main.py` must run on the host (needs microphone).

## Configuration

Copy `.env.example` to `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `AV_HOST` | `0.0.0.0` | Server bind address |
| `AV_PORT` | `5000` | Server port |
| `AV_DEBUG` | `false` | Flask debug mode |
| `AV_SECRET_KEY` | random | Flask session secret |
| `AV_AUTH_TOKEN` | (empty) | Auth token for `/update` endpoint |
| `AV_LOG_LEVEL` | `ERROR` | Logging level |
| `AV_WORKERS` | `1` | Gunicorn workers |

## Architecture

```
Browser ◀──WebSocket── app.py (Flask + SocketIO) ◀──HTTP POST── main.py ──▶ PyAudio ──▶ Vosk
```

- **`main.py`** — captures microphone audio, runs Vosk recognition, POSTs text to `app.py`
- **`app.py`** — receives text, pushes it to all connected browsers via Socket.IO
- **`config.py`** — shared configuration (paths, audio settings, Flask config, auth)
- **`static/style.css`** — styles
- **`static/app.js`** — frontend logic (mic selection, audio levels, transcript)
- **`templates/index.html`** — minimal HTML shell

## Project Structure

```
AuraVision/
├── app.py              # Flask + SocketIO web server
├── main.py             # Microphone + Vosk speech recognition
├── config.py           # Centralized configuration
├── gunicorn.conf.py    # Production WSGI config
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container image (gunicorn)
├── docker-compose.yml  # Docker Compose config
├── static/
│   ├── style.css       # Styles
│   ├── app.js          # Frontend logic
│   └── favicon.svg     # App icon
├── templates/
│   └── index.html      # HTML shell
├── tests/
│   └── test_app.py     # pytest tests
├── models/             # Vosk models (gitignored)
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── SECURITY.md
└── LICENSE
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Speech recognition | [Vosk](https://alphacephei.com/vosk/) |
| Backend | Flask + Flask-SocketIO |
| Production server | Gunicorn + eventlet |
| Audio capture | PyAudio |
| Frontend | Vanilla JS + Socket.IO |
| Fonts | Inter, [Noto Sans Arabic](https://fonts.google.com/noto/specimen/Noto+Sans+Arabic) |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions (ruff + pytest + Docker build) |
| Testing | pytest |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT — see [LICENSE](LICENSE).

## Contact

- **Email:** tsmrfangg@gmail.com
- **Telegram:** @GNS_Rfan
- **Discord:** gnsrfan
