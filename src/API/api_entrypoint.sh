#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset variables as errors

# Environment variables for the API service
APP_MODULE=${APP_MODULE:-"src.api.main:app"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}
ENVIRONEMENT=${ENVIRONEMENT:-"dev"}


# Function to run the API server
start_api() {
  if [ "$ENVIRONEMENT" = "dev" ]; then
    echo "Starting FastAPI with auto-reload..."
    exec fastapi dev src/api/main.py
  else
    echo "Starting FastAPI..."
    exec fastapi run src/api/main.py
  fi
}

# Main script execution
echo "Initializing API service..."
start_api