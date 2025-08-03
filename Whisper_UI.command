#!/bin/bash

echo "Preparing Whisper-UI. Do not close this window..."

# Check for Python
if command -v python3 &>/dev/null; then
    PYTHON_NAME=python3
elif command -v python &>/dev/null; then
    PYTHON_NAME=python
else
    echo "Python not found. Please install Python, be sure to add it to your path, and try again."
    read -p "Press any key to exit..."
    exit 1
fi

# Check for ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo "FFmpeg not found. Please install FFmpeg, be sure to add it to your path, and try again."
    read -p "Press any key to exit..."
    exit 1
else
    echo "FFmpeg found."
fi

# Setup directories
VENV_DIR="$HOME/.whisper_ui/.venv"
LOG_DIR="$HOME/.whisper_ui"
LOG_FILE="$LOG_DIR/whisper_ui.log"
TMP_DIR="$HOME/.whisper_ui/tmp"

# Create directories if needed
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi
if [ ! -d "$TMP_DIR" ]; then
    mkdir -p "$TMP_DIR"
fi

# Check for virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_NAME -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        read -p "Press any key to exit..."
        exit 1
    fi
    
    source "$VENV_DIR/bin/activate"
    
    echo "Installing packages..."
    $PYTHON_NAME -m pip install uv
    $PYTHON_NAME -m uv pip install whisper_ui==1.2.16
    $PYTHON_NAME "$VENV_DIR/Lib/site-packages/whisper_ui/install_torch.py"
else
    echo "Using existing virtual environment..."
    source "$VENV_DIR/bin/activate"

    echo "Checking for updates..."
    $PYTHON_NAME -m uv pip install whisper_ui==1.2.16
fi

echo "Starting Whisper-UI..."
nohup "$VENV_DIR/bin/python" -m whisper_ui > "$LOG_FILE" 2>&1 &

echo "Whisper-UI started. Logs available at: $LOG_FILE"
sleep 3