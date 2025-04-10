#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset variables as errors

# Environment variables for the API service
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}
ENVIRONEMENT=${ENVIRONEMENT:-"dev"}


# Function to run the API server
start_api() {
  if [ "$ENVIRONMENT" = "dev" ]; then
    echo "🚀 Starting FastAPI in development mode (auto-reload)"
    uvicorn "$src.api.main:app" \
      --host "$HOST" \
      --port "$PORT" \
      --reload \
      --reload-dir src \
      --log-level debug
  else
    echo "🚀 Starting FastAPI in production mode"
    uvicorn "$src.api.main:app" \
      --host "$HOST" \
      --port "$PORT" \
      --workers "$WORKERS" \
      --log-level info
  fi
}

start_api
