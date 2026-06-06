# CLAUDE.md — Dealix

Project-specific instructions for Claude Code (CLI, GitHub Action, and IDE).
For the full repo map, local-dev commands, and "do not re-diagnose" notes,
read **`AGENTS.md` first** — this file only adds Claude-specific priorities and
review standards. Do not duplicate `AGENTS.md`; link to it.

Dealix is an AI-native business operating system for Saudi companies: revenue
operations, WhatsApp workflows, sales follow-up, proposal automation, CRM
intelligence, and CEO dashboards. Stack is **Python / FastAPI** (backend) with a
**Next.js** frontend under `frontend/`.

## Priorities

1. Do not break production behavior.
2. Prefer small, reviewable pull requests over large rewrites.
3. Never expose secrets, tokens, customer data, or private keys.
4. Run the relevant checks before claiming completion — or clearly state what
   was not run and why.
5. Explain every risky change before editing.

## Required checks

This repo is Python-first and uses a `Makefile`, not `npm`, at the root. Before
finalizing a code change, run whichever apply (and exist) for the area you
touched:

```bash
make test            # full pytest suite with coverage
make lint            # ruff + black checks
make type-check      # mypy
make env-check       # validate .env.example contract + duplicate keys
make security-smoke  # dependency-free repo security smoke checks
make doctor          # env-check + single alembic head + security smoke
```

Lower-level equivalents if `make` is unavailable:

```bash
pytest
python scripts/check_env_contract.py
```

Frontend changes (`frontend/`) use npm in that directory:

```bash
cd frontend && npm test && npm run lint && npm run build
```

If a check can't run in the current environment, say so explicitly instead of
implying it passed.

## Review standards

Flag issues by severity:

- **P0** — security, secret/data leak, broken auth, production outage.
- **P1** — payment (Moyasar/ZATCA), CRM, webhook, WhatsApp, or deployment
  (Railway / GitHub Actions) risk.
- **P2** — maintainability, test coverage, or UX improvement.

When reviewing, verify GitHub Actions workflows, Railway deployment assumptions,
and the environment-variable contract (`.env.example` ↔ `make env-check`).

## Do not

- Do not commit secrets, tokens, private keys, or `.env*` files.
- Do not remove tests without an equivalent replacement.
- Do not disable CI to make a PR pass.
- Do not delete business docs or ledgers without explicit instruction.
- Do not rewrite large architecture without an agreed execution plan.
- Do not change deployment, secret, or production config unless explicitly asked.
