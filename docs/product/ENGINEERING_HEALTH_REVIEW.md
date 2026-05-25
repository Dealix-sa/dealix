---
title: Engineering Health Review (Monthly)
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Engineering Health Review — مراجعة صحة الهندسة الشهرية

## Purpose
Monthly cadence to read DORA + engineering metrics together, decide actions, and feed the productization ladder. Output is a short, written brief — not a meeting for its own sake.

## Inputs
- DORA numbers per [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md).
- Quality + safety numbers per [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md).
- Open bug list per [`BUG_TRIAGE.md`](BUG_TRIAGE.md).
- Incident log entries since last review.
- Open feature intake items.

## Agenda (45 minutes)
1. Numbers vs stage targets (10 min) — DORA + engineering metrics.
2. Incidents review (10 min) — every sev1/sev2 since last review; root cause and fix status.
3. Backlog hygiene (10 min) — what is overdue, what is stale, what gets killed.
4. Productization triggers (10 min) — any rung-up signals per [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md).
5. Decisions and owners (5 min).

## Outputs
- A written brief stored under `docs/product/health_reviews/YYYY-MM.md` (folder created on first review). Contains:
  - All metric values vs target (table).
  - Incident summary table (id, sev, root cause, fix date).
  - Decisions list (action, owner, due date).
  - Any productization rung-ups triggered.
- Actions flow to [`FEATURE_INTAKE.md`](FEATURE_INTAKE.md) or [`BUG_TRIAGE.md`](BUG_TRIAGE.md) as appropriate.

## Rules
- The review happens whether or not anything went wrong. Skipping is not allowed.
- If founder is unavailable, the delivery analyst writes the numbers brief and founder reviews async within 5 days.
- Decisions that change scope (kill a feature, change a target) need founder sign-off in writing.

## Evidence
- Monthly brief is the evidence. Stored in markdown.
- Each decision row links to the source metric or incident.

## Owner & cadence
- Owner: Founder.
- Cadence: monthly, first Sunday of the month.

## Cross-links
- [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md)
- [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md)
- [`BUG_TRIAGE.md`](BUG_TRIAGE.md)
- [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md)

---

## القسم العربي

**الغرض:** مراجعة شهرية لقراءة مقاييس DORA والهندسة معًا واتخاذ قرارات قصيرة موثقة.

**المدخلات:** أرقام DORA، مقاييس الجودة، قائمة الأخطاء المفتوحة، سجل الحوادث، طلبات الميزات المفتوحة.

**الأجندة (45 دقيقة):** الأرقام مقابل الأهداف، الحوادث، صحة التراكم، محفّزات المُنتجة، القرارات.

**المخرجات:** ملخص مكتوب شهري يخزّن تحت `docs/product/health_reviews/`. الإجراءات تذهب لاستقبال الميزات أو فرز الأخطاء.

**القواعد:** المراجعة لا تُلغى. القرارات التي تغيّر النطاق تحتاج توقيع المؤسس كتابيًا.

**المالك:** المؤسس. **الإيقاع:** شهري، أول أحد من الشهر.
