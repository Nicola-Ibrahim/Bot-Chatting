#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset variables as errors

# General environment variables for the backend
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
LOG_LEVEL=${LOG_LEVEL:-"info"}

# Trigger the API entry point
start_api() {
  echo "Starting the API service..."
  ./src/api/api_entrypoint.sh
}

# Main script execution
echo "Starting the backend..."
wait_for_db
initialize_backend
start_api
