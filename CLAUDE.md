# CLAUDE.md — Dealix Operating Guide for Claude

This file orients any Claude session working in this repo. Read it first.

## What Dealix is

A **governed operating layer** for revenue work. The canonical truth lives in
[`docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md`](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md).
If anything contradicts that file, that file wins.

**Operating equation:** Data + Workflow + AI + Human Approval + Governance +
Proof. Any missing column = a demo or a risk, not a product.

## The 6 non-negotiables (never violate)

1. **No scraping.** Data enters via `client_upload` / `crm_export` /
   `manual_entry` with a signed Source Passport.
2. **No cold WhatsApp / LinkedIn automation / bulk outreach.**
3. **No auto-send.** Every external message is a draft for founder approval
   (see [`docs/03_governance/HUMAN_APPROVAL_POLICY.md`](docs/03_governance/HUMAN_APPROVAL_POLICY.md)).
4. **No guaranteed revenue/sales.** Estimates use `~` + the disclaimer:
   "Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست
   نتائج مضمونة."
5. **No fake proof.** No name/logo/metric published without
   `consent_for_publication=True` per event **and** recorded founder approval.
6. **No agent without identity.** Named owner on both sides of every workflow.

Registered claims: [`docs/03_governance/CLAIMS_REGISTER.md`](docs/03_governance/CLAIMS_REGISTER.md).

## Launch gates (run before claiming "done")

```bash
python scripts/verify_dealix_positioning.py
python scripts/verify_dealix_module_status.py
python scripts/verify_dealix_growth_assets.py
python scripts/verify_dealix_launch_readiness.py
```

Verdict board: [`docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md`](docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md).
Slash command: `/dealix-launch-review`.

## Module honesty

Status of every module: [`docs/00_platform_truth/MODULE_STATUS_MAP.md`](docs/00_platform_truth/MODULE_STATUS_MAP.md),
grounded in [`docs/SERVICE_TRUTH_REPORT.md`](docs/SERVICE_TRUTH_REPORT.md).
Never present a PLANNED/ROADMAP/DEMO_FALLBACK module as LIVE.

## Delivery

- Sprint playbook: `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`
- Proof Pack template: `docs/04_delivery/PROOF_PACK_TEMPLATE.md`
- Customer folder template: `docs/04_delivery/CUSTOMER_FOLDER_TEMPLATE.md`

## Sub-agents

`.claude/agents/`: dealix-pm, dealix-delivery, dealix-sales, dealix-content,
dealix-engineer. None send external messages; all honor the non-negotiables.

## Build / test (when touching code)

- Python: `make lint`, `make test`, `make doctor` (env + alembic + security).
- Web: `cd frontend && npm ci && npm run build` (Next.js). Log build output to
  `reports/launch/npm_build.log` if it fails — record the cause, don't panic.

## House rules

- Proof before claim. Honesty over hype.
- Don't mark a future module as live. Don't invent metrics.
- When in doubt about an external-facing action, draft it and stop for approval.
