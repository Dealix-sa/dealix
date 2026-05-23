---
title: Feature Intake
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Feature Intake — استقبال طلبات الميزات

## Purpose
Single funnel for every feature idea — from clients, founder, analysts, or partners. Nothing skips this intake. No verbal-only requests survive past the weekly triage.

## Rules
- One row per request. Verbal requests are logged by the recipient within 24h.
- No work begins before triage. Triage is weekly, founder-led.
- Requests without a source (who asked, when) are rejected.
- PII in request descriptions is redacted per `docs/governance/PII_REDACTION_POLICY.md`.

## Intake template
```yaml
id: FR-YYYY-NNN
title: short noun phrase
source: client | founder | analyst | partner
requester: anonymized label
date_logged: YYYY-MM-DD
problem: what is broken or missing (1–2 sentences)
desired_outcome: measurable change
estimated_demand: count of distinct asks
attached_evidence: link to ledger / email / call notes
manual_workaround: yes/no — how it is delivered today
proposed_rung: document | template | automate | saas
```

## Operations
- Drop a new entry under `docs/product/intake/FR-YYYY-NNN.md` (folder created when first request lands).
- Weekly triage: founder marks status — `accepted-to-defer-kill`, `needs-evidence`, `rejected`.
- Accepted items move to [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md) for scoring.
- Rejected items remain logged with reason; re-open allowed if evidence improves.

## Evidence
- Each intake row links to source (call notes, email, ticket).
- Demand count is updated when the same request recurs from a different source.

## Owner & cadence
- Owner: Founder; later Product Lead.
- Cadence: weekly triage (30 min); monthly demand-count refresh.

## Cross-links
- [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md)
- [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md)
- [`NO_OVERBUILD_POLICY.md`](NO_OVERBUILD_POLICY.md)

---

## القسم العربي

**الغرض:** قمع واحد لكل طلب ميزة من العملاء أو المؤسس أو المحللين أو الشركاء.

**القواعد:** صف واحد لكل طلب، تسجيل خلال 24 ساعة، لا عمل قبل الفرز الأسبوعي، الطلبات بدون مصدر تُرفض.

**القالب:** id، عنوان، مصدر، صاحب الطلب، التاريخ، المشكلة، النتيجة المرغوبة، تقدير الطلب، الدليل المرفق، الحل اليدوي الحالي، الدرجة المقترحة.

**المالك:** المؤسس. **الإيقاع:** فرز أسبوعي 30 دقيقة.
