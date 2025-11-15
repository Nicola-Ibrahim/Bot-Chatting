# ==== Config ====
UV  := uv run
UVX := uvx
COMPOSE := docker compose

# Compose files
DEV_COMPOSE  := -f docker-compose.dev.yml
PROD_COMPOSE := -f docker-compose.yml

# Service names from your compose.yml
API_SERVICE := app
FE_SERVICE  := frontend

# Frontend local defaults
FE_DIR  := frontend
FE_PORT := 3000
FRONTEND_BACKEND_URL ?= http://localhost:8000  # exposed to browser in local FE dev

# ---- Help (targets use '## desc') ----
.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS=":.*## "; printf "\n\033[33m%s\033[0m\n","Available commands"} \
	     /^[a-zA-Z0-9_.-]+:.*## /{printf "  \033[32m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ===========================
# Backend (local, no Docker)
# ===========================
.PHONY: be-install be-fmt be-lint be-test be-coverage be-dev
be-install: ## Install backend deps (uv)
	uv install
be-fmt: ## Format backend code (ruff)
	$(UVX) ruff format src
be-lint: ## Run linters (pre-commit)
	$(UV) pre-commit run --all-files
be-test: ## Run backend tests (pytest)
	$(UV) pytest -v -rs -s -n auto --show-capture=no
be-coverage: ## Tests + coverage report
	$(UV) pytest --cov && $(UV) coverage html
be-dev: ## Run API locally (Uvicorn auto-reload)
	$(UV) uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Backend scripts (optional)
.PHONY: be-user-create be-users-seed be-tokens-flush be-shell
be-user-create: ## Create a superuser
	$(UV) python src/scripts/create_superuser.py
be-users-seed: ## Generate sample users
	$(UV) python src/scripts/generate_users.py
be-tokens-flush: ## Remove expired tokens
	$(UV) python src/scripts/flush_expired_tokens.py
be-shell: ## Open a Python REPL with project env
	$(UV) python -i

# ===========================
# Frontend (local, no Docker)
# ===========================
.PHONY: fe-install fe-dev fe-build fe-start
fe-install: ## Install frontend deps
	cd $(FE_DIR) && npm install
fe-dev: ## Run Next.js dev (http://localhost:$(FE_PORT))
	cd $(FE_DIR) && NEXT_PUBLIC_BACKEND_URL=$(FRONTEND_BACKEND_URL) npm run dev
fe-build: ## Build Next.js
	cd $(FE_DIR) && npm run build
fe-start: ## Start Next.js in prod mode
	cd $(FE_DIR) && npm run start -p $(FE_PORT)

# ===========================
# Database (local CLI)
# ===========================
.PHONY: db-revision db-upgrade
db-revision: ## Create migration (autogenerate)
	$(UV) alembic revision --autogenerate -m "migration"
db-upgrade: ## Apply migrations to head
	$(UV) alembic upgrade head

# ==================================
# Docker Compose (development stack)
# ==================================
.PHONY: dc-up dc-down dc-logs dc-clean
dc-up: ## Start full dev stack (build + detach)
	$(COMPOSE) $(DEV_COMPOSE) up --build -d
dc-down: ## Stop dev stack
	$(COMPOSE) $(DEV_COMPOSE) down
dc-logs: ## Tail dev logs (all services)
	$(COMPOSE) $(DEV_COMPOSE) logs -f
dc-clean: ## Prune dangling images & volumes (careful!)
	docker system prune -f --volumes

# Service-scoped (dev)
.PHONY: dc-be-up dc-be-rebuild dc-be-stop dc-be-logs
dc-be-up: ## Start Backend only (dev)
	$(COMPOSE) $(DEV_COMPOSE) up -d $(API_SERVICE)
dc-be-rebuild: ## Rebuild & restart Backend (dev)
	$(COMPOSE) $(DEV_COMPOSE) up -d --build $(API_SERVICE)
dc-be-stop: ## Stop Backend (dev)
	$(COMPOSE) $(DEV_COMPOSE) stop $(API_SERVICE)
dc-be-logs: ## Tail Backend logs (dev)
	$(COMPOSE) $(DEV_COMPOSE) logs -f $(API_SERVICE)

.PHONY: dc-fe-up dc-fe-rebuild dc-fe-stop dc-fe-logs
dc-fe-up: ## Start Frontend only (dev)
	$(COMPOSE) $(DEV_COMPOSE) up -d $(FE_SERVICE)
dc-fe-rebuild: ## Rebuild & restart Frontend (dev)
	$(COMPOSE) $(DEV_COMPOSE) up -d --build $(FE_SERVICE)
dc-fe-stop: ## Stop Frontend (dev)
	$(COMPOSE) $(DEV_COMPOSE) stop $(FE_SERVICE)
dc-fe-logs: ## Tail Frontend logs (dev)
	$(COMPOSE) $(DEV_COMPOSE) logs -f $(FE_SERVICE)

# ==================================
# Docker Compose (production stack)
# ==================================
.PHONY: dcp-up dcp-down dcp-logs dcp-be-up dcp-be-rebuild dcp-be-stop dcp-be-logs dcp-fe-up dcp-fe-rebuild dcp-fe-stop dcp-fe-logs
dcp-up: ## Start full prod stack (build + detach)
	$(COMPOSE) $(PROD_COMPOSE) up --build -d
dcp-down: ## Stop prod stack
	$(COMPOSE) $(PROD_COMPOSE) down
dcp-logs: ## Tail prod logs (all services)
	$(COMPOSE) $(PROD_COMPOSE) logs -f

# Service-scoped (prod)
dcp-be-up: ## Start Backend only (prod)
	$(COMPOSE) $(PROD_COMPOSE) up -d $(API_SERVICE)
dcp-be-rebuild: ## Rebuild & restart Backend (prod)
	$(COMPOSE) $(PROD_COMPOSE) up -d --build $(API_SERVICE)
dcp-be-stop: ## Stop Backend (prod)
	$(COMPOSE) $(PROD_COMPOSE) stop $(API_SERVICE)
dcp-be-logs: ## Tail Backend logs (prod)
	$(COMPOSE) $(PROD_COMPOSE) logs -f $(API_SERVICE)

dcp-fe-up: ## Start Frontend only (prod)
	$(COMPOSE) $(PROD_COMPOSE) up -d $(FE_SERVICE)
dcp-fe-rebuild: ## Rebuild & restart Frontend (prod)
	$(COMPOSE) $(PROD_COMPOSE) up -d --build $(FE_SERVICE)
dcp-fe-stop: ## Stop Frontend (prod)
	$(COMPOSE) $(PROD_COMPOSE) stop $(FE_SERVICE)
dcp-fe-logs: ## Tail Frontend logs (prod)
	$(COMPOSE) $(PROD_COMPOSE) logs -f $(FE_SERVICE)
