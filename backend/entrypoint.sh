#!/bin/bash
set -e

# Run database migrations
echo "Running Alembic migrations..."
alembic -c pyproject.toml upgrade head

# Start the application or command
echo "Starting..."
exec "$@"
