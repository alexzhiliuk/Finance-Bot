# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack

- **Python 3.11+** managed with **uv** (no pip)
- **aiogram 3** — Telegram bot framework (async, router-based)
- **aiosqlite** — async SQLite access
- **OpenAI SDK** — Whisper (transcription) + GPT-4o-mini (expense parsing)

## Commands

```bash
# Install dependencies
uv sync

# Run the bot
uv run main.py

# Add a new dependency
uv add <package>
```

## Environment

Copy `.env.example` → `.env` and fill in:
- `BOT_TOKEN` — from @BotFather
- `OPENAI_API_KEY` — from OpenAI
- `ALLOWED_USER_IDS` — comma-separated Telegram user IDs (e.g. `123456789,987654321`). If empty, all users are allowed.

## Architecture

```
main.py               — entry point: wires Bot, Dispatcher, middleware, routers, calls init_db()
bot/
  config.py           — env vars + CATEGORIES dict + ALLOWED_USER_IDS set
  middlewares/auth.py — AuthMiddleware: drops updates from users not in ALLOWED_USER_IDS
  db/database.py      — all SQL (init_db, add_expense, get_monthly_expenses, get_recent_expenses, delete_expense)
  services/ai.py      — OpenAI: transcribe_voice() via Whisper, parse_expense_text() via GPT-4o-mini
  handlers/
    start.py          — /start, /help
    expenses.py       — /add (FSM), quick-add (plain number), category callbacks, /delN
    voice.py          — F.voice handler: download → Whisper → GPT → save
    reports.py        — /report (monthly), /history (last 10)
  keyboards/inline.py — categories_keyboard(), skip_keyboard()
  utils/formatters.py — fmt_expense_saved(), fmt_report(), fmt_history() (Russian locale)
```

## Key flows

**Voice message** → `voice.py` downloads OGG bytes → `ai.transcribe_voice()` → `ai.parse_expense_text()` returns `{amount, category, description}` or `{error}` → saved to DB.

**Text add** → plain number triggers `quick_add_amount` in `expenses.py` → FSM jumps to category state → inline keyboard → optional description → saved.

**`/add`** → full FSM: amount → category → description.

## Router order matters

In `main.py`, `voice.router` is included before `expenses.router` so that `F.voice` is matched before general message handlers.

## Categories

Defined in `bot/config.py` as `CATEGORIES: dict[str, str]` (key → emoji label). Keys are stored in the DB and used in GPT prompt. Add/rename categories there only.
