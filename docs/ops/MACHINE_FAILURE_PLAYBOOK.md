# Machine Failure Playbook — Dealix

## الدور — Role

كتاب التشغيل عند فشل أي ماكينة. الهدف: تقصير MTTR وتقليل الأثر التجاري.

## الخطوات — Steps

1. **Detect** — `machine_health.csv` يُحدَّث + Daily Brief يعرض الـ failures.
2. **Triage** — تصنيف: P1 (يقطع كاش)، P2 (يقطع distribution)، P3 (يقطع reporting).
3. **Disable** — استخدام `disable_switch` من `machine_registry.yaml` فوراً.
4. **Notify** — تسجيل event في `<private_ops>/ops/incidents.csv`.
5. **Investigate** — قراءة `audit_log` + logs.
6. **Fix** — إما code fix أو operational fix.
7. **Restore** — تشغيل تدريجي + مراقبة 24 ساعة.
8. **Post-mortem** — قصيرة في `<private_ops>/learning/incidents.md`.

## P-levels

| Priority | تعريف | SLA |
| --- | --- | --- |
| P1 | يوقف كاش (payment_capture, proposal_factory) | ≤ 2 ساعات |
| P2 | يوقف distribution (queues, drafts) | ≤ 8 ساعات |
| P3 | يوقف reporting (forecast, brief) | ≤ 24 ساعة |

## القواعد — Rules

- لا "Fix فوري بدون disable" لماكينة تتفاعل مع العميل (Trust-touching).
- post-mortem إلزامي لكل P1، اختياري لـ P2/P3.
- لا يُلغى incident بدون recovery_path تطبَّق.

## الملكية — Ownership

- Owner: Founder.
- Auditor: Trust gate لـ P1.
