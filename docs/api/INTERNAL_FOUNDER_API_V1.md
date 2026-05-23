# Internal Founder API v1

## Purpose

Expose safe internal endpoints used by the Founder Console
(`apps/web/`). All endpoints are mounted under `/api/v1/internal/founder`
and gated by `require_super_admin` (see
`api/security/auth_deps.py:180`).

Phase 1 endpoints are **read-only**. They return placeholder JSON whose
shape matches the TypeScript types in `apps/web/lib/dealix-runtime.ts`.
Phase 2 of `docs/runtime/FOUNDER_CONSOLE_RUNTIME_BINDING_PLAN.md` wires
real data sources without changing the shape.

## Authentication

Every endpoint declares
`dependencies=[Depends(require_super_admin)]` on the router. A request
without a valid super-admin token returns `401`/`403`. The Founder
Console frontend swallows the error via `safeGet<T>` and renders a
fallback object — this is intentional during local browser dev.

To exercise the endpoints from a shell, supply a super-admin bearer
token issued by the existing auth flow:

```bash
curl -sS \
  -H "Authorization: Bearer $DEALIX_SUPER_ADMIN_TOKEN" \
  http://localhost:8000/api/v1/internal/founder/ceo/summary | jq .
```

## Endpoints

### CEO

`GET /api/v1/internal/founder/ceo/summary`

```json
{
  "top_action": "Approve or build first outreach batch",
  "status": "C3 Revenue Partial",
  "risk_flags": 0,
  "cash_collected_sar": 0,
  "approved_outreach": 0,
  "positive_replies": 0,
  "proposals_due": 0,
  "payment_followups_due": 0,
  "last_updated": "2026-05-23T00:00:00+00:00"
}
```

### Sales

`GET /api/v1/internal/founder/sales/funnel`

```json
{
  "lead_intelligence": 0,
  "a_leads": 0,
  "pending_approval": 0,
  "approved_outreach": 0,
  "sent": 0,
  "replies": 0,
  "positive_replies": 0,
  "samples": 0,
  "proposals": 0,
  "payment_capture": 0
}
```

### Approvals

`GET /api/v1/internal/founder/approvals` → `ApprovalItem[]`

```json
[
  {
    "id": "apt-100",
    "type": "whatsapp.send_message",
    "company": "Sample Co",
    "approval_class": "A2",
    "risk_level": "Medium",
    "summary": "Outbound WhatsApp draft awaiting approval",
    "evidence": null,
    "recommended_action": null,
    "status": "Pending"
  }
]
```

### Workers

`GET /api/v1/internal/founder/workers/health` → `WorkerHealth[]`

```json
[
  {
    "name": "lead-acquisition",
    "status": "idle",
    "last_run": null,
    "backlog": 0,
    "failures_24h": 0
  }
]
```

### Trust

`GET /api/v1/internal/founder/trust/flags` → `TrustFlag[]`

```json
[]
```

### Finance

`GET /api/v1/internal/founder/finance/summary`

```json
{
  "cash_collected_sar": 0,
  "mrr_sar": 0,
  "pipeline_sar": 0,
  "weighted_pipeline_sar": 0,
  "payment_followups_due": 0
}
```

### Distribution

`GET /api/v1/internal/founder/distribution/summary`

```json
{
  "channels": 0,
  "active_sectors": 0,
  "experiments": 0,
  "double_down": null
}
```

## Rules

- Internal endpoints require authentication (`require_super_admin`).
- External-impact actions require policy evaluation. None exist in v1.
- A2 and A3 actions require explicit approval (Phase 3, wired to the
  existing `ApprovalCenter` in `dealix/trust/`).
- No approval endpoint can bypass the Trust Plane.
- v1 responses are placeholder JSON. Phase 2 swaps the placeholders for
  real data from `founder_dashboard_router`, `execution_assurance.health`,
  `data/demo/saudi_b2b_demo.csv`, and the production database.
