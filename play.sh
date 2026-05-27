#!/bin/bash
# Launch the Pokémon Emerald agent under Rosetta (x86_64) on Apple Silicon.
# The mgba emulator binding only ships an Intel-macOS wheel, so we run the
# x86_64 venv (.venv-x86) via Rosetta 2. Any run.py flags pass straight through.
#
# Examples:
#   ./play.sh --agent-auto --record            # play 1 hour, save + journal + exit
#   ./play.sh --agent-auto --record --resume   # continue the next hour
#   ./play.sh --agent-auto --record --session-minutes 30
#
# Then watch at: http://localhost:8000/stream
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x ".venv-x86/bin/python" ]; then
  echo "❌ .venv-x86 not found. Create it first (see ONBOARDING / setup notes)." >&2
  exit 1
fi

exec arch -x86_64 .venv-x86/bin/python run.py "$@"
