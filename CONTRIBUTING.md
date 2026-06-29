# Contributing to AuraVision

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

1. Fork and clone the repo
2. Run `./init.sh` (or `init.bat` on Windows)
3. Create a branch for your change:
   ```bash
   git checkout -b feature/your-feature
   ```
4. Make your changes
5. Test locally with both `python app.py` and `python main.py`

## Guidelines

- Keep changes focused — one feature or fix per PR
- Follow existing code style (no linter configured yet, but stay consistent)
- Update the README if you add user-facing features
- Test on at least one platform before submitting

## Reporting Issues

Open an issue on GitHub with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your OS and Python version

## Ideas / Feature Requests

Open an issue with the `enhancement` label. Describe the use case, not just the solution.

## Areas Where Help Is Needed

- Raspberry Pi hardware integration
- Additional language support
- UI/UX improvements (accessibility, mobile layout)
- Performance optimization for low-end devices
- Testing infrastructure
- Documentation and translations
