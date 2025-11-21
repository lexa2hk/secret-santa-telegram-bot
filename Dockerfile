# Use Python 3.13 as base image (3.14 may not be available yet in Docker Hub)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY bot/ ./bot/
COPY run.py .

# Create directory for database
RUN mkdir -p /app/data

# Set environment variable for database path
ENV DB_PATH=/app/data/secret_santa.db

# Run the bot
CMD ["python", "run.py"]
