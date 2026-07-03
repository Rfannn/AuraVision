# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2026-07-03

### Added
- Microphone device picker (select from available input devices)
- Real-time audio level visualization
- Partial/interim text display (shows text as you speak)
- Auth token for `/update` endpoint (`AV_AUTH_TOKEN`)
- Gunicorn production server
- Docker HEALTHCHECK
- pytest test suite
- CI/CD pipeline (GitHub Actions: lint, test, Docker build)
- CHANGELOG, SECURITY.md, issue/PR templates, CODEOWNERS
- Export transcript to `.txt`
- Accessibility: ARIA labels, `lang` attribute, keyboard navigation
- `python-dotenv` support (`.env` auto-loaded)

### Changed
- CSS and JS split into `static/style.css` and `static/app.js`
- Favicon added
- Dockerfile uses gunicorn instead of Flask dev server
- Socket.IO CDN updated to 4.7.5
- Replaced `print()` with structured logging
- Added type hints to Python code
- Pinned dependency versions in requirements.txt

### Fixed
- `window.history` shadowing bug in transcript log
- Farsi text reversal hack removed (CSS handles RTL)

## [0.3.0] - 2026-07-02

### Added
- Centralized config (`config.py`)
- Environment variable support
- Auto-detect models from `models/` directory
- CORS support
- Health check endpoint
- Dark theme web UI
- RTL support for Farsi
- Docker + Docker Compose
- CONTRIBUTING.md, ROADMAP.md
