# Dealix Implementation Audit

What landed in the Production AI Certification Layer commit, and how
it maps to the spec.

## Files added (or rewritten)

### Policies, registries, evals (declarative)

- `policies/dealix_control_policy.yaml` — approval classes + 10 rules
  including 6 immutable rule ids.
- `registries/agent_registry.yaml` — 8 declared agents (CEO copilot,
  capital allocator, revenue forecaster, outreach drafter, outreach
  executor, market attack planner, AI governance auditor, company
  memory curator).
- `registries/machine_registry.yaml` — 6 scheduled machines, none
  external-action.
- `registries/integration_registry.yaml` — 7 integrations
  (WhatsApp, Email, Moyasar, HubSpot, Google Search, Groq LLM,
  PostHog), all server-only, kill switches named.
- `evals/gates/dealix_agent_eval_gate.yaml` — global thresholds +
  per-agent suites pointing at existing `evals/*.yaml|jsonl` cases.

### Verifier scripts (the gate)

- `scripts/_dealix_cert_common.py` — shared report model + safe YAML
  loader + UTF-8 stdout.
- `scripts/verify_policy_as_code.py`
- `scripts/verify_agent_registry.py`
- `scripts/verify_machine_registry.py`
- `scripts/verify_eval_gate.py`
- `scripts/verify_prompt_output_quality.py`
- `scripts/verify_live_send_safety.py`
- `scripts/verify_railway_readiness.py`
- `scripts/verify_production_env.py`
- `scripts/verify_ai_company_os.py`
- `scripts/verify_everything.py` — master roll-up
- `scripts/smoke_internal_api.py` — offline + online (BASE_URL) smoke

### Generators (private_ops-driven, never send)

- `scripts/_private_ops_runtime.py`
- `scripts/bootstrap_private_ops_runtime.py`
- `scripts/generate_ceo_daily_brief.py`
- `scripts/generate_capital_allocation_report.py`
- `scripts/generate_strategy_scorecard.py`
- `scripts/generate_revenue_forecast.py`
- `scripts/generate_company_memory_report.py`

### Internal API scaffold

- `api/internal/__init__.py`
- `api/internal/auth.py` — `X-Dealix-Internal-Token` gate, constant-time
  compare, never logs the token, returns 401/403/500 with no value
  echoed.
- `api/internal/runtime_reader.py` — read-only views over private_ops,
  path-traversal guard.
- `api/internal/policy_adapter.py` — `decide(PolicyContext)` returning
  one of `ALLOW | ALLOW_AFTER_APPROVAL | REQUIRE_EVIDENCE | ESCALATE |
  DENY`, with rule precedence (DENY beats ESCALATE beats ...).
- `api/internal/audit_writer.py` — append-only JSON lines, secret
  scrub on key names matching `TOKEN|SECRET|API_KEY|...`.
- `api/internal/integration_gate.py` — the only path external sends
  may take.
- `api/routers/internal/__init__.py`
- `api/routers/internal/founder_console.py` — four endpoints (CEO
  summary, approvals queue, finance forecast, trust incidents).

### Makefile additions

`policy-check`, `agent-registry-check`, `machine-registry-check`,
`eval-gate-check`, `prompt-output-check`, `live-send-safety`,
`railway-readiness`, `production-env-check`, `ai-company-os`,
`everything`, `production-certification`, `internal-api-smoke`,
`ceo-daily-brief`, `capital-allocation`, `strategy-scorecard`,
`revenue-forecast`, `company-memory`.

### CI

- `.github/workflows/dealix-production-certification.yml` — runs every
  verifier on `push` to `main` and `claude/**`, plus PRs into `main`.
  Also includes a `frontend-build` job (skipped if `apps/web/package.json`
  is absent).

### Docs

- `docs/ops/DEALIX_FINAL_READINESS_REPORT.md`
- `docs/ops/DEALIX_MISSING_SYSTEMS.md`
- `docs/ops/DEALIX_IMPLEMENTATION_AUDIT.md` (this file)
- `docs/railway/RAILWAY_PRODUCTION_DEPLOYMENT.md`
- `docs/security/RAILWAY_SECRET_HANDLING.md`
- `docs/security/LIVE_INTEGRATION_KILL_SWITCHES.md`
- `docs/trust/LIVE_SEND_SAFETY_GATE.md`
- `docs/trust/WHATSAPP_APPROVAL_GATE.md`
- `docs/trust/EMAIL_APPROVAL_GATE.md`

## Files that exist in the spec but were intentionally NOT built

- 19 Founder Console pages (`apps/web/app/<slug>/page.tsx`). Tracked
  as WARN in `verify_ai_company_os.py` and listed in
  `docs/ops/DEALIX_MISSING_SYSTEMS.md`.
- Brand component pack (`apps/web/components/brand/*`,
  `apps/web/lib/dealix-runtime.ts`). Premature without the pages.
- LLM eval runner. Declared in the gate yaml; runner script not yet
  written.

## What does NOT change

- The existing 130+ routers under `api/routers/*` are untouched. The
  new internal scaffold lives at `api/routers/internal/` to avoid
  collision.
- The existing `Makefile` v5 / v10 sections are untouched.
- No existing CI workflow is removed.

## Verification

```bash
# Bootstrap a CI-style private_ops for local testing
python scripts/bootstrap_private_ops_runtime.py \
  --private-ops /tmp/dealix-private-ops-ci

DEALIX_PRIVATE_OPS=/tmp/dealix-private-ops-ci \
  python scripts/verify_everything.py
```

Expected on a fresh checkout: PASS with WARN entries for the Founder
Console punch list and any unbootstrapped private_ops sections.
