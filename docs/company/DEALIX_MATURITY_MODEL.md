# Dealix Maturity Model

## Stages

- **Stage 0 — Manual.** No AI agents. Spreadsheets.
- **Stage 1 — Scripted.** A few CLIs but no trust gate.
- **Stage 2 — Founder Console + Audit.** Internal API, approvals,
  audit log. (Current target.)
- **Stage 3 — CI-Enforced Trust.** Policy / registry / eval verifiers
  required on every PR. Branch protection enabled.
- **Stage 4 — Postgres + Event-Sourced Audit.** Approval decisions are
  events with a hash chain.
- **Stage 5 — External-Facing AI Workforce.** Sending workers exist but
  every send remains policy-checked and reversible.

## How to know you're at a stage

| Check | Stage |
|---|---|
| `scripts/verify_ultimate_operating_layer.py` passes | ≥ 2 |
| `npm --prefix apps/web run build` passes | ≥ 2 |
| `.github/workflows/dealix-ultimate-operating-layer.yml` is required | ≥ 3 |
| Postgres tables exist and are read by the API | ≥ 4 |
| Send-capable workers exist with policy + kill switch | ≥ 5 |
