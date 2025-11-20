# ==== Config ====
UV  := uv run
UVX := uvx
COMPOSE := docker compose

# Backend directory
BACKEND_DIR := backend

# Compose files
DEV_COMPOSE  := -f docker-compose.dev.yml
PROD_COMPOSE := -f docker-compose.yml

# Service names from your compose.yml
API_SERVICE := app
FE_SERVICE  := frontend

# Frontend local defaults
FRONTEND_DIR  := frontend
FE_PORT := 3000
FRONTEND_BACKEND_URL ?= http://localhost:8000  # exposed to browser in local FE dev

# ---- Help (targets use '## desc') ----
.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS=":.*## "; printf "\n\033[33m%s\033[0m\n","Available commands"} \
	     /^[a-zA-Z0-9_.-]+:.*## /{printf "  \033[32m%-36s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ===========================
# Backend (local, no Docker)
# ===========================
.PHONY: backend-format backend-lint backend-test backend-test-coverage backend-run-dev

backend-format: ## Format backend code using ruff
	cd $(BACKEND_DIR) && $(UVX) ruff format src

backend-lint: ## Run backend linters (pre-commit)
	cd $(BACKEND_DIR) && $(UV) pre-commit run --all-files

backend-test: ## Run backend tests (pytest)
	cd $(BACKEND_DIR) && $(UV) pytest -v -rs -s -n auto --show-capture=no

backend-test-coverage: ## Run backend tests with coverage report
	cd $(BACKEND_DIR) && $(UV) pytest --cov && $(UV) coverage html

backend-run-dev: ## Run backend API locally with Uvicorn (auto-reload)
	cd $(BACKEND_DIR) && $(UV) python -m src.server

# Backend scripts (optional)
.PHONY: backend-create-superuser backend-generate-sample-users backend-flush-expired-tokens backend-shell
backend-create-superuser: ## Create a backend superuser
	cd $(BACKEND_DIR) && $(UV) python src/scripts/create_superuser.py

backend-generate-sample-users: ## Generate sample backend users
	cd $(BACKEND_DIR) && $(UV) python src/scripts/generate_users.py

backend-flush-expired-tokens: ## Remove expired auth tokens
	cd $(BACKEND_DIR) && $(UV) python src/scripts/flush_expired_tokens.py

backend-shell: ## Open a Python REPL with backend environment
	cd $(BACKEND_DIR) && $(UV) python -i

# ===========================
# Frontend (local, no Docker)
# ===========================
.PHONY: frontend-install-deps frontend-run-dev frontend-build frontend-run-prod
frontend-install-deps: ## Install frontend dependencies (npm install)
	cd $(FRONTEND_DIR) && npm install

frontend-run-dev: ## Run Next.js dev server (http://localhost:$(FE_PORT))
	cd $(FRONTEND_DIR) && npm run dev

frontend-build: ## Build Next.js frontend for production
	cd $(FRONTEND_DIR) && npm run build

frontend-run-prod: ## Start Next.js in production mode
	cd $(FRONTEND_DIR) && npm run start -p $(FE_PORT)

# Dockerized frontend dev (build and run image from frontend/)
.PHONY: frontend-run-dev-docker
frontend-run-dev-docker: ## Build & run frontend Docker image for development
	cd $(FRONTEND_DIR) && \
	  docker build -t chat-frontend-dev . && \
	  docker run --rm -p $(FE_PORT):3000 \
	    -e BACKEND_URL=$(FRONTEND_BACKEND_URL) \
	    chat-frontend-dev

# ===========================
# Database (local CLI)
# ===========================
.PHONY: db-create-migration db-apply-migrations
db-create-migration: ## Create a new Alembic migration (autogenerate)
	cd $(BACKEND_DIR) && $(UV) alembic -c alembic.ini revision --autogenerate -m "migration"

db-apply-migrations: ## Apply all Alembic migrations to head
	cd $(BACKEND_DIR) && $(UV) alembic -c alembic.ini upgrade head

# ==================================
# Docker Compose (development stack)
# ==================================
.PHONY: dev-stack-up dev-stack-down dev-stack-logs docker-clean-system
dev-stack-up: ## Start full development stack (build + detach)
	$(COMPOSE) $(DEV_COMPOSE) up --build -d

dev-stack-down: ## Stop development stack
	$(COMPOSE) $(DEV_COMPOSE) down

dev-stack-logs: ## Tail development stack logs (all services)
	$(COMPOSE) $(DEV_COMPOSE) logs -f

docker-clean-system: ## Prune dangling Docker images and volumes (careful!)
	docker system prune -f --volumes

# ==================================
# Docker Compose (production stack)
# ==================================
.PHONY: prod-stack-up prod-stack-down prod-stack-logs
prod-stack-up: ## Start full production stack (build + detach)
	$(COMPOSE) $(PROD_COMPOSE) up --build -d

prod-stack-down: ## Stop production stack
	$(COMPOSE) $(PROD_COMPOSE) down

prod-stack-logs: ## Tail production stack logs (all services)
	$(COMPOSE) $(PROD_COMPOSE) logs -f
