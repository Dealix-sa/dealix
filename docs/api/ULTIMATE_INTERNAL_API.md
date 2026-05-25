# Ultimate Internal API

> The contract between the Founder Console (and any internal tool) and the rest of Dealix.
> Every endpoint here is **authenticated, audited, and trust-gated**.

---

## 1. Conventions

- **Base path:** `/api/v1/internal`
- **Auth:** Bearer token (founder JWT). Anonymous calls → `401`.
- **Authorization:** Founder role required by default. Endpoints that downgrade to "trusted operator" are explicitly marked.
- **Audit:** Every state-changing endpoint (`POST/PATCH/DELETE`) writes to `audit_events`.
- **Trust gate:** Every external-impact endpoint calls `POST /trust/evaluate` internally before acting; if denied, the endpoint returns `409 Conflict` with the policy result.
- **Idempotency:** State-changing endpoints accept an `Idempotency-Key` header.
- **Pagination:** Cursor-based: `?cursor=&limit=` (default 50, max 200).
- **Errors:** RFC 7807 problem+json: `{ type, title, status, detail, instance, trace_id }`.
- **Tracing:** Every response sets `X-Trace-Id`. Use it to correlate with `audit_events`.

---

## 2. Founder (`/ceo`)

### `GET /api/v1/internal/ceo/summary`
One-screen view for the CEO page.

Response:
```json
{
  "company_score": 73,
  "bottleneck": "approval_latency",
  "highest_risk": { "kind": "stale_worker", "subject": "lead-discovery", "severity": "amber" },
  "cash_collected_mtd_sar": 12500,
  "projected_cash_30d_sar": 28000,
  "computed_at": "2026-05-23T07:00:00+03:00",
  "source": "live"
}
```

### `GET /api/v1/internal/ceo/top-action`
The single most important thing to do right now.

Response:
```json
{
  "summary": "Approve 7 outreach drafts for AlRajhi sector",
  "url": "/approvals?filter=alrajhi",
  "severity": "amber",
  "computed_at": "2026-05-23T07:00:00+03:00"
}
```

### `GET /api/v1/internal/ceo/company-score`
Sub-scores for the company-score number.

Response:
```json
{
  "overall": 73,
  "components": {
    "revenue_factory": 60,
    "trust": 90,
    "delivery": 80,
    "workers": 70,
    "finance": 65
  },
  "worst": "revenue_factory"
}
```

---

## 3. Sales (`/sales-cockpit`)

### `GET /api/v1/internal/sales/funnel`
Funnel counts per stage for the current week (configurable via `?period=`).

Response:
```json
{
  "period": "week",
  "stages": [
    { "stage": "lead_intelligence", "count": 412 },
    { "stage": "outreach_drafted",  "count": 88 },
    { "stage": "outreach_sent",     "count": 51 },
    { "stage": "replies",           "count": 6 },
    { "stage": "samples",           "count": 3 },
    { "stage": "proposals",         "count": 2 },
    { "stage": "payments",          "count": 1 }
  ]
}
```

### `GET /api/v1/internal/sales/bottleneck`
The single weakest conversion in the funnel this week.

Response:
```json
{
  "from": "outreach_sent",
  "to": "replies",
  "rate": 0.117,
  "benchmark": 0.20,
  "recommendation": "Refresh outreach drafts for sector AlRajhi"
}
```

### `GET /api/v1/internal/sales/payment-capture`
Every proposal awaiting payment.

Response:
```json
{
  "items": [
    {
      "proposal_id": "p_001",
      "client": "Acme",
      "amount_sar": 4999,
      "sent_at": "2026-05-15T09:00:00+03:00",
      "days_since_sent": 8,
      "last_followup_at": "2026-05-21T09:00:00+03:00",
      "next_followup_due": "2026-05-24T09:00:00+03:00"
    }
  ]
}
```

---

## 4. Approvals (`/approvals`)

### `GET /api/v1/internal/approvals`
Pending decisions, sorted by `urgency × class`.

Response:
```json
{
  "items": [
    {
      "id": "ap_001",
      "class": "A2",
      "summary": "Send outreach to 7 contacts at AlRajhi",
      "policy_result": { "decision": "ALLOWED_WITH_APPROVAL", "checks": ["suppression_ok", "no_overclaim_ok"] },
      "evidence_url": "/audit/ap_001/evidence",
      "age_minutes": 42,
      "created_at": "2026-05-23T06:18:00+03:00"
    }
  ]
}
```

### `POST /api/v1/internal/approvals/{id}/approve`
Body:
```json
{ "note": "Reviewed batch; tone is correct." }
```
Effects:
- Writes `approval_decisions` row with `decision=approved`.
- Writes `audit_events` row.
- Enqueues the downstream action (send / sample / proposal / payment).

### `POST /api/v1/internal/approvals/{id}/reject`
Body: `{ "reason": "Wrong sector framing" }`
Writes audit; downstream action is canceled.

### `POST /api/v1/internal/approvals/{id}/request-edit`
Body: `{ "edits": "Tighten the second paragraph; remove KPIs claim." }`
Writes audit; the originating worker re-runs the draft with the edit instruction.

### `POST /api/v1/internal/approvals/{id}/escalate`
Body: `{ "to": "trust_review" }`
Writes audit; routes the item to the Trust Center queue (`/trust`).

---

## 5. Workers (`/workers`)

### `GET /api/v1/internal/workers/health`
Response:
```json
{
  "items": [
    {
      "worker_id": "lead-discovery",
      "owner": "revenue-ops",
      "schedule": "0 6 * * *",
      "last_run": "2026-05-23T03:00:00+00:00",
      "status": "ok",
      "failures_24h": 0,
      "backlog": 0,
      "disable_switch": false
    }
  ],
  "overall_score": 92
}
```

