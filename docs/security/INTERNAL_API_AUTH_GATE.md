# Internal API Auth Gate — بوابة مصادقة الواجهة الداخلية

Status: v1
Owner: Founder

## 1. Purpose — الغرض

The Internal API Auth Gate is the single mechanism that authenticates and authorizes every call to `/api/v1/internal/`. It also writes the audit entry for that call.

بوابة المصادقة الداخلية هي الآلية الوحيدة لمصادقة وتفويض كل استدعاء على `/api/v1/internal/`. كما أنها تكتب قيد التدقيق لذلك الاستدعاء.

## 2. Header Contract — عقد الترويسة

- Header: `X-Internal-Token: <token>`
- Required on every internal API call.
- Missing or malformed token => `401`.
- Valid token but missing scope => `403`.
- Valid token, scope OK, but Guardian in fail-closed => `503`.

## 3. Token Format — صيغة الرمز

- Opaque random string, at least 32 bytes of entropy, base32-encoded.
- Stored hashed at rest (Argon2id).
- Bound to: caller identity, environment, scope set, IP allowlist, expiration.
- Tokens are non-extractable from the console (display-once at issuance).

## 4. Scopes — النطاقات

| Scope | Endpoints | Used by |
|---|---|---|
| `control:read` | `/internal/control/*` | Founder Console |
| `approvals:read` | `/internal/approvals` (read) | Founder Console |
| `approvals:write` | `/internal/approvals/*/approve|reject|edit` | Founder Console (founder identity) |
| `agents:read` | `/internal/agents` | Founder Console |
| `agents:kill` | `/internal/agents/*/kill|enable` | Founder identity only |
| `audit:read` | `/internal/audit*` | Founder Console |
| `workers:read` | `/internal/workers` | Founder Console |
| `workers:write` | `/internal/workers/*/kill|restart` | Founder identity only |

## 5. Audit Logging — سجل التدقيق

For every call (success or fail), the gate writes:
- `trace_id`, `at`, `caller_identity`, `token_id`, `scope`, `method`, `path`, `status`, `ip`, `user_agent`, `request_hash`, `response_summary`.

Audit writes are synchronous on mutating calls; an audit-write failure rejects the response with `503`.

## 6. Rate Limiting and Anomaly — حدود المعدل وكشف الشذوذ

- Per-token rate limits.
- Per-IP rate limits.
- Anomaly detection on token usage patterns; suspicious patterns auto-suspend the token and page the founder.

## 7. Rotation — التدوير

- Tokens have max lifetime 90 days; founder tokens 30 days.
- Rotation: dual-token window for 24 hours.
- Compromise: immediate revocation, audit entry, postmortem.

## 8. Internet Exposure — التعرض للإنترنت

- The internal API base path is not routed to the internet without:
  - The auth gate active.
  - WAF rules in front.
  - IP allowlist for founder endpoints.
- Misconfigured exposure is a P0.

## 9. Local Dev — التطوير المحلي

- Local dev uses a development token bound to `127.0.0.1` and a non-production environment marker.
- Production tokens never work in dev and vice versa (environment binding).
- Token issuance scripts refuse to mint production tokens outside the deploy path.

## 10. Non-Negotiables — خطوط حمراء

- No call without `X-Internal-Token`.
- No call without an audit entry.
- No token in source code, logs, or screenshots.
- No long-lived tokens beyond the policy maximum.

## 11. References — مراجع

- `docs/api/ULTIMATE_INTERNAL_API.md`
- `docs/api/CONTROL_PLANE_API.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/security/PRODUCTION_SECURITY_GATE.md`
