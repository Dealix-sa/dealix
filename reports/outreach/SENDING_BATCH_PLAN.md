# خطة دفعات الإرسال — Sending Batch Plan

> قالب يُجمَّع من [data/outreach/sending_batches.jsonl](../../data/outreach/sending_batches.jsonl)
> وفق [schemas/sending_batch.schema.json](../../schemas/sending_batch.schema.json).
> كحالة: {{as_of}} — Asia/Riyadh. إرسال تدريجي لا دفعة جماعية.

## منحنى الإحماء (سقف الإرسال/يوم)
| الأسبوع | المسودات/يوم | الإرسال/يوم |
|---|---|---|
| 0 | 250 | 0–20 |
| 1 | 250 | 25–50 |
| 2 | 250 | 50–100 |
| 3 | 250 | 100–150 |
| 4+ | 250 | 150–250 (فقط بصحة سليمة) |

السقف يُحسب آليًا عبر `sending_ramp_cap(week, health)` — يهبط إلى 0 عند تجاوز عتبات الصحة.

## لا تُرسَل الدفعة إذا
no unsubscribe · no approval · no personalization · suppressed recipient ·
domain unhealthy · bounce spike. المرجع: `batch_send_allowed`.

## الدفعات
| batch_id | account | domain | sector | step | batch_size | cap | approved_at | status |
|---|---|---|---|---|---|---|---|---|
| {{batch_id}} | {{account}} | {{domain}} | {{sector}} | {{step}} | {{size}} | {{cap}} | {{approved}} | {{status}} |

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
