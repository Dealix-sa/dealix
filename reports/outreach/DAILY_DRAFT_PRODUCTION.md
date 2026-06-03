# إنتاج المسودات اليومي — Daily Draft Production

> قالب يُجمَّع من [data/outreach/drafts.jsonl](../../data/outreach/drafts.jsonl) وفق
> [schemas/outreach_draft.schema.json](../../schemas/outreach_draft.schema.json).
> كحالة: {{as_of}} — Asia/Riyadh.

## الهدف اليومي — 250 مسودة (الإنتاج فقط؛ الإرسال محكوم بالمنحنى)

| sequence_step | المستهدف | المنتج | اجتاز بوابة الجودة |
|---|---:|---:|---:|
| first_touch | 100 | {{n}} | {{passed}} |
| follow_up_1 | 75 | {{n}} | {{passed}} |
| follow_up_2 | 50 | {{n}} | {{passed}} |
| proposal_intro | 15 | {{n}} | {{passed}} |
| close_loop | 10 | {{n}} | {{passed}} |
| **الإجمالي** | **250** | {{total}} | {{total_passed}} |

## بوابة الجودة (لا تُرسَل المسودة إذا)
- personalization < P1 · risk_level = high · unsubscribe مفقود · ادعاء بلا دليل ·
  الشركة في قائمة الكبت · subject مضلّل.
- المرجع البرمجي: `draft_quality_gate` في
  [market_production_os.py](../../dealix/marketing_factory/market_production_os.py).

## عيّنة
| draft_id | company | sector | step | offer | personalization | compliance | approval | unsubscribe |
|---|---|---|---|---|---|---|---|---|
| {{draft_id}} | {{company}} | {{sector}} | {{step}} | {{offer}} | {{p}} | {{c}} | {{a}} | {{u}} |

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
