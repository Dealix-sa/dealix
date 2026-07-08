# Implementation Note — Money Now + Autonomous Growth Foundation

Branch: `claude/money-now-autonomous-growth-qiu1ex`
Mode: draft-only, approval-first. No live outbound. No secrets. No production changes.

## Discovery findings

- **Railway config is already aligned and stable.** `railway.toml` / `railway.json`
  already use `builder = DOCKERFILE`, `dockerfilePath = Dockerfile`, a guarded
  `preDeployCommand`, `healthcheckPath = /healthz`, `healthcheckTimeout = 300`,
  `restartPolicyType = ON_FAILURE`, `numReplicas = 1`. The repo-canonical rule
  (`CLAUDE.md`, `.claude/rules/dealix-railway.md`) explicitly requires the
  `uvicorn api.main:app` start command, so we deliberately did **not** override the
  runtime or churn this file — changing a working, canonical config would risk the
  production stability we are trying to protect. `/healthz` route exists
  (`api/routers/platform_meta.py`) and returns `{"status":"ok"}`.
  - The only deviation from the master prompt's suggested values is
    `restartPolicyMaxRetries = 10` (prompt suggested 3). The repo value is already
    production-safe; we left it as the repo canonical.

- Existing systems reused rather than rebuilt: `autonomous_growth/`,
  `dealix/business_now/`, `scripts/commercial/*`. This work adds a thin,
  dependency-light execution/registry layer on top; it does not replace them.

## What this change adds (net-new, no rebuild)

1. `dealix/strategy_execution/` — internal draft-only execution engine
   (registry, planner, safety gate, action/approval queues, proof logger,
   learning loop, model router, growth engine, orchestrator). Level 5 (external
   send / publish / payments / production change) is **blocked by default and
   not implemented**.
2. `dealix/strategy_execution/strategies/*.yaml` — 13 strategy definitions.
3. `scripts/commercial/run_money_now_sprint.py` + `verify_money_now_sprint.py`
   — first-revenue founder action plan + evidence-chain verification.
4. `scripts/commercial/run_autonomous_growth_daily.py` +
   `verify_autonomous_growth.py` — daily draft-only internal run.
5. `scripts/commercial/verify_launch_foundation.py` — one-shot foundation check.
6. `.github/workflows/dealix-autonomous-growth-daily.yml` — scheduled draft-only
   internal run (no secrets, no send, no deploy, concurrency-guarded).
7. Docs under `docs/commercial/`.

## Safety posture

- Revenue is only recognized when a `payment_received` evidence event exists.
- Every external-facing action is routed to an approval queue, never executed.
- No live charge, no auto-send, no public model endpoints, no fake proof.
- All generated artifacts are internal reports/drafts under `reports/`.
