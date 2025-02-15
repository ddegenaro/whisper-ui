#!/bin/bash

echo "Preparing Whisper-UI. Do not close this window..."

echo "Installing Whisper-UI/checking for updates..."

if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get install ffmpeg
elif command -v yum >/dev/null 2>&1; then
    sudo yum install ffmpeg
elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
else
    echo "Couldn't install ffmpeg for you."
fi

if command -v python >/dev/null 2>&1; then
    python -m pip install --upgrade torch openai-whisper whisper_ui
    echo "Starting Whisper-UI..."
    nohup python -m whisper_ui > whisper_ui.log 2>&1 &
else
    python3 -m pip install --upgrade torch openai-whisper whisper_ui
    echo "Starting Whisper-UI..."
    nohup python3 -m whisper_ui > whisper_ui.log 2>&1 &
fi

echo "Whisper-UI started. Logs are available in whisper_ui.log."
exit
