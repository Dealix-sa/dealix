# مراجعة صحة الدومين — Domain Health Review

> قالب يُجمَّع من [data/outreach/email_accounts.jsonl](../../data/outreach/email_accounts.jsonl)
> وفق [schemas/email_account.schema.json](../../schemas/email_account.schema.json).
> كحالة: {{as_of}} — Asia/Riyadh.

## العتبات
- bounce_rate < 0.03 · spam_complaint_rate < 0.003 (0.3%) · لا provider_warning.
- عند التجاوز: `sending_ramp_cap` يُرجع 0 (إيقاف مؤقت) ويُعاد الإحماء.

## الحالة لكل دومين
| account_id | domain | warmup_stage | daily_cap | bounce_rate | spam_rate | provider_warning | health_status |
|---|---|---|---|---|---|---|---|
| {{account}} | {{domain}} | {{stage}} | {{cap}} | {{bounce}} | {{spam}} | {{warn}} | {{health}} |

## إجراءات
- degraded/paused → خفّض الحجم، راجع المحتوى والمصادر، عالج الارتداد، أعد الإحماء.

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