### `GET /api/v1/internal/workers/failures`
Failed worker runs in the last 24h.

Response:
```json
{
  "items": [
    {
      "worker_id": "outreach-draft",
      "run_id": "r_8821",
      "failed_at": "2026-05-23T02:14:00+00:00",
      "error": "ProviderTimeout: model call exceeded 30s",
      "retryable": true
    }
  ]
}
```

### `POST /api/v1/internal/workers/{id}/retry`
Body: `{ "run_id": "r_8821" }` (optional; if omitted, retries the most recent failure).
Effects: enqueues a retry; writes audit.

---

## 6. Trust (`/trust`)

### `GET /api/v1/internal/trust/flags`
Response:
```json
{
  "items": [
    {
      "kind": "suppression_violation_attempt",
      "subject": "contact:c_4421",
      "severity": "red",
      "opened_at": "2026-05-23T02:00:00+03:00",
      "owner": "trust"
    }
  ]
}
```

### `POST /api/v1/internal/trust/evaluate`
Evaluate an action against the trust plane (called by other endpoints; exposed for manual checks).

Body:
```json
{
  "action": "outreach_send",
  "subject": { "contact_id": "c_4421" },
  "payload_digest": "sha256:…",
  "actor": "founder",
  "evidence": { "draft_id": "d_99" }
}
```

Response:
```json
{
  "decision": "ALLOWED" | "ALLOWED_WITH_APPROVAL" | "DENIED",
  "class": "A0|A1|A2|A3",
  "checks": [
    { "name": "suppression", "result": "pass" },
    { "name": "no_overclaim", "result": "pass" },
    { "name": "approval_required", "result": "needs_approval" }
  ],
  "reason": "External contact requires founder approval"
}
```

### `GET /api/v1/internal/trust/incidents`
Open and recently-closed incidents.

---

## 7. Finance (`/finance`)

### `GET /api/v1/internal/finance/summary`
Response:
```json
{
  "cash_collected_mtd_sar": 12500,
  "mrr_sar": 4999,
  "pipeline_sar": 78000,
  "weighted_pipeline_sar": 32450,
  "gross_margin_pct": 68
}
```

### `GET /api/v1/internal/finance/unit-economics`
Response:
```json
{
  "ai_cost_sar_per_proposal": 14.20,
  "tool_cost_sar_per_proposal": 3.10,
  "founder_hours_per_proposal": 1.5,
  "revenue_sar_per_proposal": 4999,
  "contribution_margin_pct": 92
}
```

### `GET /api/v1/internal/finance/runway`
Response:
```json
{
  "cash_on_hand_sar": 42000,
  "burn_sar_per_month": 8000,
  "runway_months": 5.25
}
```

---

## 8. Delivery (`/delivery`)

### `GET /api/v1/internal/delivery/queue`
Response:
```json
{
  "items": [
    {
      "client": "acme",
      "start_date": "2026-05-20",
      "stage": "delivery_in_progress",
      "qa_status": "pending",
      "next_milestone": "QA review by 2026-05-25"
    }
  ]
}
```

### `POST /api/v1/internal/delivery/{client}/start`
Starts a delivery workspace. Creates `clients/{client}/intake.md` and seeds the delivery plan.

### `POST /api/v1/internal/delivery/{client}/qa`
Body: `{ "pass": true, "notes": "Clean. Ready for handoff." }`
Writes QA record; gates handoff.

---

## 9. Product (`/product`)

### `GET /api/v1/internal/product/usage`
Per-feature usage counts.

### `GET /api/v1/internal/product/repeated-workflows`
Workflows used by ≥2 paid customers — productization candidates.

---

## 10. Audit (`/audit`)

### `GET /api/v1/internal/audit/approvals`
Response:
```json
{
  "items": [
    {
      "id": "ad_001",
      "approval_id": "ap_001",
      "actor": "founder",
      "decision": "approved",
      "class": "A2",
      "timestamp": "2026-05-23T07:01:00+03:00",
      "payload_digest": "sha256:…",
      "trace_id": "tr_…"
    }
  ]
}
```

### `GET /api/v1/internal/audit/actions`
Every external-impact action that left the building.

Response:
```json
{
  "items": [
    {
      "id": "act_001",
      "action": "outreach_send",
      "subject": "contact:c_4421",
      "actor": "worker:outreach-send",
      "approval_id": "ap_001",
      "timestamp": "2026-05-23T07:02:00+03:00",
      "result": "delivered",
      "trace_id": "tr_…"
    }
  ]
}
```

---

## 11. Cross-cutting

### 11.1 Errors

```json
{
  "type": "https://dealix/errors/trust-denied",
  "title": "Trust gate denied the action",
  "status": 409,
  "detail": "Contact is on the suppression list",
  "instance": "/api/v1/internal/approvals/ap_001/approve",
  "trace_id": "tr_…"
}
```

### 11.2 Rate limits
- Read endpoints: 600/min per actor.
- State-changing endpoints: 60/min per actor.
- `/trust/evaluate`: 1200/min (called by many other endpoints).

### 11.3 Versioning
- `v1` is stable for the entire L0–L5 lifecycle.
- Breaking changes ship under `v2` with a parallel surface; `v1` continues for 90 days.

### 11.4 Observability
- Every request emits a structured log entry: `actor`, `endpoint`, `trace_id`, `status`, `duration_ms`, `trust_decision`.
- Every state-changing request adds an `audit_event_id`.

---

## 12. Rule

> **Internal APIs are authenticated, audited, and trust-gated.**

No internal endpoint is allowed to bypass any of the three. A "private" or "admin" endpoint that is not in this document does not exist.
