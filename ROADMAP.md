# AuraVision Roadmap

Progress toward a production-ready accessibility tool.

## v0.3.0 — Configuration & Usability

- [x] Centralized config (`config.py`)
- [x] Environment variables (`AV_PORT`, `AV_DEBUG`, etc.)
- [x] Graceful shutdown (signal handling)
- [x] CORS support
- [x] Health check endpoint (`/health`)
- [x] Auto-detect models from `models/` with interactive picker
- [ ] CLI arguments (`--lang fa`, `--model path`)
- [ ] Auto-download models on first run

## v0.4.0 — UI & Microphone

- [x] Dark theme with grid background
- [x] RTL support for Farsi (Noto Sans Arabic)
- [x] Transcript history with timestamps
- [x] Audio visualizer animation
- [x] Mobile-responsive layout
- [x] Language auto-detection badge
- [x] Microphone device picker
- [x] Real-time audio level display
- [x] Partial/interim text display
- [x] Export transcript to `.txt`
- [x] ARIA labels and keyboard navigation
- [ ] Light/dark theme toggle
- [ ] Language selector in browser UI

## v0.5.0 — Deployment & Quality

- [x] Docker image (gunicorn + eventlet)
- [x] Docker Compose with model volume mount
- [x] Docker HEALTHCHECK
- [x] Auth token for `/update` endpoint
- [x] Structured logging (replaces print)
- [x] Type hints on all functions
- [x] pytest test suite
- [x] CI/CD pipeline (ruff + pytest + Docker build)
- [x] CHANGELOG, SECURITY.md, issue/PR templates
- [x] CSS/JS split from HTML
- [ ] ARM-optimized build for Raspberry Pi
- [ ] Systemd service file
- [ ] 3D-printable hardware case

## v0.6.0 — Advanced Features

- [ ] Multi-language simultaneous recognition
- [ ] Word-level confidence scores
- [ ] WebSocket auto-reconnect
- [ ] Monitoring dashboard (audio levels, model stats)
- [ ] ruff linting in CI (currently manual)

## v1.0.0 — Production Release

- [ ] Raspberry Pi hardware kit
- [ ] Multi-language documentation (EN, FA, ES)
- [ ] Performance benchmarks
- [ ] Code coverage reporting
