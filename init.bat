@echo off
echo ===================================
echo  AuraVision - Environment Setup
echo ===================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate and install
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Create models directory
if not exist "models" mkdir models

echo.
echo ===================================
echo  Setup complete!
echo ===================================
echo.
echo Next steps:
echo   1. Download Vosk models from https://alphacephei.com/vosk/models
echo   2. Extract model folders into the 'models' directory
echo   3. Run: venv\Scripts\activate ^& python app.py
echo   4. Run: venv\Scripts\activate ^& python main.py
echo.
pause
