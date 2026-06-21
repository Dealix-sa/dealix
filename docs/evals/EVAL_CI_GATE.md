# Eval CI Gate / بوابة CI للتقييم

## Purpose / الغرض

Make AI quality a required release gate.

جعل جودة الذكاء بوابة إصدار مطلوبة.

## Eval Suites / حزم التقييم

- no-overclaim / لا مبالغة
- approval classification / تصنيف الموافقة
- sensitive data leakage / تسريب بيانات حساسة
- prompt injection / حقن الموجهات
- Arabic quality / جودة العربية
- lead scoring consistency / اتساق تقييم العملاء
- proposal quality / جودة العروض
- evidence use / استخدام الدليل

## CI Rule / قاعدة CI

Any PR that changes agents, prompts, scoring, outreach, or proposals must run evals.

أي PR يغير الوكلاء أو الموجهات أو التقييم أو التواصل أو العروض يجب أن يشغل التقييمات.

## Pass Criteria / معايير النجاح

- no A3 bypass / لا تجاوز A3
- no guaranteed claims / لا ادعاءات مضمونة
- no secret leakage / لا تسريب أسرار
- no suppressed lead outreach / لا تواصل مع عميل مستبعد
- no public proof without approval / لا إثبات عام بدون موافقة

## See Also / مراجع

- [`../agents/AGENT_GOVERNANCE_V3.md`](../agents/AGENT_GOVERNANCE_V3.md)
- [`../content/PROOF_TO_DEMAND_MACHINE.md`](../content/PROOF_TO_DEMAND_MACHINE.md)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
