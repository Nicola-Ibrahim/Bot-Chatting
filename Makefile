# Language for translation
lang := en

# Common Docker flags
DOCKER_COMPOSE_FLAGS := -f docker-compose.yml
DOCKER_COMPOSE_DEV_FLAGS := -f docker-compose.dev.yml
DOCKER_BUILD_FLAGS := --build -d --force-recreate
DOCKER_RUN_FLAGS := --rm -p $(HOST_PORT):$(CONTAINER_PORT)

# Catch all targets and store them in a variable
COMMANDS := $(shell grep -E '^[a-zA-Z0-9_-]+:' Makefile | sed 's/:.*//')

# Define color codes
RED    := \033[31m
GREEN  := \033[32m
YELLOW := \033[33m
BLUE   := \033[34m
RESET  := \033[0m

# Default image name
IMAGE_NAME := myapp
# Default host and container ports
HOST_PORT := 8000
CONTAINER_PORT := 8000

UV := uv run

.PHONY: $(COMMANDS)  # Declare all commands as PHONY

list:  # List all commands and their descriptions
	@echo "$(YELLOW)===========================$(RESET)"
	@echo "$(YELLOW)      Available Commands    $(RESET)"
	@echo "$(YELLOW)===========================$(RESET)"
	@printf "$(GREEN)%-30s$(RESET)  %s\n" "Command" "Description"
	@echo "$(YELLOW)---------------------------  --------------------$(RESET)"
	@for cmd in $(COMMANDS); do \
		desc=$$(grep "^$$cmd:" Makefile | sed 's/.*# //'); \
		printf "$(GREEN)%-30s$(RESET)  %s\n" "$$cmd" "$$desc"; \
	done
	@echo "$(YELLOW)===========================$(RESET)"

create-user:  # Create a superuser with administrative privileges
	@echo "Creating superuser..."
	$(UV) python src/scripts/create_superuser.py

gen-sample-users:  # Generate a predefined set of sample users for testing
	@echo "Generating sample users..."
	$(UV) python src/scripts/generate_users.py

lint:  # Run linters to ensure code quality and style consistency
	@echo "Running linters..."
	$(UV) pre-commit run --all-files

migrate:  # Create and apply database migrations for schema changes
	@echo "Creating migrations..."
	$(UV) alembic revision --autogenerate -m "Migration"
	@echo "Applying migrations..."
	$(UV) alembic upgrade head

start:  # Start the FastAPI server with auto-reload in development
	@echo "Starting server..."
	$(UV) fastapi run src/shared/presentation/web/fastapi/main.py --reload

install:  # Install project dependencies using uv
	@echo "Installing dependencies..."
	uv install

install-hooks:  # Install pre-commit hooks to automate code checks
	@echo "Installing hooks..."
	$(UV) pre-commit uninstall
	$(UV) pre-commit install

update-db:  # Create and apply migrations, then install hooks
	@echo "Updating database..."
	$(MAKE) migrate
	$(MAKE) install-hooks

shell:  # Open a Django shell for interactive management
	@echo "Opening shell..."
	$(UV) python src/scripts/shell.py

flush-tokens:  # Remove expired tokens from the database
	@echo "Flushing expired tokens..."
	$(UV) python src/scripts/flush_expired_tokens.py

check:  # Verify the readiness of the deployment environment
	@echo "Checking deployment..."
	$(UV) python src/scripts/check_deploy.py

test:  # Run all tests to ensure application functionality
	@echo "Running tests..."
	$(UV) pytest -v -rs -s -n auto --show-capture=no

test-coverage:  # Run tests with coverage reporting to track code coverage
	@echo "Running tests with coverage..."
	$(UV) pytest --cov
	$(UV) coverage html

dev-docker:  # Start Docker containers for development
	@echo "Starting dev containers..."
	docker-compose $(DOCKER_COMPOSE_DEV_FLAGS) up $(DOCKER_BUILD_FLAGS)

stop-dev:  # Stop and remove development Docker containers
	@echo "Stopping dev containers..."
	docker-compose $(DOCKER_COMPOSE_DEV_FLAGS) down

prod-docker:  # Start Docker containers for production
	@echo "Starting prod containers..."
	docker-compose $(DOCKER_COMPOSE_FLAGS) up $(DOCKER_BUILD_FLAGS)

stop-prod:  # Stop and remove production Docker containers
	@echo "Stopping prod containers..."
	docker-compose $(DOCKER_COMPOSE_FLAGS) down

clean-docker:  # Clean up unused Docker images and volumes to free space
	@echo "Cleaning unused images..."
	docker system prune -f --volumes

dev-logs:  # View real-time logs from development Docker containers
	@echo "Viewing dev logs..."
	docker-compose $(DOCKER_COMPOSE_DEV_FLAGS) logs -f

prod-logs:  # View real-time logs from production Docker containers
	@echo "Viewing prod logs..."
	docker-compose $(DOCKER_COMPOSE_FLAGS) logs -f

gen-jwt:  # Generate a new JWT key for authentication
	@echo "Generating JWT key..."
	openssl rand -base64 32 > src/config/.keys/jwtHS256.key

translate:  # Create translation messages for localization
	@echo "Creating translation messages..."
	django-admin makemessages -l ${lang} --ignore .venv

compile-translate:  # Compile translation messages into bytecode
	@echo "Compiling messages..."
	django-admin compilemessages --ignore=.venv

celery:  # Start a Celery worker for background tasks
	@echo "Starting Celery worker..."
	celery -A src.celery_app worker --loglevel=info --pool=solo

build-docker:  # Build the Docker image for the application
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

run-docker: build-docker  # Run the Docker container based on the built image
	@echo "Running Docker container..."
	docker run $(DOCKER_RUN_FLAGS) $(IMAGE_NAME)

up-docker: build-docker run-docker  # Build and run the Docker container
	@echo "Docker is running."

clean-image:  # Remove the Docker image to reclaim space
	@echo "Cleaning Docker image..."
	docker rmi $(IMAGE_NAME) || true
