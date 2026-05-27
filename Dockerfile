# Pokémon Emerald agent — Linux image.
# On Apple Silicon this builds as arm64 Linux, where the mgba wheel
# (manylinux2014_aarch64) is self-contained — unlike the broken macOS wheel.
FROM python:3.11-slim

# System libs: opencv needs libGL + glib; tesseract powers OCR dialogue detection.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_NO_CACHE_DIR=1 \
    SDL_VIDEODRIVER=dummy \
    SDL_AUDIODRIVER=dummy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the core dependencies (the ML/local extra is intentionally excluded).
COPY . /app
RUN pip install -e .

# Server (8000) + frame server (8001) for the web stream.
EXPOSE 8000 8001

# Default: autonomous, recording, headless. Override flags via `docker run ... <flags>`.
CMD ["python", "run.py", "--agent-auto", "--record", "--headless"]
