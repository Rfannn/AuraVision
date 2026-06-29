#!/bin/bash
set -e

echo "==================================="
echo " AuraVision - Environment Setup"
echo "==================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.8+."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Create models directory
mkdir -p models

echo
echo "==================================="
echo " Setup complete!"
echo "==================================="
echo
echo "Next steps:"
echo "  1. Download Vosk models from https://alphacephei.com/vosk/models"
echo "  2. Extract model folders into the 'models' directory"
echo "  3. Run: source venv/bin/activate && python app.py"
echo "  4. Run: source venv/bin/activate && python main.py"
