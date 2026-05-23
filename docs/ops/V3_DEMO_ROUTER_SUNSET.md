# v3 demo router sunset (internal)

## Current state

- [`api/routers/v3.py`](../../api/routers/v3.py) exposes `/api/v1/v3/*` with response header `X-Dealix-Deprecated: true`.
- These routes are **demo-only** and must not be used for external integrations.

## Production spine (keep and extend)

- Decision Passport: `/api/v1/decision-passport/*`
- Revenue OS catalog and gates: `/api/v1/revenue-os/*`
- Leads intake: `POST /api/v1/leads`
- Personal Operator: `/api/v1/personal-operator/*`
- Approvals: `/api/v1/approvals/*`
- Draft-first outreach: `/api/v1/gmail/*`, `/api/v1/linkedin/*` (via [`api/routers/drafts.py`](../../api/routers/drafts.py))

## Migration checklist for internal consumers

1. Replace `GET /api/v1/v3/command-center/snapshot` with Founder/Executive surfaces backed by `approval_center`, `revenue_os/catalog`, and `personal-operator/daily-brief`.
2. Replace any `GET /api/v1/v3/stack` usage with static docs plus `GET /api/v1/revenue-os/catalog`.
3. Track remaining callers via repo search for `/api/v1/v3` before deleting the router.

## Removal gate

- Zero references in `frontend/`, `api/`, and `tests/` to `/api/v1/v3/` outside `v3.py` itself.
- Smoke tests green for golden chain ([`tests/test_revenue_os_golden_chain_smoke.py`](../../tests/test_revenue_os_golden_chain_smoke.py)).

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
