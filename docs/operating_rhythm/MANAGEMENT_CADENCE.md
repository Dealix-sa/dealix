# Dealix Management Cadence — إيقاع الإدارة

أفضل الشركات لها **إيقاع واضح**. هذا الملف يُعرّف الإيقاع الذي يُبقي Dealix تنفّذ، تتعلّم، وتُحسّن.

## الغرض — Purpose

تحديد الإيقاع الذي يحوّل Dealix من ردود فعل إلى نظام يومي/أسبوعي/شهري/ربعي.

## المالك — Owner

Sami / Founder CEO.

## إيقاع المراجعة — Review Cadence

ربعي (هذا الملف نفسه يُراجَع كل ربع).

## مصدر البيانات — Source of Truth

الأرقام السرية في `/home/user/dealix-ops-private/` (خارج المستودع). يقرأها `dealix/finance/calculator.py` ويُنتج تقارير في `dealix-ops-private/finance/`.

---

## Daily — اليومي

- شغّل أمر stage / morning brief.
- نفّذ إجراء إيراد واحد على الأقل (DM, sample, proposal, follow-up).
- حدّث `pipeline_value.csv`.
- راجع approvals queue.
- أغلق اليوم بـ daily log.

**المرجع:** [`DAILY_CEO_CHECK.md`](DAILY_CEO_CHECK.md)

---

## Weekly — الأسبوعي

- شغّل weekly-close.
- راجع مقاييس الإيراد (Level 1 + Level 2 من [`CEO_KPI_TREE.md`](CEO_KPI_TREE.md)).
- راجع trust risks.
- راجع جودة التسليم (delivery QA).
- أنتج learning decision واحد على الأقل.
- حدّث playbook واحد.
- commit System Improvement.

**المراجع:**
- [`WEEKLY_OPERATING_MEETING.md`](WEEKLY_OPERATING_MEETING.md)
- [`WEEKLY_GOVERNANCE_REVIEW.md`](WEEKLY_GOVERNANCE_REVIEW.md)
- [`WEEKLY_PROOF_REVIEW.md`](WEEKLY_PROOF_REVIEW.md)
- [`WEEKLY_PRODUCTIZATION_REVIEW.md`](WEEKLY_PRODUCTIZATION_REVIEW.md)
- قالب: `dealix-ops-private/founder/weekly_ceo_review_template.md`

---

## Monthly — الشهري

- مراجعة مالية: `make ceo-finance` ثم قراءة `dealix-ops-private/finance/monthly_finance_review.md`.
- مراجعة استراتيجية.
- مراجعة الـ moat.
- مراجعة المنتجة (productization gate).
- مراجعة تخصيص رأس المال — [`../operating_finance/CAPITAL_ALLOCATION_SYSTEM_V1.md`](../operating_finance/CAPITAL_ALLOCATION_SYSTEM_V1.md).
- 30-day scorecard.

**المرجع:** [`MONTHLY_BOARD_MEMO.md`](MONTHLY_BOARD_MEMO.md)

---

## Quarterly — الربعي

- استراتيجية العروض (offer strategy).
- التسعير (pricing).
- معايير التوظيف (hiring triggers).
- استراتيجية الشركاء.
- جاهزية SaaS.
- مراجعة هذا الملف نفسه.

**المراجع:**
- [`QUARTERLY_STRATEGIC_REVIEW.md`](QUARTERLY_STRATEGIC_REVIEW.md)
- [`../company/OPERATING_CALENDAR.md`](../company/OPERATING_CALENDAR.md)

---

## القواعد — Rules

- لا يُغلق **يوم** بدون إجراء إيراد.
- لا يُغلق **أسبوع** بدون learning decision.
- لا يُغلق **شهر** بدون مراجعة مالية.
- لا يُغلق **ربع** بدون reset استراتيجي.

## الأدلّة — Evidence

- daily brief logs
- weekly review markdown
- `dealix-ops-private/finance/monthly_finance_review.md`
- Git commits

## Last Reviewed

YYYY-MM-DD
