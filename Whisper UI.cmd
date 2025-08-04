@echo off
echo Preparing Whisper-UI. Do not close this window...

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    set PYTHON_NAME=python
) else (
    where python3 >nul 2>&1
    if %ERRORLEVEL%==0 (
        set PYTHON_NAME=python3
    ) else (
        echo Python not found. Please install Python, be sure to add it to your path, and try again.
        pause
        exit /b 1
    )
)

REM Check for FFmpeg
where ffmpeg -version >nul 2>&1
if %ERRORLEVEL%==0 (
    echo FFmpeg found.
) else (
    echo FFmpeg not found. Please install FFmpeg and be sure to add it to your path.
)

REM Setup directories
set VENV_DIR=%USERPROFILE%\.whisper_ui\.venv
set LOG_DIR=%USERPROFILE%\.whisper_ui
set LOG_FILE=%LOG_DIR%\whisper_ui.log

REM Create directory if needed
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Check for virtual environment
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    %PYTHON_NAME% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    
    call "%VENV_DIR%\Scripts\activate"
    
    echo Installing packages...
    %PYTHON_NAME% -m pip install uv
    %PYTHON_NAME% -m uv pip install --upgrade whisper_ui
    %PYTHON_NAME% "%VENV_DIR%\Lib\site-packages\whisper_ui\install_torch.py"
) else (
    echo Using existing virtual environment...
    call "%VENV_DIR%\Scripts\activate"

    echo Checking for updates...
    %PYTHON_NAME% -m uv pip install --upgrade whisper_ui
)

echo Starting Whisper-UI...
start "Whisper-UI" cmd /c "%VENV_DIR%\Scripts\python.exe -m whisper_ui > "%LOG_FILE%" 2>&1"

echo Whisper-UI started. Logs available at: %LOG_FILE%
timeout /t 3 > nul