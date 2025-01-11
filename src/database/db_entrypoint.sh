#!/bin/bash

# Wait for PostgreSQL to be ready
wait_for_db() {
  echo "Waiting for database connection at $DB_HOST:$DB_PORT..."
  until nc -z "$DB_HOST" "$DB_PORT"; do
    echo "Waiting for the database to be ready..."
    sleep 2
  done
  echo "Database is ready!"
}

# Initialize database (Optional: Add database migrations or other startup tasks here)
initialize_db() {
  echo "Running database initialization..."
  # For example, if you want to run migrations:
  # alembic upgrade head  # For SQLAlchemy (replace with appropriate migration tool for your project)
# Run database migrations using Alembic
  echo "Running database migrations..."
  alembic upgrade head
}



# Main entry point
echo "Starting PostgreSQL container..."

# Wait for PostgreSQL to be ready
wait_for_db

# Optional: Run initialization tasks (e.g., migrations)
initialize_db

# Execute the default entrypoint for PostgreSQL to start the server
exec "$@"
