lang := en  # Language for translation

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

.PHONY: $(COMMANDS)  # Declare all commands as PHONY

list:  # List all commands
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
	poetry run python src/scripts/create_superuser.py

gen-sample-users:  # Generate a predefined set of sample users for testing
	@echo "Generating sample users..."
	poetry run python src/scripts/generate_users.py

lint:  # Run linters to ensure code quality and style consistency
	@echo "Running linters..."
	poetry run pre-commit run --all-files

migrate:  # Create and apply database migrations for schema changes
	@echo "Creating migrations..."
	poetry run alembic revision --autogenerate -m "Migration"
	@echo "Applying migrations..."
	poetry run alembic upgrade head

start:  # Start the FastAPI server for development
	@echo "Starting server..."
	fastapi run src/shared/presentation/web/fastapi/main.py --reload

install:  # Install project dependencies from Poetry
	@echo "Installing dependencies..."
	poetry install

install-hooks:  # Install pre-commit hooks to automate code checks
	@echo "Installing hooks..."
	poetry run pre-commit uninstall
	poetry run pre-commit install

update-db:  # Create and apply migrations, then install hooks
	@echo "Updating database..."
	$(MAKE) migrate
	$(MAKE) install-hooks

shell:  # Open a Django shell for interactive management
	@echo "Opening shell..."
	poetry run python src/scripts/shell.py

flush-tokens:  # Remove expired tokens from the database
	@echo "Flushing expired tokens..."
	poetry run python src/scripts/flush_expired_tokens.py

check:  # Verify the readiness of the deployment environment
	@echo "Checking deployment..."
	poetry run python src/scripts/check_deploy.py

test:  # Run all tests to ensure application functionality
	@echo "Running tests..."
	poetry run pytest -v -rs -s -n auto --show-capture=no

test-coverage:  # Run tests with coverage reporting to track code coverage
	@echo "Running tests with coverage..."
	poetry run pytest --cov
	poetry run coverage html

dev-docker:  # Start Docker containers for development
	@echo "Starting dev containers..."
	docker-compose -f docker-compose.dev.yml up --build -d --force-recreate

stop-dev:  # Stop and remove development Docker containers
	@echo "Stopping dev containers..."
	docker-compose -f docker-compose.dev.yml down

prod-docker:  # Start Docker containers for production
	@echo "Starting prod containers..."
	docker-compose -f docker-compose.yml up --build -d --force-recreate

stop-prod:  # Stop and remove production Docker containers
	@echo "Stopping prod containers..."
	docker-compose -f docker-compose.yml down

clean-docker:  # Clean up unused Docker images and volumes to free space
	@echo "Cleaning unused images..."
	docker system prune -f --volumes

dev-logs:  # View real-time logs from development Docker containers
	@echo "Viewing dev logs..."
	docker-compose -f docker-compose.dev.yml logs -f

prod-logs:  # View real-time logs from production Docker containers
	@echo "Viewing prod logs..."
	docker-compose -f docker-compose.yml logs -f

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
	docker run --rm -p $(HOST_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

up-docker: build-docker run-docker  # Build and run the Docker container
	@echo "Docker is running."

clean-image:  # Remove the Docker image to reclaim space
	@echo "Cleaning Docker image..."
	docker rmi $(IMAGE_NAME) || true
