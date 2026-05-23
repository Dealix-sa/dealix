# CLAUDE.md — Dealix Project Manifest

Identity
- Project: Dealix — Saudi B2B Revenue Operating Company.
- Owner: founder (Sami).
- Stack: FastAPI backend (`api/`), Next.js 15 App Router frontend (`apps/web/`),
  policy/registry/eval YAML, Makefile + GitHub Actions, optional Postgres.
- Operating principle: AI prepares and recommends; humans approve every
  external/critical move. The founder runs the company from one internal
  Founder Console.

Never automatic (must be human-approved)
- Outbound sending (email, WhatsApp, LinkedIn, SMS).
- Pricing commits or proposal price changes.
- Contract, refund, or payment terms.
- Sensitive data exports (PDPL).
- Public client proof publishing.
- Destructive file/branch/data operations.

Required checks before declaring a change complete
- Python compile / pytest (where available).
- Frontend build: `npm --prefix apps/web run build`.
- Verifier scripts under `scripts/verify_*.py`.
- Master verifier: `python scripts/verify_ultimate_operating_layer.py`.

Coding rules
- Preserve existing architecture (`api/routers/`, `api/routers/domains/`,
  `apps/web/app/`).
- No secrets in repo. Use env vars and `.env.example`.
- No fake production claims. Source-tag fallback data with `source: "fallback"`.
- Every external-impact action must pass policy and write to the audit log.
- New systems must have: source of truth + verifier + docs + CI hook +
  trust boundary + audit path.

Trust gate (Policy-as-Code)
- File: `policies/dealix_control_policy.yaml`.
- Approval classes: A0 (info), A1 (internal draft), A2 (external after
  approval), A3 (banned automated).
- Rules: `no_a3_auto`, `no_suppressed_outreach`, `high_risk_requires_evidence`,
  `no_guaranteed_revenue_claims`, `approved_a2_can_request_execution`.

Agent registry
- File: `registries/agent_registry.yaml`.
- Every agent has `kill_switch: true`, `eval_required: true`,
  `external_action_allowed: false` unless explicitly A2-approved.
- No A3 agent may have `external_action_allowed: true`.

Eval gate
- File: `evals/gates/dealix_agent_eval_gate.yaml`.
- Suites: guaranteed-claims, approval-bypass, prompt-injection, sensitive-
  data-leakage, suppression-compliance, evidence-required, arabic-quality,
  proposal-safety, tool-misuse, A3-escalation.

Audit log
- Path: `${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv` (default
  `/opt/dealix-ops-private/trust/approval_decisions.csv`).
- Append-only. Every approve/reject/edit/escalate writes a row.

Private operating data
- Default root: `/opt/dealix-ops-private/` (overridable via env
  `DEALIX_PRIVATE_OPS`).
- Never commit private ops data. Bootstrap with:
  `make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private`.

Internal API authentication
- Env: `DEALIX_INTERNAL_TOKEN`.
- Header: `X-Dealix-Internal-Token`.
- If env unset, local dev allows requests but the auth gate logs a warning
  and refuses to mark the system production-ready.

How to run
```
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
make policy-check
make agent-registry
make eval-gate
make operating-scorecard PRIVATE_OPS=/opt/dealix-ops-private
make founder-console-v5
make control-plane-stage
make ultimate-operating-layer
make smoke-internal-api
npm --prefix apps/web run build
python scripts/verify_ultimate_operating_layer.py
```

Founder Console pages (must build)
- `/ceo`, `/sales-cockpit`, `/approvals`, `/workers`, `/trust`, `/finance`,
  `/distribution`, `/delivery`, `/retention`, `/proof`, `/control-plane`,
  `/audit`, `/evals`, `/product`, `/security`.

Frontend rule: all pages must build even when the API is offline. Fallback
data must be visibly tagged `source: "fallback"` and must never claim
production readiness.

Production readiness gates (see `docs/security/PRODUCTION_SECURITY_GATE.md`)
- `DEALIX_INTERNAL_TOKEN` set.
- No secrets in repo (gitleaks/detect-secrets).
- CI required checks green: policy, registry, eval, prompt safety,
  master verifier, frontend build.
- Branch protection on `main` matches `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`.

Where things live
- Backend internal router: `api/routers/internal/founder_console.py`.
- Internal helpers: `api/internal/runtime_reader.py`,
  `api/internal/auth.py`, `api/internal/policy_adapter.py`.
- Frontend shell: `apps/web/components/founder/founder-shell.tsx`.
- Runtime client: `apps/web/lib/dealix-runtime.ts`.
- Action client: `apps/web/lib/dealix-actions.ts`.
- Bootstrap script: `scripts/bootstrap_private_ops_runtime.py`.
- Master verifier: `scripts/verify_ultimate_operating_layer.py`.
- Smoke: `scripts/smoke_internal_api.py`.

Honesty rule
- Never claim production readiness unless all verifiers and the frontend
  build pass. State explicitly when something is fallback, mock, or
  manual-only.
