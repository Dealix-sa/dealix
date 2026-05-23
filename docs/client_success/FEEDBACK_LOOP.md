---
title: Feedback Loop
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Feedback Loop — حلقة التغذية الراجعة

## Purpose
How feedback is solicited, logged, and acted on. Without a structured loop, feedback gets remembered selectively and biases decisions.

## Sources
- Weekly report responses.
- Standing call notes.
- Monthly review meetings per `docs/delivery/CLIENT_REVIEW_MEETING.md`.
- End-of-engagement debrief.
- Unsolicited messages (email, chat, in-person).
- Internal observations by delivery analyst.

## Logging
Every feedback item gets one row in `docs/client_success/clients/<anonymized-label>/feedback.md` with:
- Date received.
- Source (call, email, meeting note, etc.).
- Verbatim or near-verbatim quote (anonymized of any PII).
- Sentiment tag: positive | neutral | negative.
- Topic tag: scope | quality | speed | communication | pricing | other.
- Status: new | acknowledged | acted-on | closed.
- Linked action (if any).

## Rules
- Feedback is logged within 48 hours of receipt.
- Negative feedback is acknowledged in writing within 48 hours.
- No editing of client quotes to soften. Quote is verbatim or summarized but tagged "summary" not "quote".
- Feedback used in case studies or content requires written A2 client consent per [`docs/content/CASE_STUDY_SYSTEM.md`](../content/CASE_STUDY_SYSTEM.md).
- Internal observations are tagged "internal" and never quoted externally.

## Acting on feedback
- Quality issues → bug or change in [`docs/product/BUG_TRIAGE.md`](../product/BUG_TRIAGE.md) / `docs/delivery/CHANGE_REQUEST_PROCESS.md`.
- Scope issues → change request per `docs/delivery/CHANGE_REQUEST_SYSTEM.md`.
- Pricing → noted for renewal per [`RENEWAL_PLAYBOOK.md`](RENEWAL_PLAYBOOK.md), not adjusted mid-contract.
- Pattern across clients → feeds [`docs/product/FEATURE_INTAKE.md`](../product/FEATURE_INTAKE.md).

## Operations
- Delivery analyst logs feedback; founder reviews weekly.
- Monthly: founder reads all negative-tag items as a batch, looks for patterns.

## Evidence
- Feedback log per client. Quarterly summary in client portfolio review.

## Owner & cadence
- Owner: Delivery analyst logs; founder reviews and acts.
- Cadence: per item, weekly review, monthly pattern scan.

## Cross-links
- [`CLIENT_HEALTH_SCORE.md`](CLIENT_HEALTH_SCORE.md)
- [`RETENTION_PLAYBOOK.md`](RETENTION_PLAYBOOK.md)
- [`docs/product/FEATURE_INTAKE.md`](../product/FEATURE_INTAKE.md)

---

## القسم العربي

**الغرض:** التغذية الراجعة تُجمع وتُسجّل ويُعمل بها بطريقة مهيكلة.

**المصادر:** ردود التقرير، ملاحظات المكالمات، اجتماعات المراجعة، debrief نهاية العقد، رسائل عفوية، ملاحظات داخلية.

**التسجيل:** صف واحد لكل بند يحوي التاريخ، المصدر، الاقتباس الحرفي بعد تنقية PII، وسم المشاعر، وسم الموضوع، الحالة، الإجراء المرتبط.

**القواعد:** التسجيل خلال 48 ساعة. الإقرار بالتغذية السلبية كتابيًا خلال 48 ساعة. لا تعديل لاقتباس العميل. أي اقتباس خارجي يحتاج موافقة A2.

**التحرك:** مشاكل الجودة لفرز الأخطاء، نطاق لطلب تغيير، التسعير يُحفظ للتجديد لا يُعدل وسط العقد، النمط بين العملاء يغذي استقبال الميزات.

**المالك:** المحلل يسجّل، المؤسس يراجع ويتحرك. **الإيقاع:** فوري، مراجعة أسبوعية، فحص نمط شهري.
