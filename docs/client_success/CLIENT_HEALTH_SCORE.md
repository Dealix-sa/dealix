---
title: Client Health Score
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Client Health Score — نقاط صحة العميل

## Purpose
A single number 0-100 per active client. Drives tier assignment, retention work, and upsell readiness. Computed from observed behaviour, not feelings.

## Scoring rules
Each item adds 20 points if true within the last 30 days:

| Signal | Points |
|---|---|
| Client used the latest deliverable (report, dashboard, output) — confirmed in conversation or via usage signal | +20 |
| Positive written feedback received (email, message, meeting note) | +20 |
| Asked for more work (new sprint, retainer, additional scope) | +20 |
| Meetings were created from Dealix output (e.g., scored leads led to client booking calls) | +20 |
| Asked about monthly support / retainer continuation | +20 |

Maximum: 100. Minimum: 0.

## Bands

| Band | Score | Tier | Action |
|---|---|---|---|
| Retainer-ready | 90-100 | Strategic candidate | Plan upsell per [`UPSELL_PLAYBOOK.md`](UPSELL_PLAYBOOK.md); request consent for case study per [`docs/content/CASE_STUDY_SYSTEM.md`](../content/CASE_STUDY_SYSTEM.md) |
| Nurture | 60-89 | Core | Maintain weekly cadence; deepen one usage habit per [`RETENTION_PLAYBOOK.md`](RETENTION_PLAYBOOK.md) |
| Risk | 0-59 | Risk | Trigger risk playbook within 7 days; founder owns the conversation |

## Rules
- Score is recomputed weekly when the weekly report is sent.
- A signal counts only with evidence (link to email, meeting note, or usage record). No "I think they liked it".
- Score is private to Dealix; not shared with the client.
- A score drop of ≥20 points week-over-week triggers an immediate founder check-in.
- No score is published as a customer-facing metric.

## Operations
- Stored as a row per week in `docs/client_success/clients/<anonymized-label>/health.md`.
- Roll-up table in the client portfolio review.

## Evidence
- Each scored signal links to its source (email, note, usage log).

## Owner & cadence
- Owner: Founder.
- Cadence: weekly recompute; monthly tier review.

## Cross-links
- [`CLIENT_TIERING.md`](CLIENT_TIERING.md)
- [`RETENTION_PLAYBOOK.md`](RETENTION_PLAYBOOK.md)
- [`UPSELL_PLAYBOOK.md`](UPSELL_PLAYBOOK.md)
- [`RENEWAL_PLAYBOOK.md`](RENEWAL_PLAYBOOK.md)

---

## القسم العربي

**الغرض:** رقم واحد 0-100 لكل عميل نشط. يحرك التصنيف والاحتفاظ والتوسعة.

**قواعد التسجيل (كل بند +20 إذا تحقق خلال 30 يومًا):**
- استخدم العميل آخر مُخرج — مؤكد بمحادثة أو إشارة استخدام.
- تغذية راجعة إيجابية مكتوبة.
- طلب مزيدًا من العمل.
- أنشئت اجتماعات من مُخرجاتنا (مثلًا حجز عميل مكالمات من leads مُسجّلة).
- سأل عن دعم/Retainer شهري.

**الفئات:** 90-100 جاهز لـ Retainer (استراتيجي)، 60-89 Nurture (أساسي)، 0-59 خطر.

**القواعد:** إعادة حساب أسبوعية مع التقرير. كل إشارة تحتاج دليلًا. النقاط داخلية لا تُشارك. هبوط ≥20 نقطة أسبوعيًا يستدعي تدخل المؤسس فورًا.

**المالك:** المؤسس. **الإيقاع:** أسبوعي.
