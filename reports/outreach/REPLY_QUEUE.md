# طابور الردود — Reply Queue

> قالب يُجمَّع من [data/outreach/replies.jsonl](../../data/outreach/replies.jsonl) وفق
> [schemas/reply.schema.json](../../schemas/reply.schema.json). كحالة: {{as_of}} — Asia/Riyadh.
> التصنيف عبر `auto_client_acquisition/email/reply_classifier.py`.

## خريطة الإجراء (المرجع: `reply_next_action`)
| الفئة | الإجراء |
|---|---|
| positive | discovery_invite |
| interested_later | nurture |
| price_question | offer_card |
| send_more_info | proof_pack |
| wrong_person | referral_ask |
| not_interested | close_polite |
| unsubscribe | suppress (فوري ودائم) |
| angry | apologize_and_suppress |
| auto_reply | ignore |
| bounce | suppress |

## الردود
| reply_id | prospect_ref | category | sentiment | next_action | requires_founder |
|---|---|---|---|---|---|
| {{reply_id}} | {{prospect}} | {{category}} | {{sentiment}} | {{action}} | {{founder}} |

> الردود الإيجابية تُوجَّه إلى [مسار واتساب بعد الرد](../../docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md)
> أو الحجز — بعد التفاعل وبموافقة المؤسس فقط.

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
