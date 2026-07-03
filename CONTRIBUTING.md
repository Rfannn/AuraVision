# Contributing to AuraVision

Thanks for your interest! Here's everything you need to get started.

## Development Setup

### Prerequisites

- Python 3.8+
- `portaudio19-dev` (Linux: `sudo apt install portaudio19-dev`)
- Microphone access

### Local Setup

```bash
git clone https://github.com/Rfannn/AuraVision.git
cd AuraVision
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Setup (web server only)

```bash
docker compose up --build
```

Still need to run `main.py` on the host for microphone access.

### Running

You need two terminals:

```bash
# Terminal 1
python app.py

# Terminal 2
python main.py
```

Open `http://localhost:5000`.

## Making Changes

1. Create a branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Make your changes
3. Test with both `app.py` and `main.py`
4. Commit with a clear message:
   ```bash
   git commit -m "feat: add new feature"
   ```
5. Push and open a PR:
   ```bash
   git push origin feature/your-feature
   ```

### Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `chore:` — build, CI, or tooling changes

## Code Style

- Python: follow PEP 8, 4-space indent
- JavaScript: semicolons, `var`/`let`/`const`, no framework
- Keep functions focused — one thing per function
- No comments unless the logic is non-obvious

## Reporting Bugs

Open an issue with:

1. What you expected
2. What happened
3. Steps to reproduce
4. OS, Python version, browser

## Requesting Features

Open an issue with the `enhancement` label. Describe the **use case**, not just the solution.

## What We Need Help With

- [ ] Raspberry Pi integration & hardware case
- [ ] Additional language support
- [ ] Accessibility (screen reader, keyboard navigation)
- [ ] Testing infrastructure (pytest, CI)
- [ ] Documentation translations
- [ ] Performance profiling on low-end devices
