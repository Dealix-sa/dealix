# Dealix — Context for Claude

> **Read `AGENTS.md` first.** It is the authoritative repo guide: local dev
> commands, repo anatomy, the canonical module map, and "resolved — do not
> re-diagnose" operational notes. This file is only a lean lookup table.

## Stack
Python 3.11 · FastAPI · PostgreSQL (Supabase) · Next.js · Railway deployment

## Rules
1. Async/await everywhere in Python. No sync blocking calls in request paths.
2. Arabic-first content (العربية أولاً), bilingual UI. SAR currency only.
3. Make small, safe, requested changes. Prefer fixing existing code over adding.
4. Never enable auto external sends (WhatsApp / LinkedIn / email) in any env.
5. Tests live in `tests/`. Run only when the user asks.

## Doctrine guards (non-negotiables — must always pass, never disable)
`tests/test_no_cold_whatsapp.py` · `tests/test_no_linkedin_automation.py` ·
`tests/test_no_scraping_engine.py` · `tests/test_no_guaranteed_claims.py` ·
`tests/test_no_source_no_answer.py` · `tests/test_no_pii_in_logs.py`.
If one fails, fix the root cause — never bypass a guard.

## Key files
- `AGENTS.md` — source of truth for commands, anatomy, agent orchestration.
- `api/routers/` — 120+ FastAPI routers (thin I/O; logic lives in modules).
- `core/config/` — env vars & settings.

## Commands
```bash
APP_ENV=test pytest -v        # full suite (~15-20 min); see AGENTS.md for the quick bundle
ruff check . && black --check .   # lint (or: make lint)
make run                      # run API server (dev, reload)
alembic upgrade head          # migrations (single head enforced in CI)
```

## Skills (load on demand)
- `@token-optimizer/02-claude-md/skills/api.md` — API conventions (120+ routers)
- `@token-optimizer/02-claude-md/skills/database.md` — DB schema & patterns
- `@token-optimizer/02-claude-md/skills/commercial.md` — commercial chain (diagnostic→pilot→proof→payment→upsell)
- `@token-optimizer/02-claude-md/skills/frontend.md` — frontend patterns
- `@token-optimizer/02-claude-md/skills/testing.md` — test conventions
- `@token-optimizer/02-claude-md/skills/deployment.md` — deploy procedures
