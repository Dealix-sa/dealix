---
title: Bug Triage
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Bug Triage — فرز الأخطاء

## Purpose
Single severity scale, single SLA per tier, single owner per bug. Everything else (cosmetic, nice-to-have) becomes a feature request in [`FEATURE_INTAKE.md`](FEATURE_INTAKE.md), not a bug.

## Severity tiers

| Tier | Definition | Examples | SLA acknowledge | SLA fix or rollback |
|---|---|---|---|---|
| Sev1 | Customer cannot use a paid service; data loss; PII exposure; AI taking unapproved external action | Production down, payment broken, leaked PII | 30 min | 4 hours |
| Sev2 | Major function broken with manual workaround; AI quality degraded below eval threshold | Report build fails for one sector, eval pass rate <90% | 4 hours | 2 business days |
| Sev3 | Minor function broken; visual defect with workaround | Wrong label on dashboard, stale link | 1 business day | 10 business days |
| Sev4 | Cosmetic; nice-to-have polish | Spacing, wording preference | 5 business days | next quarterly cleanup or kill |

## Rules
- Sev1 is paged immediately. If founder is unreachable for >30 min, delivery analyst rolls back per the release rollback plan.
- Sev2 enters the active sprint at next standup.
- Sev3 enters the backlog; if it ages past 30 days, it is auto-promoted to Sev2 or killed.
- Sev4 is not a bug; reclassify as feature request or kill.
- Every Sev1 generates an incident review per `docs/governance/INCIDENT_RESPONSE.md`.

## Operations
- Reporter logs the bug with steps to reproduce, expected vs actual, customer impact.
- Triage owner (founder, later engineering lead) sets severity within the acknowledge SLA.
- Owner is assigned; due date set from SLA.
- Resolution recorded: fix link, rollback link, or kill rationale.

## Evidence
- Bug tracker is the source of truth. Monthly summary in [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md).
- Sev1 incidents feed Change Failure Rate per [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md).

## Owner & cadence
- Owner: Founder (later Engineering Lead).
- Cadence: daily Sev1/Sev2 scan; weekly Sev3 review; quarterly Sev4 sweep.

## Cross-links
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md)
- [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md)
- [`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md)
- `docs/governance/INCIDENT_RESPONSE.md`

---

## القسم العربي

**الغرض:** مقياس شدّة واحد، SLA واحد لكل درجة، مالك واحد لكل خطأ.

**الدرجات:**
- Sev1: العميل لا يستطيع الاستخدام، فقد بيانات، تسريب PII — إقرار خلال 30 دقيقة، إصلاح خلال 4 ساعات.
- Sev2: وظيفة رئيسية معطلة مع حل بديل — إقرار 4 ساعات، إصلاح يومان عمل.
- Sev3: وظيفة ثانوية أو عيب بصري — إقرار يوم عمل، إصلاح 10 أيام عمل.
- Sev4: تجميلي — ليس خطأ، أعد تصنيفه طلب ميزة أو أوقف.

**القواعد:** Sev1 يستدعي مراجعة حادثة دائمًا. Sev3 الذي يتجاوز 30 يومًا يُرفّع تلقائيًا أو يُلغى.

**المالك:** المؤسس. **الإيقاع:** مسح يومي للدرجات العالية، أسبوعي للمتوسطة، ربعي للمنخفضة.
