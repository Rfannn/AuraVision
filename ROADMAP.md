# AuraVision Roadmap

## v0.3.0 — Configuration & Usability

- [x] Centralized config file (no more hardcoded paths)
- [x] Environment variable support
- [x] Graceful shutdown with signal handling
- [x] CORS support for external devices
- [x] Health check endpoint (`/health`)
- [x] Auto-detect models from `models/` directory with picker
- [ ] CLI arguments for language selection (skip interactive prompt)
- [ ] Auto-download models on first run

## v0.4.0 — UI Improvements

- [x] Dark theme with modern design
- [x] RTL support for Farsi with proper Arabic font
- [x] Transcript history with timestamps
- [x] Audio visualizer
- [x] Mobile-responsive layout
- [ ] Language selector in the browser UI
- [ ] Dark/light theme toggle
- [ ] Accessibility improvements (screen reader support)

## v0.5.0 — Deployment

- [x] Docker image for web server
- [x] Docker Compose setup
- [ ] Optimized audio pipeline for ARM
- [ ] Systemd service file for auto-start
- [ ] Hardware case design (3D-printable)
- [ ] Power management (sleep/wake)

## v0.6.0 — Advanced Features

- [ ] Multi-language simultaneous recognition
- [ ] Confidence scores and word-level timestamps
- [ ] Export transcript to text file
- [ ] WebSocket reconnection handling
- [ ] Logging and monitoring dashboard

## v1.0.0 — Production Release

- [ ] Full test suite
- [ ] CI/CD pipeline
- [ ] Hardware kit available
- [ ] Multi-language documentation
- [ ] Performance benchmarks
