# AuraVision Roadmap

Progress toward a production-ready accessibility tool.

## v0.3.0 — Configuration & Usability ✅

- [x] Centralized config (`config.py`)
- [x] Environment variables (`AV_PORT`, `AV_DEBUG`, etc.)
- [x] Graceful shutdown (signal handling)
- [x] CORS support
- [x] Health check endpoint (`/health`)
- [x] Auto-detect models from `models/` with interactive picker
- [ ] CLI arguments (`--lang fa`, `--model path`)
- [ ] Auto-download models on first run

## v0.4.0 — UI Improvements ✅

- [x] Dark theme with grid background
- [x] RTL support for Farsi (Noto Sans Arabic)
- [x] Transcript history with timestamps
- [x] Audio visualizer animation
- [x] Mobile-responsive layout
- [x] Language auto-detection badge
- [ ] Language selector in browser UI
- [ ] Light/dark theme toggle
- [ ] Screen reader support (ARIA labels)

## v0.5.0 — Deployment ✅

- [x] Docker image (Python 3.11-slim + portaudio)
- [x] Docker Compose with model volume mount
- [ ] ARM-optimized build for Raspberry Pi
- [ ] Systemd service file
- [ ] 3D-printable hardware case
- [ ] Sleep/wake power management

## v0.6.0 — Advanced Features

- [ ] Multi-language simultaneous recognition
- [ ] Word-level confidence scores
- [ ] Export transcript to `.txt` / `.srt`
- [ ] WebSocket auto-reconnect
- [ ] Monitoring dashboard (audio levels, model stats)

## v1.0.0 — Production Release

- [ ] Full test suite (pytest)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Raspberry Pi hardware kit
- [ ] Multi-language documentation (EN, FA, ES)
- [ ] Performance benchmarks
