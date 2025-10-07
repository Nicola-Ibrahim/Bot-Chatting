#!/bin/bash
set -euo pipefail

# Configuration
MAX_RETRIES=${POSTGRES_MAX_RETRIES:-30}
RETRY_DELAY=${POSTGRES_RETRY_DELAY:-2}

# Wait for database to be ready
wait_for_db() {
  echo "🔌 Waiting for database connection at $POSTGRES_HOST:$POSTGRES_PORT..."
  local attempt=1

  while [ $attempt -le $MAX_RETRIES ]; do
    if pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; then
      echo "✅ Database connection established"
      return 0
    fi
    echo "⚠️ Attempt $attempt/$MAX_RETRIES failed. Retrying in $POSTGRES_RETRY_DELAY seconds..."
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
# initialize_db

# Execute any passed commands (for container entrypoints)
exec "$@"