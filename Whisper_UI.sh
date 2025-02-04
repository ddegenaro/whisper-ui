#!/bin/bash

# Check if the script is executable and prompt to make it so if not
if [ ! -x "$0" ]; then
    echo "This script is not executable. Making it executable now..."
    chmod +x "$0"
    echo "Re-run the script now: ./$0"
    exit
fi

echo "Preparing Whisper-UI. Do not close this window..."

echo Installing Whisper-UI/checking for updates...
pip install torch
pip install -U whisper-ui
pip3 install torch
pip3 install -U whisper-ui

# Run whisper-ui in the background, avoid opening a terminal window
echo "Starting Whisper-UI..."
pythonw -m whisper_ui

# Exit the script
exit
