#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset variables as errors

# General environment variables for the backend
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
LOG_LEVEL=${LOG_LEVEL:-"info"}

start_api() {
  echo "🌍 Starting API service..."
  exec ./api_entrypoint.sh
}


main() {
  wait_for_db
  initialize_backend
  start_api
}

main


