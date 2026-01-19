FROM python:3.12-slim

# System deps (often needed for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project metadata first (better caching)
COPY pyproject.toml README.md ./

# Copy source
COPY src ./src

# Install uv and deps
RUN pip install --no-cache-dir uv \
 && uv pip install --system -e .

# Expose API port
EXPOSE 8542

# Start your CLI entrypoint which starts the API
CMD ["investment-research-crew"]