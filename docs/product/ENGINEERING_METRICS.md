---
title: Engineering Metrics (Beyond DORA)
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Engineering Metrics — مقاييس الهندسة (ما وراء DORA)

## Purpose
DORA covers throughput and stability. This doc adds quality, safety, and AI-specific health metrics that DORA does not capture.

## Definitions

| Metric | What it measures | Target (MVP/Commercial) |
|---|---|---|
| Test coverage (critical paths) | Lines/branches covered for payment, PII, AI write actions | ≥80% |
| Eval pass rate | % of golden cases passing on each prompt/model change | ≥95% |
| Incident rate | Incidents per month, sev2 and above | ≤2/month |
| PII incident count | Confirmed PII leaks per quarter | 0 |
| Banned-claim incidents | Public claims caught by QA per quarter | 0 |
| Backlog age (p90) | 90th percentile age of open bugs | ≤30 days |
| Dependency staleness | % of dependencies >1 major version behind | ≤20% |
| Rollback rate | % of releases requiring rollback within 72h | ≤10% |

## Rules
- A PII incident or banned-claim incident, even one, triggers an incident review per `docs/governance/INCIDENT_RESPONSE.md`.
- Eval pass rate is computed before any model change ships per [`RELEASE_POLICY.md`](RELEASE_POLICY.md).
- Coverage is measured on critical paths only — we do not chase 100% coverage of utility code.

## Operations
- Test coverage: automated report stored with each release.
- Eval pass rate: run golden suite, store score in release log.
- Incident rate, PII, banned-claim: pulled from incident log monthly.
- Backlog age: pulled from issue tracker monthly.
- Dependency staleness: quarterly audit.

## Evidence
- Each metric has a source row (script, log, tracker).
- Trends plotted in [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md).

## Owner & cadence
- Owner: Founder (later Engineering Lead).
- Cadence: monthly compute; quarterly target reset.

## Cross-links
- [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md)
- [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md)
- [`BUG_TRIAGE.md`](BUG_TRIAGE.md)
- `docs/governance/INCIDENT_RESPONSE.md`

---

## القسم العربي

**الغرض:** مقاييس تكمل DORA — الجودة، الأمان، صحة الذكاء الاصطناعي.

**الأهم:** تغطية اختبارية للمسارات الحرجة ≥80%، نسبة اجتياز التقييمات ≥95%، حوادث ≤2/شهر، تسريبات PII = 0، ادعاءات ممنوعة منشورة = 0، عمر التراكم p90 ≤30 يومًا.

**القواعد:** أي حادثة PII أو ادعاء ممنوع تستدعي مراجعة حادثة. تقييمات الذكاء الاصطناعي تُشغّل قبل أي تغيير نموذج.

**المالك:** المؤسس. **الإيقاع:** حساب شهري، إعادة ضبط أهداف ربعية.
