lang := en  # Language for translation

# Catch all targets and store them in a variable
COMMANDS := $(shell grep -E '^[a-zA-Z0-9_-]+:' Makefile | sed 's/:.*//')

# Define color codes
RED    := \033[31m
GREEN  := \033[32m
YELLOW := \033[33m
BLUE   := \033[34m
RESET  := \033[0m

.PHONY: $(COMMANDS)  # Declare all commands as PHONY


list:  # List all available commands with descriptions
	@printf "$(YELLOW)Available commands:$(RESET)\n"
	@printf "$(YELLOW)=====================$(RESET)\n"
	@printf "\n"
	@printf "%-20s  %s\n" "Command" "Description"  # Header without colors
	@printf "$(YELLOW)---------------------  --------------------$(RESET)\n"
	@for cmd in $(COMMANDS); do \
		desc=$$(grep "^$$cmd:" Makefile | sed 's/.*# //'); \
		printf "%-20s  %s\n" "$$cmd" "$$desc"; \
	done


# Define your targets with descriptions
superuser:  # Create a superuser
	poetry run python src/scripts/create_superuser.py

users:  # Generate sample users
	poetry run python src/scripts/generate_users.py

lint:  # Run linters
	poetry run pre-commit run --all-files

migrations:  # Create new migrations
	poetry run alembic revision --autogenerate -m "Migration message"

migrate:  # Apply database migrations
	poetry run alembic upgrade head

runserver:  # Start the FastAPI server
	fastapi run src/main.py --reload

install:  # Install project dependencies
	poetry install

install-pre-commit:  # Install pre-commit hooks
	poetry run pre-commit uninstall
	poetry run pre-commit install

update:  # Update the database and install pre-commit hooks
	migrations migrate install-pre-commit

shell:  # Open Django shell
	poetry run python src/scripts/shell.py

flush-tokens:  # Flush expired tokens
	poetry run python src/scripts/flush_expired_tokens.py

check-deploy:  # Check deployment readiness
	poetry run python src/scripts/check_deploy.py

db-graph:  # Generate database graph
	poetry run python src/scripts/db_graph.py

test:  # Run tests
	poetry run pytest -v -rs -s -n auto --show-capture=no

test-cov:  # Run tests with coverage
	poetry run pytest --cov
	poetry run coverage html

dev-docker:  # Start development Docker containers
	docker-compose -f docker-compose.dev.yml up --build -d --force-recreate

prod-docker:  # Start production Docker containers
	docker-compose -f docker-compose.yml up --build -d --force-recreate

generate_key:  # Generate a new JWT key
	openssl rand -base64 32 > src/config/.keys/jwtHS256.key

translate:  # Create translation messages
	django-admin makemessages -l ${lang} --ignore .venv

compile-translate:  # Compile translation messages
	django-admin compilemessages --ignore=.venv

run-celery:  # Run Celery worker
	celery -A src.celery_app worker --loglevel=info --pool=solo

