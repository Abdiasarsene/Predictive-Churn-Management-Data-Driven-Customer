FROM python:3.11-slim

# Environment Variable
ENV PYTHONUNBUFFERED=1

# Define working directory
WORKDIR /app

# Copy
COPY . .

# Installer curl pour debug
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Install all dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

# Expose API listening port
EXPOSE 8000

# Launch FastAPI API via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]