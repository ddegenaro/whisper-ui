#!/bin/bash

echo "Preparing Whisper-UI. Do not close this window..."

echo "Installing Whisper-UI/checking for updates..."
python3 -m pip install --upgrade torch whisper whisper-ui

# Run whisper-ui in the background and log output
echo "Starting Whisper-UI..."
nohup python3 -m whisper_ui > whisper_ui.log 2>&1 &

echo "Whisper-UI started. Logs are available in whisper_ui.log."
exit
