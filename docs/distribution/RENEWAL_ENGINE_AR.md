# Dealix Renewal & Upsell Engine — محرك التجديد والتوسعة

`dealix/distribution/renewals.py` · CLI: `scripts/generate_renewal_queue.py` ·
Make: `make renewal-queue`

> التصريف الحقيقي ليس أول بيع — بل **التجديد**. والقاعدة: **لا upsell قبل Proof.**

## المنطق
- يبني فرص تجديد/upsell للعملاء المُسلَّمين (prospects حالتهم `won`).
- الرُتبة التالية تأتي من سلّم العروض الرسمي (`natural_next_offer`).
- **يتخطّى** أي عميل `evidence_level < L1` (لا توسعة لقيمة لم تُثبت).
- `due_date = today + RENEWAL_LEAD_DAYS (90)`.

## سلّم الـ upsell (مثال من الكتالوج)
```
ai_workflow_audit → agentic_workflow_pilot → … → ai_ops_retainer → department_expansion
```

## البنية
يطابق `schemas/renewal.schema.json`:
```
id, client, current_offer, delivered_value, next_offer,
evidence_level, due_date, status, created_at
```
الحالات: `upcoming → drafted → approved → sent → renewed | lost`.

## التحقق
```python
from dealix.distribution.renewals import build_renewal
build_renewal({"company": "Co", "sector": "clinics", "evidence_level": 0})  # None (لا proof)
```
