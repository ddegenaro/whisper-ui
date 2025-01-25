#!/bin/bash

PACKAGE_NAME="whisper-ui"

# Check if the package is installed
if python3 -m pip show "$PACKAGE_NAME" > /dev/null 2>&1; then
    # Run the package
    python3 -m whisper_ui
else
    # Install the package and run it
    python3 -m pip install "$PACKAGE_NAME" && python3 -m whisper_ui
fi
