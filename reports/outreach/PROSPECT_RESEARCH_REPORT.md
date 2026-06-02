# تقرير بحث العملاء المحتملين — Prospect Research Report

> قالب يُجمَّع من [data/prospects/prospects.jsonl](../../data/prospects/prospects.jsonl)
> وفق [schemas/prospect.schema.json](../../schemas/prospect.schema.json). بدون scraping.
> كحالة: {{as_of}} — Asia/Riyadh.

## ملخص
- عدد العملاء المحتملين: {{count}} — مؤهّلون: {{qualified}} — جاهزون لمسودة: {{draft_ready}}
- مصادر: founder_list · inbound · referral · public_research · event · partner
- قائمة الكبت فعّالة: [suppression_list.jsonl](../../data/prospects/suppression_list.jsonl)

## النقاط (Score = 100)
sector_fit 20 · likely_lead_flow 20 · decision_maker_clarity 15 · pain_signal 15 ·
payment_ability 15 · personalization_signal 10 · low_risk 5

| prospect_id | company | sector | status | score.total | personalization | risk |
|---|---|---|---|---|---|---|
| {{prospect_id}} | {{company}} | {{sector}} | {{status}} | {{score}} | {{p_level}} | {{risk}} |

## أعلى 10 (مرتبة بالنقاط)
1. … (تُملأ آليًا)

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
