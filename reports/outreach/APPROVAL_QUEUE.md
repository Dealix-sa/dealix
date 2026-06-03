# قائمة موافقة المؤسس — Founder Approval Queue

> قالب يُجمَّع من [data/outreach/drafts.jsonl](../../data/outreach/drafts.jsonl) و
> [data/outreach/approval_actions.jsonl](../../data/outreach/approval_actions.jsonl)
> وفق [schemas/approval_action.schema.json](../../schemas/approval_action.schema.json).
> كحالة: {{as_of}} — Asia/Riyadh. لا إرسال بلا قرار مُسجّل.

## قرارات المؤسس
approve · reject · rewrite · shorten · make_formal · change_offer · move_nurture · do_not_contact

## أفضل 50 مسودة لليوم
| # | draft_id | company | sector | offer | risk | القرار المقترح |
|---|---|---|---|---|---|---|
| 1 | {{draft_id}} | {{company}} | {{sector}} | {{offer}} | {{risk}} | approve/rewrite/… |

## عناصر عالية الخطورة
| draft_id | السبب | الإجراء |
|---|---|---|
| {{draft_id}} | risk_high / claim بلا دليل | reject/rewrite |

## أفضل القطاعات اليوم
1. … (من SECTOR_PRIORITY_REPORT)

## دفعة الإرسال المقترحة
راجع [SENDING_BATCH_PLAN](SENDING_BATCH_PLAN.md).

## تحذيرات opt-out / bounce
راجع [DELIVERABILITY_REVIEW](DELIVERABILITY_REVIEW.md).

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
