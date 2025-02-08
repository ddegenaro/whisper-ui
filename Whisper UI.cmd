@echo off
echo Preparing Whisper-UI. Do not close this window...

echo Installing Whisper-UI/checking for updates...

where python >nul 2>nul
if %errorlevel%==0 (
    python -m pip install --upgrade torch openai-whisper whisper_ui
    echo Starting Whisper-UI...
    start /B python -m whisper_ui > whisper_ui.log 2>&1
) else (
    python3 -m pip install --upgrade torch openai-whisper whisper_ui
    echo Starting Whisper-UI...
    start /B python3 -m whisper_ui > whisper_ui.log 2>&1
)

echo Whisper-UI started. Logs are available in whisper_ui.log.
exit
