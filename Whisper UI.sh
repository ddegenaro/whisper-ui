#!/bin/bash

# Check if the script is executable and prompt to make it so if not
if [ ! -x "$0" ]; then
    echo "This script is not executable. Making it executable now..."
    chmod +x "$0"
    echo "Re-run the script now: ./$0"
    exit
fi

echo "Preparing Whisper-UI. Do not close this window..."

# Check if the pip package 'whisper-ui' is installed
pip show whisper-ui > /dev/null 2>&1

# If not installed, install it
if [ $? -ne 0 ]; then
    echo "Installing Python library..."
    pip install whisper-ui
fi

# Run whisper-ui in the background, avoid opening a terminal window
echo "Starting Whisper-UI..."
nohup pythonw -m whisper_ui > /dev/null 2>&1 &

# Exit the script
exit
