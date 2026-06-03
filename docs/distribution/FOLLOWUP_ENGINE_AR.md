# Dealix Follow-up Engine — محرك المتابعة

`dealix/distribution/followups.py` · CLI: `scripts/generate_followup_queue.py` ·
Make: `make followup-queue`

> تذكير فقط — يوضّح **مَن** تتابع اليوم. لا يرسل شيئًا.

## الإيقاع (cadence)
- `new` بلا `last_contact` → لمسة أولى (`first_touch`)، أولوية **high**.
- `contacted` / `qualified` / `proposal` → مستحق بعد `DUE_AFTER_DAYS = 4`.
- `nurture` → مستحق بعد `NURTURE_AFTER_DAYS = 30`.
- `won` / `lost` → لا يُستحق أبدًا.

الأولوية حسب التأخر: ≥14 يوم **high** · 7–13 **medium** · غير ذلك **low**.

## المخرجات
سجل `data/followups/followups.jsonl` يطابق `schemas/followup.schema.json`:
```
id, prospect_id, company, sector, channel, last_contact,
due_date, days_since_contact, priority, reason, status="due", created_at
```

## حتمية وقابلة للاختبار
`today` قابل للحقن:
```python
from datetime import date
from dealix.distribution.followups import compute_due
compute_due(prospects, today=date(2026, 6, 2))
```

## الإغلاق
```python
from dealix.distribution.followups import complete_followup
complete_followup(followup_id)
```
