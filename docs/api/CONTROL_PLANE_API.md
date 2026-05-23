# Control Plane API — واجهة لوحة التحكم

Status: v1
Owner: Founder
Auth: `X-Internal-Token` required on every call. See Internal API Auth Gate.

## 1. Purpose — الغرض

The Control Plane API is the read API that powers the Founder Console and any internal observer.
It returns the current state of policies, agents, scorecards, and risks in one shape per page.

واجهة لوحة التحكم هي واجهة القراءة التي تُغذّي لوحة المؤسس وأي مراقب داخلي.
ترجع الحالة الحالية للسياسات، الوكلاء، البطاقة، والمخاطر بشكل موحد لكل صفحة.

## 2. Base — الأساس

- Base path: `/api/v1/internal/control/`
- Auth header: `X-Internal-Token: <token>`
- Content type: `application/json; charset=utf-8`
- All endpoints are read-only.

## 3. Endpoints — النقاط

### 3.1 `GET /api/v1/internal/control/summary`
The "Today" briefing source.

Response shape:
```json
{
  "company": { "stage": "AI-governed", "stage_progress_pct": 62 },
  "queue": { "a2_open": 7, "a3_open": 1 },
  "agents": { "enabled": 9, "disabled": 1, "in_eval": 0 },
  "evals": { "gate": "green", "last_run": "2026-05-23T07:10:00Z" },
  "workers": { "fresh": 12, "stale": 1, "down": 0 },
  "ai_cost_24h_sar": 38.50,
  "risks_open": 3,
  "last_audit_entry_at": "2026-05-23T07:42:01Z",
  "stale": false
}
```

### 3.2 `GET /api/v1/internal/control/policies`
Returns the current policy version and a redacted preview.
```json
{
  "version": "2026.05.23-1",
  "hash": "sha256:...",
  "loaded_at": "2026-05-23T06:00:00Z",
  "rule_count": 84,
  "rules_preview": [
    { "id": "no_external_send", "severity": "P0" },
    { "id": "no_pricing_commit", "severity": "P0" }
  ]
}
```

### 3.3 `GET /api/v1/internal/control/agents`
Joins the agent registry with current runtime state.
```json
{
  "agents": [
    {
      "id": "revenue_outreach_drafter",
      "name": "Revenue Outreach Drafter",
      "approval_class_max": "A2",
      "enabled": true,
      "last_run_at": "2026-05-23T07:32:10Z",
      "last_eval_state": "green",
      "kill_switch": "flags.agents.revenue_outreach_drafter.enabled",
      "data_access_level": "internal",
      "owner": "founder@dealix.sa"
    }
  ]
}
```

### 3.4 `GET /api/v1/internal/control/scorecard`
The maturity + DORA + AI cost view.
```json
{
  "maturity": { "stage": "AI-governed", "next": "Sovereign", "progress_pct": 62 },
  "dora": {
    "deployment_frequency_per_week": 4.2,
    "lead_time_for_changes_hours": 6.3,
    "change_failure_rate_pct": 5.0,
    "mttr_minutes": 22
  },
  "ai_cost": { "last_24h_sar": 38.50, "last_7d_sar": 254.30 },
  "audit_completeness_pct": 100.0,
  "worker_freshness_pct": 92.3
}
```

### 3.5 `GET /api/v1/internal/control/risks`
Open risks tracked by Trust Guardian and the founder.
```json
{
  "risks": [
    {
      "id": "risk_2026_05_001",
      "title": "Worker freshness below SLO on intelligence_collector",
      "severity": "P2",
      "owner": "founder@dealix.sa",
      "opened_at": "2026-05-22T19:11:00Z",
      "status": "open"
    }
  ]
}
```

## 4. Errors — الأخطاء

| Code | When |
|---|---|
| 401 | Missing or invalid `X-Internal-Token` |
| 403 | Token valid but scope missing |
| 409 | Eval gate red and endpoint requires green |
| 503 | Underlying source (Postgres or worker) unavailable; `stale: true` in body when partial |

All errors return `{ "error": { "code", "message", "trace_id" } }`.

## 5. Caching — التخزين المؤقت

- Summary cacheable for up to 30 s server-side; clients show `last_refreshed_at`.
- Per-resource endpoints are not cached on the server.

## 6. Non-Negotiables — خطوط حمراء

- No write endpoints in this API. Mutations live under `/internal/approvals/`, `/internal/agents/`, `/internal/workers/`.
- No restricted PII is ever returned.
- Stale data is always labeled; never silently masked.
- Token leaks trigger immediate rotation and audit.

## 7. References — مراجع

- `docs/api/ULTIMATE_INTERNAL_API.md`
- `docs/security/INTERNAL_API_AUTH_GATE.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
- `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`
