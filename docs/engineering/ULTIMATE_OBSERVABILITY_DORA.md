# Ultimate Observability + DORA — الرصد الشامل ومقاييس DORA

Status: v1
Owner: Founder

## 1. Purpose — الغرض

A single observability discipline that covers DORA delivery metrics, AI cost, audit completeness, and worker freshness. Anything we cannot measure, we do not claim.

انضباط رصد واحد يغطي مقاييس تسليم DORA، تكلفة الذكاء الاصطناعي، اكتمال التدقيق، وحداثة العُمَّال. ما لا نستطيع قياسه، لا نَدَّعيه.

## 2. The Four DORA Metrics — مقاييس DORA الأربعة

| Metric | Definition | Source | Target |
|---|---|---|---|
| Deployment frequency | Production deploys per week | Release tags | >= 3 / week |
| Lead time for changes | PR merged -> deployed (hours) | CI/CD + tag | <= 24 h |
| Change failure rate | % deploys requiring rollback or hotfix | Incidents + tags | <= 10% |
| MTTR | Mean time to recover from a production incident | Incident log | <= 60 min |

DORA is computed weekly and exposed via `/api/v1/internal/control/scorecard`.

## 3. AI Cost — تكلفة الذكاء الاصطناعي

- Per-agent token and SAR spend, daily and weekly.
- Per-provider breakdown.
- Cost per approved draft (signal for value vs. spend).
- Hard cap per agent per day; soft cap alerts at 80%.
- Hard cap per provider per day; routing falls back when capped.

## 4. Audit Completeness — اكتمال التدقيق

Measured as the % of mutating operations that produced an audit entry.
- Target: 100%. Any value below 100% is a P1.
- Sources: API mutations, Guardian decisions, approvals, kill-switch toggles, registry changes, policy reloads.
- Reconciliation job runs hourly and flags gaps.

## 5. Worker Freshness — حداثة العُمَّال

- Each worker declares a freshness SLO (e.g., "intelligence_collector must produce within 60 min").
- Heartbeats every minute.
- Freshness % per worker: window where the worker met its SLO / total window.
- A worker that falls below target flips to "stale" on the Founder Console and opens a risk.

## 6. Eval Gate Telemetry — قياس بوابة التقييم

- Suite pass/fail per release.
- Time to green after a regression.
- Red-team corpus growth per month (must be non-negative).

## 7. Logs, Metrics, Traces — السجلات والمقاييس والآثار

- Logs: structured JSON, correlation IDs (`trace_id`, `agent_id`, `run_id`, `policy_version`).
- Metrics: counters, gauges, histograms; namespaced `dealix.<domain>.<name>`.
- Traces: every API request and every agent run; gates emitted as span events.

## 8. SLOs — أهداف مستوى الخدمة

| Surface | SLO |
|---|---|
| Control Plane API availability | 99.5% monthly |
| Control Plane summary latency (p95) | < 500 ms |
| Guardian decision latency (p95) | < 1.5 s |
| Audit write success | 100% |
| Worker freshness, average | >= 95% |

## 9. Alerting — التنبيه

- P0: external send attempted (impossible by design; alert if detected).
- P0: Guardian crash or disablement without audit.
- P1: audit completeness < 100%.
- P1: eval gate red.
- P2: worker freshness < SLO.
- P2: AI cost soft cap breached.
- P3: DORA metric outside target two consecutive weeks.

## 10. Non-Negotiables — خطوط حمراء

- No metric is presented without a source field.
- No dashboard hides staleness.
- No deploy without DORA tagging.
- No agent ships without a token cost cap.

## 11. References — مراجع

- `docs/api/CONTROL_PLANE_API.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/runtime/ULTIMATE_WORKER_MESH.md`
