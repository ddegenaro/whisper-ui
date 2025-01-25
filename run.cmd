@echo off

set "PACKAGE_NAME=whisper-ui"

python3 -m pip show %PACKAGE_NAME% >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python -m whisper_ui
) else (
    pip install whisper-ui
    python -m whisper_ui
)
