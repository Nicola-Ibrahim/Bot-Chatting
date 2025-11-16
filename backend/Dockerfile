# Use a single stage for building and running the application
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies required for uv and runtime
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential libpq-dev \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set or change to the working directory for the application
WORKDIR /bot

# Copy only the uv file to leverage Docker layer caching for dependencies
COPY uv.lock pyproject.toml /bot/

# Install project dependencies using uv
RUN uv install

# Copy the entire application code to the container
COPY . /bot

# Create a non-root user for better security practices and set permissions
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# Expose the application port (8000) to allow access to the FastAPI application
EXPOSE 8000

# Add the entrypoint to run the start_backend.sh script
ENTRYPOINT ["./src/backend_entrypoint.sh"]
