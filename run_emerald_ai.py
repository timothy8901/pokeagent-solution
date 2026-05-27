#!/usr/bin/env python3
"""
run_emerald_ai.py — Pokémon Emerald AI Full Game Runner

Runs the pokeagent-solution agent from the very beginning (title screen)
through to the Elite Four using Google Gemini as the vision model.

Features:
  - Starts from title screen (no savestate needed)
  - Records video of gameplay (mp4)
  - Auto-quits after configurable time, saves game + writes journal to Obsidian vault
  - Supports --resume to continue from last checkpoint
  - Full Elite Four milestone tracking (65 milestones)

Usage:
    cd pokeagent-solution
    python run_emerald_ai.py --record --session-minutes 60
    python run_emerald_ai.py --resume --record --session-minutes 60
"""

import os
import sys
import time
import argparse
import subprocess
import signal
import json
import glob as glob_mod
from pathlib import Path

# ── paths ───────────────────────────────────────────────────────────────
PROJECT_DIR  = Path(__file__).resolve().parent
VENV_PY      = PROJECT_DIR / ".venv" / "bin" / "python"
SESSION_STATE = PROJECT_DIR / ".pokeagent_cache" / "session_latest.state"


# ── helpers ─────────────────────────────────────────────────────────────

def wait_for_server(url, timeout=20):
    """Block until the server responds with HTTP 200."""
    import requests
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}/health", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def find_video_files(project_dir):
    """Find recently created mp4 files in the project dir."""
    files = glob_mod.glob(str(project_dir / "*.mp4"))
    return sorted(files, key=lambda f: os.path.getmtime(f), reverse=True)


# ── main ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pokemon Emerald AI Full Game Runner (Title -> Champion)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  # Fresh start, record video, 60-min session
  python run_emerald_ai.py --record

  # Resume from last session
  python run_emerald_ai.py --resume --record

  # 30-minute session with custom journal dir
  python run_emerald_ai.py --record --session-minutes 30 --journal-dir ~/obsidian/vault
        """,
    )
    parser.add_argument("--resume",  action="store_true", help="Resume from last savestate")
    parser.add_argument("--backend", default="gemini",    help="VLM backend (gemini or openai)")
    parser.add_argument("--model",   default="gemini-2.5-flash", help="Model name")
    parser.add_argument("--scaffold", default="simple",   choices=["simple", "react", "fourmodule"])
    parser.add_argument("--session-minutes", type=int, default=60, help="Run for N minutes then quit (default: 60)")
    parser.add_argument("--journal-dir", type=str, default=None, help="Obsidian vault / journal directory")
    parser.add_argument("--port",    type=int, default=8000, help="Server HTTP port")
    parser.add_argument("--record",  action="store_true", default=None, help="Record video to mp4")
    parser.add_argument("--no-record", action="store_true", help="Disable video recording")
    parser.add_argument("--headless", action="store_true", default=True, help="No display window")
    parser.add_argument("--rom",     type=str, default=None, help="ROM file path")
    args = parser.parse_args()

    # ── ROM path ──
    if args.rom is None:
        args.rom = str(PROJECT_DIR / "Emerald-GBAdvance" / "rom.gba")

    # ── Journal dir ──
    if args.journal_dir is None:
        vault_candidate = Path.home() / "Obsidian Vault"
        if vault_candidate.exists():
            args.journal_dir = str(vault_candidate)
        else:
            args.journal_dir = str(Path.home() / "Desktop" / "pokemon-emerald-journal")
    os.makedirs(args.journal_dir, exist_ok=True)

    # ── Video recording ──
    record = (args.record is True) and (args.no_record is not True)

    # ── Print summary ──
    print("=" * 62)
    print("  Pokemon Emerald AI — Full Game Runner")
    print("  (Title Screen -> Elite Four -> Champion)")
    print("=" * 62)
    print(f"  Python          {VENV_PY}")
    print(f"  ROM             {args.rom}")
    print(f"  Backend         {args.backend}/{args.model}")
    print(f"  Scaffold        {args.scaffold}")
    print(f"  Session limit   {args.session_minutes} min")
    print(f"  Journal         {args.journal_dir}")
    print(f"  Video record    {'ON' if record else 'OFF'}")
    print(f"  Resume          {args.resume}")
    print("=" * 62)

    # ── Start server process ──
    server_cmd = [
        str(VENV_PY), "-m", "server.app",
        "--port", str(args.port),
        "--rom", args.rom,
    ]
    server_cmd.append("--headless")
    if record:
        server_cmd.append("--record")
    if args.resume and SESSION_STATE.exists():
        server_cmd.extend(["--load-state", str(SESSION_STATE)])

    print(f"\n[server] Starting FastAPI server (PID: {subprocess.Popen(server_cmd).pid})...")
    server_proc = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    server_pid = server_proc.pid

    server_url = f"http://localhost:{args.port}"
    print("[server] Waiting for health check...")
    if not wait_for_server(server_url):
        for line in iter(server_proc.stdout.readline, ""):
            print(f"[server] {line.rstrip()}")
        print("[server] ERROR: Health check never succeeded.")
        server_proc.terminate()
        sys.exit(1)
    print("[server] Ready! (http://127.0.0.1:{args.port}/stream)")

    # ── Start agent process ──
    client_cmd = [
        str(VENV_PY), str(PROJECT_DIR / "run.py"),
        "--backend", args.backend,
        "--model-name", args.model,
        "--scaffold", args.scaffold,
        "--session-minutes", str(args.session_minutes),
        "--journal-dir", args.journal_dir,
        "--headless",
        "--agent-auto",
    ]
    if record:
        client_cmd.append("--record")
    if not record:
        client_cmd.append("--no-record")
    if args.resume and SESSION_STATE.exists():
        client_cmd.append("--resume")

    print(f"\n[agent] Starting AI agent loop...")
    client_proc = subprocess.Popen(
        client_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    client_pid = client_proc.pid
    print(f"[agent] Agent PID: {client_pid}")
    print("-" * 62)

    # ── Stream combined output ──
    try:
        print("[output] Live output (Ctrl-C to stop):")
        print("-" * 62)

        # Stream server output
        for line in server_proc.stdout:
            print(f"[server] {line.rstrip()}")
            if not line.strip():
                break

        # Stream client (agent) output
        for line in client_proc.stdout:
            print(f"[agent]  {line.rstrip()}")
            if not line.strip():
                break
    except KeyboardInterrupt:
        print("\n\n[!] Interrupt received — shutting down...")
    finally:
        # ── Cleanup ──
        for name, proc in [("agent", client_proc), ("server", server_proc)]:
            if proc.poll() is None:
                print(f"\n[stop]  Terminating {name} (PID {proc.pid})...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"[stop]  Force killing {name}...")
                    proc.kill()
            else:
                print(f"[stop]  {name} already exited (code {proc.returncode})")

        # ── Report ──
        print("\n" + "=" * 62)
        print("  Session complete.")
        print("=" * 62)
        print(f"  Savestate:    {SESSION_STATE}")
        print(f"  Journal dir:  {args.journal_dir}")
        print(f"  LLM logs:     {PROJECT_DIR / 'llm_logs'}")

        # Video files
        videos = find_video_files(PROJECT_DIR)
        if videos:
            print(f"\n  Video recordings:")
            for v in videos[:5]:  # Show latest 5
                size_mb = os.path.getsize(v) / 1e6
                print(f"    {Path(v).name}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
