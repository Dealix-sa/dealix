# Dealix Proof Pack Factory — مصنع أطقم الإثبات

`dealix/distribution/proof_packs.py` · CLI: `scripts/generate_proof_pack.py` ·
Make: `make proof-packs`

> أقوى أداة تصريف: الدليل. لكن **لا إثبات مزيّف** — الحقول تصف *خطة القياس*، لا
> أرقامًا مفترضة.

## مستويات الأدلة (canonical — `auto_client_acquisition/proof_engine/evidence.py`)

| المستوى | المعنى | الاستخدام |
| --- | --- | --- |
| L0 | مخطط — لم يُنفَّذ | داخلي |
| L1 | مسودة داخلية | داخلي (افتراضي للطقم المولّد) |
| L2 | راجعها العميل | خاص |
| L3 | وافق العميل | مبيعات خاصة |
| L4 | موافقة نشر عام | دراسة حالة عامة |
| L5 | دليل إيراد/توسعة | بعد التزام/دفع حيث ينطبق |

## المنطق
- يولّد طقمًا لكل prospect حالته `contacted`+ (dedupe لكل prospect).
- الطقم المولّد يبدأ **L1 داخلي** و`consent_public = false`.
- الترقية للاستخدام العام تمرّ عبر بوابة:
  ```python
  from dealix.distribution.proof_packs import promote_to_public
  promote_to_public(proof_id, level=4, consent_public=True)
  # يرفع ValueError إن كان <L4 أو بدون موافقة (assert_public_proof_allowed)
  ```

## البنية
يطابق `schemas/proof_pack.schema.json`:
```
id, prospect_id, company, sector, current_workflow, leakage_points[],
quick_win, measurement_plan, before_after, evidence_level,
consent_public, risks[], status, created_at
```
