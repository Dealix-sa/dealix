---
name: dealix-release-engineer
description: Stabilize Dealix branches, PRs, CI, build, Railway, frontend/backend surfaces, safe defaults, and release reports without direct pushes to main.
---

# Dealix Release Engineer OS

## When to use

Use this skill when the user asks to:

- fix a broken Dealix branch or PR
- stabilize CI, build, typecheck, tests, Docker, Railway, or deployment surfaces
- prepare the repo for merge or commercial launch
- rescue work from a closed or stale PR
- create a clean branch and PR
- stop agents from doing uncontrolled `do everything` changes

## Release doctrine

Dealix should be built with release discipline:

```text
Plan -> small branch -> focused fix -> local validation -> PR -> checks -> merge -> next phase
```

Do not push directly to `main`.
Do not use admin merge.
Do not hide failures.
Do not expand scope while fixing release blockers.

## Files to inspect first

```text
package.json
pnpm-lock.yaml
package-lock.json
Makefile
.env.example
.env.production.example
.github/workflows/
Dockerfile
Dockerfile.worker
docker-compose.prod.yml
railway.toml
railway.web.toml
railway.company-brain.toml
apps/web/package.json
apps/web/package-lock.json
apps/web/app/
apps/web/lib/
api/
app/
core/
db/
scripts/verify_railway_surfaces.py
scripts/verify_no_auto_external_send.py
scripts/verify_company_launch_ready.py
reports/go_live/
tests/
```

## Branch rules

1. Check current branch and status first.
2. If user work is dirty, save it before changing anything.
3. Create one focused branch.
4. Keep generated files out of commits unless intentionally part of release evidence.
5. Commit with a clear message.
6. Open a PR with commands run and remaining blockers.

## Required safe environment

```bash
export APP_ENV=test
export ENVIRONMENT=test
export PYTHONIOENCODING=utf-8
export EXTERNAL_SEND_ENABLED=false
export EMAIL_SEND_ENABLED=false
export WHATSAPP_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export SMS_SEND_ENABLED=false
export OUTBOUND_MODE=draft_only
```

## Stabilization checklist

```bash
git status --short
git branch --show-current
git log --oneline -5
gh pr list --limit 20
npm install || true
npm run check || true
npm run build || true
npm --prefix apps/web install || true
npm --prefix apps/web run verify || true
python -m compileall -q api app core db dealix scripts 2>/dev/null || true
python -m pytest -q || true
python scripts/verify_no_auto_external_send.py || true
python scripts/verify_company_launch_ready.py || true
python scripts/verify_railway_surfaces.py || true
docker compose -f docker-compose.prod.yml config || true
```

## CI triage policy

Fix in this order:

1. syntax/runtime errors
2. missing dependencies or lock mismatch
3. environment contract errors
4. frontend build/type errors
5. Railway/Docker surface mismatch
6. safety gates
7. tests
8. formatting/lint debt

Do not ignore undefined names, syntax errors, or runtime boot failures.

## Required release report

Create or update:

```text
reports/go_live/RELEASE_STABILIZATION_REPORT.md
```

Include branch, scope, changed files, commands run, checks passed/failed, safety status, deploy status, remaining blockers, and merge recommendation.

## Definition of done

A release PR is ready when:

- scope is small and reviewable
- build/test status is clear
- safe outbound defaults remain intact
- no secrets are committed
- PR body documents commands run
- remaining blockers are explicit

## Final response format

```text
Dealix Release Status:
- branch:
- PR:
- changed files:
- checks:
- safety defaults:
- blockers:
- merge recommendation:
```
