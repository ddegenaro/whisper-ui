#!/bin/bash

# Unix start script for Whisper-UI

echo Starting Whisper-UI. Do not close this window...

# check if pip package whisper-ui is installed or not:

pip show whisper-ui >/dev/null 2>&1

# if not installed, install it:

if [ $? -ne 0 ]; then
    pip install whisper-ui
fi

# run whisper-ui avoid opening a terminal window:

pythonw -m whisper_ui

# exit the script:

exit
