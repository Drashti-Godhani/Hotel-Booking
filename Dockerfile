FROM python:3.11-slim

WORKDIR /app

# uv install karo
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dependencies pehle copy karo (cache ke liye)
COPY pyproject.toml .
RUN uv sync --no-dev

# Baaki sab copy karo
COPY . .

EXPOSE 8501