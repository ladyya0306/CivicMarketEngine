FROM python:3.10-bookworm

# Install uv and common tools
RUN apt-get update && apt-get install -y curl git && \
    pip install uv && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace/atlas-market-engine

# Copy code
COPY . .

# Set up venv + install runtime and dev deps
RUN uv venv .venv --python=3.10 && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt && \
    uv pip install pytest pre-commit mypy

# Keep container alive for development
CMD ["tail", "-f", "/dev/null"]
