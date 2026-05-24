# Ultimate Internal API — واجهة برمجة داخلية شاملة

Status: v1
Owner: Founder
Surface: internal-only. Never internet-exposed without the Internal API Auth Gate.

## 1. Purpose — الغرض

The Internal API is the single backplane for Dealix's own surfaces (Founder Console, worker mesh, internal jobs). It exposes state, accepts approvals, and serves the Control Plane.

الواجهة الداخلية هي القناة الوحيدة للأسطح الداخلية في Dealix. تكشف الحالة، تستقبل الاعتمادات، وتخدم لوحة التحكم.

## 2. Conventions — اتفاقيات

- Base path: `/api/v1/internal/`
- Auth: `X-Internal-Token` header. Mandatory on every endpoint. See Internal API Auth Gate.
- Content type: `application/json; charset=utf-8`.
- Time: ISO-8601 UTC.
- IDs: UUIDv4 or stable slug.
- Pagination: `?limit=` and `?cursor=`; max 200 per page.
- Errors: `{ "error": { "code": string, "message": string, "trace_id": string } }`.

## 3. Endpoint Groups — مجموعات

| Group | Prefix | Purpose |
|---|---|---|
| Control | `/internal/control/` | Read state (covered separately) |
| Approvals | `/internal/approvals/` | Queue, decide, edit |
| Agents | `/internal/agents/` | Read state, trip kill switches |
| Audit | `/internal/audit/` | Read append-only log |
| Workers | `/internal/workers/` | Read heartbeats, freshness |
| Evals | `/internal/evals/` | Read suite state, last run |
| Policies | `/internal/policies/` | Read policy version + hash |

## 4. Approvals Endpoints — اعتمادات

- `GET /internal/approvals?class=A2|A3&status=open` — list queue.
- `GET /internal/approvals/{id}` — read one item with evidence.
- `POST /internal/approvals/{id}/approve` — body `{ "note": string? }`. Audit entry written.
- `POST /internal/approvals/{id}/reject` — body `{ "reason": string }`. Audit entry written.
- `POST /internal/approvals/{id}/edit` — body `{ "diff": string }`. Edits an A2 draft, re-runs Guardian.

A3 items refuse `approve` unless the caller identity is the founder.

## 5. Agents Endpoints — وكلاء

- `GET /internal/agents` — registry-derived view with current state.
- `GET /internal/agents/{id}` — single agent details, last 50 runs.
- `POST /internal/agents/{id}/kill` — trips kill switch; audited; founder only.
- `POST /internal/agents/{id}/enable` — flips kill switch back on; requires green eval gate.

## 6. Audit Endpoints — تدقيق

- `GET /internal/audit?since=&until=&actor=&agent=&class=` — filtered, paginated, append-only view.
- `GET /internal/audit/{entry_id}` — single entry, immutable.

Write to audit is internal only; no external endpoint exists.

## 7. Workers Endpoints — عُمَّال

- `GET /internal/workers` — list workers, last heartbeat, freshness, last error.
- `POST /internal/workers/{id}/kill` — stops worker; audited.
- `POST /internal/workers/{id}/restart` — restarts; audited.

## 8. Evals and Policies Endpoints — تقييم وسياسات

- `GET /internal/evals/gate` — gate state with per-suite pass/fail and last run timestamp.
- `GET /internal/evals/suites/{id}/runs/latest` — most recent run summary.
- `GET /internal/policies` — current policy version, hash, last loaded at.

## 9. Non-Negotiables — خطوط حمراء

- No endpoint sends external messages. Ever.
- No endpoint accepts a free-form prompt for an LLM. Drafting goes through agents, never raw.
- No endpoint returns `restricted` data. The serializer masks PII at the boundary.
- Every mutating endpoint writes one audit entry.
- All endpoints honor kill switches and the Guardian.

## 10. Versioning — الإصدار

- `/api/v1/internal/` is the only path. Breaking changes require `/v2/`.
- Schema changes go through a typed contract test in CI.

## 11. References — مراجع

- `docs/api/CONTROL_PLANE_API.md`
- `docs/security/INTERNAL_API_AUTH_GATE.md`
- `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`
- `docs/architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md`
