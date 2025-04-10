#!/bin/bash
set -euo pipefail

# Configuration
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_DELAY=${RETRY_DELAY:-2}

# Wait for database to be ready
wait_for_db() {
  echo "🔌 Waiting for database connection at $DB_HOST:$DB_PORT..."
  local attempt=1
  
  while [ $attempt -le $MAX_RETRIES ]; do
    if nc -z -w1 "$DB_HOST" "$DB_PORT"; then
      echo "✅ Database connection established"
      return 0
    fi
    echo "⚠️ Attempt $attempt/$MAX_RETRIES failed. Retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
    ((attempt++))
  done
  
  echo "❌ Failed to connect to database after $MAX_RETRIES attempts"
  return 1
}

# Initialize database (migrations, etc)
initialize_db() {
  echo "⚙️ Running database migrations..."
  alembic upgrade head
  echo "✅ Database initialization completed"
}

# Main execution
echo "Starting database service..."
wait_for_db
initialize_db

# Execute any passed commands (for container entrypoints)
exec "$@"