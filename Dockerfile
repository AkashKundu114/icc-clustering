FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt requirements-lock.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pytest-cov ruff mypy

COPY src/ ./src/
COPY configs/ ./configs/
COPY tests/ ./tests/
COPY demo.py ./

RUN pip install --no-cache-dir -e .

CMD ["python", "demo.py"]
