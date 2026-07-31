# ─────────────────────────────────────────────────────────────
# Backend Dockerfile — Multi-stage build
# Stage: development  → hot reload, all dev tools
# Stage: production   → slim, gunicorn
# ─────────────────────────────────────────────────────────────

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libmagic1 \
    tesseract-ocr \
    tesseract-ocr-eng \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Create required directories
RUN mkdir -p /app/uploads /app/data /app/.cache/huggingface

# ─────────────────────────────────────────────────────────────
# Development stage
# ─────────────────────────────────────────────────────────────
FROM base AS development

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]

# ─────────────────────────────────────────────────────────────
# Production stage
# ─────────────────────────────────────────────────────────────
FROM base AS production

COPY . .

# Create non-root user
RUN groupadd -r hiresmart && useradd -r -g hiresmart hiresmart && \
    chown -R hiresmart:hiresmart /app

USER hiresmart

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]
