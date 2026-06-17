---
name: run-launch-gates
description: Run the Dealix launch verification gates and report a GREEN/RED verdict with real output. Use before recommending any PR for merge or making a Go/No-Go call. Never hides failures, never claims green without evidence, never uses npm test (it does not exist).
---

# Skill: run-launch-gates

## When to use
Before recommending a PR for merge, or for a Go/No-Go decision.

## Commands (run, show real output)
```
cd frontend && npm ci && npm run lint && npm run typecheck && npm run build
make env-check
python scripts/security_smoke.py
python scripts/verify_website_positioning.py   # available after PR7
python scripts/verify_growth_assets.py         # available after PR7
python scripts/verify_launch_readiness.py      # available after PR7
git diff --stat
```

## Rules
- No `npm test` (does not exist). JS = build+lint+typecheck.
- Known `security-smoke` false positives (`.env.*.example`, fixtures) — note them, don't delete fixtures.
- For the launch gate itself, also prove it FAILS on an injected violation.

## Output
GREEN/RED verdict, each command's result, `git diff --stat`, and blockers if RED.
