@echo off

echo Preparing Whisper-UI. Do not close this window...

@REM check if pip package whisper-ui is installed or not:

pip show whisper-ui >nul 2>&1

@REM if not installed, install it:

if errorlevel 1 (
    echo Installing Python library...
    pip install whisper-ui
)

@REM run whisper-uim avoid opening a terminal window:

echo Starting Whisper-UI...
start /B pythonw -m whisper_ui

@REM exit the script:

exit
