@echo off

echo Starting Whisper-UI. Do not close this window...

@REM check if pip package whisper-ui is installed or not:

pip show whisper-ui >nul 2>&1

@REM if not installed, install it:

if errorlevel 1 (
    pip install whisper-ui
)

@REM run whisper-uim avoid opening a terminal window:

start /B pythonw -m whisper_ui

@REM exit the script:

exit
