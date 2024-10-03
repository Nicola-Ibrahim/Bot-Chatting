# Use a single stage for building and running the application
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.0 \
    PATH="/root/.local/bin:$PATH"

# Install dependencies required for Poetry and runtime
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the application
WORKDIR /code

# Copy only the poetry files to leverage Docker layer caching for dependencies
COPY poetry.lock pyproject.toml /code/

# Install project dependencies using Poetry; disable virtual environments
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the entire application code to the container
COPY . /code

# Create a non-root user for better security practices and set permissions
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# Expose the application port (8000) to allow access to the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn, specifying the main application file
CMD ["fastapi", "run", "src/main.py", "--proxy-headers", "--port", "8000"]