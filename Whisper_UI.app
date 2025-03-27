#!/bin/bash

echo "Preparing Whisper-UI. Do not close this window..."

echo "Installing Whisper-UI/checking for updates..."

if command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg found."
else
    echo "Attempting to install ffmpeg. You may be prompted for your password."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install ffmpeg
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install ffmpeg
    elif command -v brew >/dev/null 2>&1; then
        brew install ffmpeg
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S ffmpeg
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install ffmpeg
    elif command -v apk >/dev/null 2>&1; then
        sudo apk add ffmpeg
    elif command -v pkg >/dev/null 2>&1; then
        sudo pkg install ffmpeg
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install ffmpeg
    elif command -v xbps-install >/dev/null 2>&1; then
        sudo xbps-install -S ffmpeg
    elif command -v emerge >/dev/null 2>&1; then
        sudo emerge -av media-video/ffmpeg
    elif command -v nix-env >/dev/null 2>&1; then
        nix-env -iA nixpkgs.ffmpeg
    elif command -v guix package >/dev/null 2>&1; then
        guix package -i ffmpeg
    else
        echo "Couldn't install ffmpeg for you."
    fi
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
