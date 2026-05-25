---
title: DORA Metrics Policy
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# DORA Metrics Policy — سياسة مقاييس DORA

## Purpose
Define the four DORA metrics Dealix tracks for engineering throughput and stability. Targets are stage-appropriate; we do not benchmark against enterprise teams while we are a founder + analysts.

## Definitions
- **Deployment frequency (DF)** — how often production receives a successful change.
- **Lead time for changes (LT)** — time from commit merged to running in production.
- **Change failure rate (CFR)** — % of deployments causing user-impacting incident, rollback, or hotfix within 24h.
- **Time to restore service (MTTR)** — median time from incident detection to restored service.

## Stage targets

| Stage | DF | LT | CFR | MTTR |
|---|---|---|---|---|
| MVP (pre-revenue) | ≥1/week | ≤3 days | ≤25% | ≤24h |
| Commercial (≤SAR 50k MRR) | ≥2/week | ≤2 days | ≤20% | ≤8h |
| Scaling (SAR 50–250k MRR) | ≥1/day | ≤1 day | ≤15% | ≤4h |
| Mature (>SAR 250k MRR) | on-demand | ≤4h | ≤10% | ≤1h |

## Rules
- A deployment counts only if it survives 24h without rollback.
- Hotfixes count as deployments and as change failures.
- Manual ops scripts run against production count if they mutate customer data.
- Targets are reviewed each quarter against actual stage.

## Operations
- Measurement source: git log + deploy log + incident log (see `docs/governance/INCIDENT_RESPONSE.md`).
- Monthly: founder pulls the four numbers, logs them, compares to stage target.
- Below-target metrics generate an action item in [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md).

## Evidence
- Numbers stored alongside engineering health review notes.
- Each incident contributing to CFR or MTTR is linked.

## Owner & cadence
- Owner: Founder (later Engineering Lead).
- Cadence: monthly recompute; quarterly target review.

## Cross-links
- [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md)
- [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md)
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md)
- `docs/governance/INCIDENT_RESPONSE.md`

---

## القسم العربي

**الغرض:** أربعة مقاييس DORA لقياس إنتاجية الهندسة واستقرارها.

**التعريفات:** تكرار النشر، زمن وصول التغيير للإنتاج، نسبة فشل التغيير، زمن استعادة الخدمة.

**الأهداف حسب المرحلة:**
- MVP: نشر/أسبوع، وصول ≤3 أيام، فشل ≤25%، استعادة ≤24س.
- تجاري: نشر مرتين/أسبوع، ≤2 يوم، ≤20%، ≤8س.
- توسع: نشر يومي، ≤يوم، ≤15%، ≤4س.
- ناضج: عند الطلب، ≤4س، ≤10%، ≤1س.

**القواعد:** النشر لا يُحسب إلا إذا صمد 24 ساعة بدون تراجع. الإصلاحات السريعة تُحسب نشرًا وفشلًا.

**المالك:** المؤسس. **الإيقاع:** حساب شهري، مراجعة أهداف ربعية.
