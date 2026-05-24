# Ultimate Founder Console — لوحة المؤسس الشاملة

Status: v1
Owner: Founder
Surface: internal-only, identity-gated, audit-logged.

## 1. Purpose — الغرض

One console for the founder to operate the whole company. Read state. Approve queues. Trip kill switches. Read the audit log. Nothing more, nothing less.

لوحة واحدة يدير منها المؤسس الشركة بالكامل. قراءة الحالة. اعتماد الطوابير. تشغيل قواطع الإيقاف. قراءة سجل التدقيق. لا أكثر ولا أقل.

## 2. Branded Shell — الإطار المُعلَّم

- Bilingual (AR primary, EN mirrored).
- Dealix design system tokens.
- Top bar: company state, eval gate state, kill-switch status, founder identity.
- Left nav: pages listed in Section 4.
- Footer: build hash, registry hash, policy hash, time of last refresh.

## 3. Data Source Contract — عقد مصدر البيانات

- The console MUST consume data ONLY via the Control Plane API (`/api/v1/internal/control/*`).
- No page may call third-party APIs directly.
- No page may write through any path other than the audited approvals endpoint.
- All numbers carry a source field (which worker / which run id).

## 4. Pages — الصفحات

| Page | Route | Source | Purpose |
|---|---|---|---|
| Today | `/console` | `/control/summary` | Daily founder briefing |
| Approvals | `/console/approvals` | `/control/approvals` | The queue; approve / reject / edit |
| Agents | `/console/agents` | `/control/agents` | Per-agent state, kill switches |
| Policies | `/console/policies` | `/control/policies` | Read-only policy view + version |
| Scorecard | `/console/scorecard` | `/control/scorecard` | Maturity stage, DORA, AI cost |
| Risks | `/console/risks` | `/control/risks` | Open risks, severity, owner |
| Eval Gate | `/console/evals` | `/control/evals` | Suites, pass/fail, last run |
| Workers | `/console/workers` | `/control/workers` | Freshness, heartbeats, last error |
| Audit | `/console/audit` | `/control/audit` | Filtered, paginated audit log |
| Settings | `/console/settings` | local | Founder identity, kill switches, theme |

## 5. Fallback Rule — قاعدة الاحتياط

Every page MUST handle three states:
1. Fresh data — render normally with timestamps.
2. Stale data — render with a visible "stale since HH:MM" banner; never silently mask freshness.
3. No data — render the empty state with the reason ("worker offline", "eval gate red", "feature flag off"), never a fake number, never a zero in place of unknown.

If the Control Plane API returns 4xx/5xx, the page shows the error class and a link to the audit log entry.

## 6. Approvals UX — تجربة الاعتماد

- One item at a time.
- Shows: title, evidence panel, agent + run id, class (A2 or A3), policy decision, draft body, suggested edits.
- Buttons: Approve, Reject (with reason), Edit-then-Approve.
- Every action: writes an audit entry; updates the queue; no silent state changes.
- A3 items show a banner: "Founder-only. Not auto-approvable."

## 7. Identity and Auth — الهوية

- Founder identity required at session start (SSO or managed credential).
- IP allowlist enforced at the edge.
- Internal token required on every API call (see Internal API Auth Gate).
- Session bound to a device fingerprint; rotation enforced.

## 8. Observability of the Console — رصد اللوحة نفسها

- Page-load metrics, API call rate, error rate.
- Every approve/reject action is a tracked event.
- Console exceptions feed the same observability stack as agents.

## 9. Anti-Patterns Banned — أنماط محظورة

- No marketing copy in the console.
- No charts whose source isn't a Control Plane endpoint.
- No buttons that bypass the Guardian.
- No page that calls an LLM directly from the browser.

## 10. References — مراجع

- `docs/api/CONTROL_PLANE_API.md`
- `docs/security/INTERNAL_API_AUTH_GATE.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
- `docs/ai/CEO_COPILOT_SYSTEM.md`
