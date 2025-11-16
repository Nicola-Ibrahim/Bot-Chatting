#!/usr/bin/env bash
set -Eeuo pipefail

# -----------------------------
# Env (with sane defaults)
# -----------------------------
# Back-compat: if ENVIRONEMENT (typo) is set, use it if ENVIRONMENT is empty
: "${ENVIRONMENT:=${ENVIRONEMENT:-dev}}"

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WORKERS:-1}"

# Logging
if [[ "${ENVIRONMENT}" == "dev" ]]; then
  LOG_LEVEL="${LOG_LEVEL:-debug}"
else
  LOG_LEVEL="${LOG_LEVEL:-info}"
fi

# Uvicorn app import path
APP_MODULE="${APP_MODULE:-src.api.main:app}"

# Reload settings (dev)
RELOAD_DIR="${RELOAD_DIR:-src}"

# Database hints (optional)
DB_HOST="${DB_HOST:-}"
DB_PORT="${DB_PORT:-}"
DB_USER="${DB_USER:-}"
DB_NAME="${DB_NAME:-}"

# Alembic toggle
RUN_MIGRATIONS="${RUN_MIGRATIONS:-true}"

# DB readiness wait config
DB_MAX_RETRIES="${DB_MAX_RETRIES:-30}"
DB_RETRY_DELAY="${DB_RETRY_DELAY:-2}"

# -----------------------------
# Helpers
# -----------------------------
log()  { printf '==> %s\n' "$*"; }
warn() { printf '==> ⚠️  %s\n' "$*" >&2; }
err()  { printf '==> ❌ %s\n' "$*" >&2; }


# -----------------------------
# Start API
# -----------------------------
start_api() {
  if [[ "${ENVIRONMENT}" == "dev" ]]; then
    log "Starting FastAPI in DEVELOPMENT mode (auto-reload) on ${HOST}:${PORT}"
    exec uvicorn "${APP_MODULE}" \
      --host "${HOST}" \
      --port "${PORT}" \
      --reload \
      --reload-dir "${RELOAD_DIR}" \
      --log-level "${LOG_LEVEL}"
  else
    log "Starting FastAPI in PRODUCTION mode on ${HOST}:${PORT} (workers=${WORKERS})"
    exec uvicorn "${APP_MODULE}" \
      --host "${HOST}" \
      --port "${PORT}" \
      --workers "${WORKERS}" \
      --log-level "${LOG_LEVEL}"
  fi
}

# -----------------------------
# Main
# -----------------------------
main() {
  start_api
}

main
