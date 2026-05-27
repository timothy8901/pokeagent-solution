# 🎮 Pokémon Emerald AI — Full Game Run (Title → Champion)

This directory contains a fully functional AI agent that plays **Pokémon Emerald** from the very beginning and defeats the Elite Four and Champion Wallace.

## What It Does

1. **Boots the game** from the title screen (no savestate needed)
2. **Sees the game** via Gemini 2.5 Flash vision model
3. **Makes decisions** every ~5-10 seconds (navigating, battling, interacting)
4. **Progresses through milestones** tracking full game completion
5. **Records video** of gameplay (optional)
6. **Saves state** every 10 steps for resuming
7. **Writes journal** to your Obsidian vault at the end of each session

## Quick Start

### 1. Set your Gemini API key

```bash
export GEMINI_API_KEY="AIzaSyBVmkcflA_uiJucUUh9eWxSt4mX8vXqCFI"
```

### 2. Run the AI for 1 hour, recording video

```bash
cd pokeagent-solution
python run_emerald_ai.py --record --session-minutes 60
```

That's it. The AI will:
- Start from the title screen
- Choose **Mudkip** as starter (guided by milestones)
- Play through Route 101, Oldale, Petalburg Woods
- Battle the Elite Four (Sidney → Phoebe → Glacia → Drake → Wallace)
- After 60 minutes: **auto-save**, **write journal** to your Obsidian vault, and quit

### 3. Resume later

```bash
python run_emerald_ai.py --resume --record --session-minutes 60
```

## File Locations

| Item | Path |
|------|------|
| Runner script | `pokeagent-solution/run_emerald_ai.py` |
| ROM | `pokeagent-solution/Emerald-GBAdvance/rom.gba` |
| Savestate | `pokeagent-solution/.pokeagent_cache/session_latest.state` |
| Video | `pokeagent-solution/pokegent_recording_*.mp4` |
| Journal | Your Obsidian vault directory |
| LLM logs | `pokeagent-solution/llm_logs/` |
| Milestone config | `pokeagent-solution/milestone_config.json` (65 milestones) |

## Progression Path

The milestone config tracks 65 checkpoints:

**Tutorial (0-15):** Title screen → starter selection → Route 101 → Oldale Town → get Pokédex

**Hoenn Gyms (15-200):** Petalburg (Brawly) → Rustboro (Roxane) → Dewford (Wattson) → Lavaridge (Flannery) → Pacifidlog (Norman) → Fortree (Winona) → Mossdeep (Tate & Liza) → Sootopolis (Juan)

**Elite Four & Champion (200+):** Sidney (Dark) → Phoebe (Ghost) → Glacia (Ice) → Drake (Dragon) → Wallace (Champion)

## Options

```
--record              Enable video recording to MP4
--resume              Resume from last savestate
--session-minutes N   Run for N minutes, then quit (default: 60)
--journal-dir PATH    Obsidian vault for journal (default: ~/Obsidian Vault)
--backend gemini      Use Google Gemini (default)
--backend openai      Use OpenAI API
--model gemini-2.5-flash  Gemini model name
--scaffold simple     Agent architecture (simple/react/fourmodule)
--headless            No display window
--port 8000           Server port
```

## How It Works

```
┌─────────────┐     HTTP/WS      ┌──────────────┐
│  Agent       │  ◄────────────►  │  Server      │
│  (Gemini VLM)│  State+Actions   │  (mGBA Emu)  │
│              │                  │              │
│ Sees frame   │  ← Screenshot    │  Emulates    │
│ Decides btn  │  → Action        │  Game logic  │
│ Generates    │                  │  Records     │
│ code         │                  │  Video       │
└─────────────┘                  └──────────────┘
        │                               │
        ▼                               ▼
  LLM API                        Savestates
  (Gemini)                       + Journal
```

The agent uses Google Gemini 2.5 Flash to:
1. **Perceive** the current game frame (what's on screen)
2. **Analyze** the game state (location, party, badges, etc.)
3. **Plan** the next action (move, battle, talk, pick up item)
4. **Execute** button inputs via the mGBA emulator
5. **Learn** from the result and iterate

## Expected Timelines

| Milestone | Approx. Time |
|-----------|-------------|
| Choose Mudkip | 5-10 min |
| Get Pokédex | 10-15 min |
| Petalburg Woods | 15-20 min |
| Rustboro City | 20-25 min |
| Stone Badge | 25-30 min |
| 8 Gyms total | 8-12 hours |
| Elite Four | 1-2 hours |
| Full game | 10-15 hours |

## Troubleshooting

- **"mgba not installed"** → The script auto-installs it in the project venv
- **"GEMINI_API_KEY not set"** → Export it first: `export GEMINI_API_KEY=your-key`
- **Game stuck** → The agent retries automatically; check `llm_logs/` for details
- **Video won't record** → Ensure OpenCV is installed in the venv

## Architecture

This uses the existing `pokeagent-solution` project:
- **Server**: FastAPI server + mGBA emulator (headless)
- **Client**: Python agent loop (1-second timestep)
- **VLM**: Google Gemini 2.5 Flash (vision)
- **Agent**: Simple scaffold (direct frame → action)
- **Memory**: Persistent milestone tracking + LLM context
- **Recorder**: OpenCV video writer (30 FPS MP4)
