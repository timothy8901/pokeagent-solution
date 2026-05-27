# 🎮 Pokemon Emerald AI Speedrun — Quick Start

**AI plays the full Pokemon Emerald game from title screen to Champion using Google Gemini.**

## Prerequisites (✅ Already Met)

- ✅ Valid Pokemon Emerald ROM: `Emerald-GBAdvance/rom.gba`
- ✅ mGBA 0.10.5 installed (Homebrew)
- ✅ Gemini API key (provided)
- ✅ All Python dependencies in `.venv-x86`

## Run the AI

### Option 1: 60-minute session with video recording

```bash
cd /Users/tim/pokeagent-solution
export GEMINI_API_KEY="AIzaSyBVmkcflA_uiJucUUh9eWxSt4mX8vXqCFI"
python run_emerald_ai.py --record --session-minutes 60
```

### Option 2: Resume from last session

```bash
python run_emerald_ai.py --resume --record --session-minutes 60
```

### Option 3: 30-minute session with custom journal

```bash
python run_emerald_ai.py --record --session-minutes 30 --journal-dir ~/obsidian/vault
```

## What Happens

1. **Server starts** (mGBA emulator, headless, FastAPI on port 8000)
2. **Agent starts** (Gemini vision model, auto-play mode)
3. **AI sees game frames**, makes decisions via Gemini VLM
4. **Video recorded** to `*.mp4` files in project directory
5. **Savestates saved** every 10 steps (`.pokeagent_cache/session_latest.state`)
6. **After 60 minutes**: auto-saves, writes journal, quits
7. **Journal** written to your Obsidian vault with:
   - What was accomplished this session
   - What the AI would do with 15-20 more minutes

## Progression Path (61 milestones)

```
Title → Mudkip → Route 101 → Oldale → Pokedex → Route 102
→ Petalburg City → Brawly (Gym 1) → Rustboro (Gym 2)
→ Dewford (Gym 3) → Lavaridge (Gym 4) → Pacifidlog (Gym 5)
→ Fortree (Gym 6) → Mossdeep (Gym 7) → Sootopolis (Gym 8)
→ Pokemon League → Elite Four (Sidney, Phoebe, Glacia, Drake)
→ Champion Wallace → GAME COMPLETE
```

## File Reference

| Item | Path |
|------|------|
| Runner | `run_emerald_ai.py` |
| ROM | `Emerald-GBAdvance/rom.gba` |
| Savestate | `.pokeagent_cache/session_latest.state` |
| Video | `pokeagent_recording_*.mp4` |
| Journal | `~/Obsidian Vault/` (or custom dir) |
| LLM Logs | `llm_logs/` |
| Milestones | `milestone_config.json` (65) + `utils/milestone_manager.py` (61) |
| Agent | `agent/simple.py` (Gemini VLM agent) |
| Server | `server/app.py` (FastAPI + mGBA) |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GEMINI_API_KEY not set" | `export GEMINI_API_KEY=your-key` |
| "No video recorded" | Use `--record` flag explicitly |
| Game stuck | Check `llm_logs/` for LLM interaction details |
| Need more context | View live stream at `http://127.0.0.1:8000/stream` |

## Expected Timeline

| Milestone | Real-World Time |
|-----------|----------------|
| Title → Starter | 5–10 min |
| Starter → Pokedex | 10–15 min |
| Pokedex → Rustboro | 20–30 min |
| First Gym | 30–45 min |
| All 8 Gyms | 8–12 hours |
| Elite Four | 1–2 hours |
| Full Game | 10–15 hours |

Each 60-minute session will save progress and write a journal entry for the next session to resume from.
