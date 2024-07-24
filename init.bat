@echo off
echo Setting up AuraVision environment...

:: Install Python dependencies
pip install -r requirements.txt

:: Download Vosk language models (replace with actual download link)
:: Example: curl -o F:\\stt\\en.zip https://example.com/en.zip
:: Unzip the downloaded file to F:\\stt\\

echo Installation completed! You're ready to run AuraVision.
pause
