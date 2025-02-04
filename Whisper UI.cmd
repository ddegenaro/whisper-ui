@echo off

echo Preparing Whisper-UI. Do not close this window.

echo Installing Whisper-UI/checking for updates...
pip install torch
pip install -U whisper-ui

echo Starting Whisper-UI...
start /B pythonw -m whisper_ui

exit
