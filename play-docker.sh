#!/bin/bash
# Build + run the Pokémon Emerald agent in Docker (arm64 Linux) on Apple Silicon.
# The Linux mgba wheel is self-contained, so this avoids the macOS native-lib problem.
#
# Usage:
#   export GEMINI_API_KEY="..."
#   ./play-docker.sh                       # play 1 hour, save + journal + exit
#   ./play-docker.sh --resume              # continue the next hour
#   ./play-docker.sh --session-minutes 30
#
# Then watch at: http://localhost:8000/stream
# Journals are written to your Obsidian vault's journal/ folder; recordings + the
# resume savestate persist in this repo (mounted into the container).
set -euo pipefail
cd "$(dirname "$0")"

VAULT="${POKEAGENT_VAULT:-/Users/tim/Obsidian Vault/obsidian/qwen-pokemon}"
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY first:  export GEMINI_API_KEY=...}"

echo "🐳 Building image (first time is slow)..."
docker build -t pokeagent .

echo "🎮 Starting — watch at http://localhost:8000/stream  (Ctrl-C to stop)"
docker run --rm -it \
  -p 8000:8000 -p 8001:8001 \
  -e GEMINI_API_KEY \
  -e POKEAGENT_JOURNAL_DIR=/vault/journal \
  -v "$PWD":/app \
  -v "$VAULT":/vault \
  pokeagent \
  python run.py --agent-auto --record --headless --journal-dir /vault/journal "$@"
