# Retainer Conversion Playbook — دليل التحويل إلى عقد شهري

## الغرض (AR)
يشرح هذا الدليل كيف تتحوّل التجربة المُسلَّمة إلى عقد شهري متكرر (Retainer). العقد الشهري هو مصدر الدخل المستقر، ويُبنى على نتائج التجربة الموثّقة. كل العروض شفافة وبلا ضمانات عائد، والتواصل يدوي ومعتمد.

## Purpose (EN)
This playbook explains how a delivered pilot converts into a recurring retainer. The retainer is the stable revenue source, built on documented pilot results. All offers are transparent with no guaranteed ROI, and contact is manual and approved.

## شرط البداية / Entry Condition
- يجب أن تكون الحالة `pilot_delivered`.
- توفّر أصول إثبات (proof assets) من التجربة دون كشف بيانات العميل.

The deal must be at `pilot_delivered` with proof assets generated without exposing client data.

## من التجربة إلى العقد / From Pilot to Retainer
1. **مراجعة نتائج التجربة** / Review pilot outcomes مقابل معايير النجاح المتفق عليها.
2. **صياغة القيمة المستمرة** / Frame ongoing value: ما الذي يستمر العميل في الحصول عليه شهريًا.
3. **هيكلة العقد** / Structure the retainer: النطاق الشهري، التسعير، مدة الالتزام، آلية المراجعة.
4. **العرض والإغلاق** / Propose and close: اتفاق مكتوب، ثم تسجيل `retainer_started`.

## هيكلة العقد / Retainer Structuring

| العنصر / Element | التوصية / Recommendation |
|---|---|
| النطاق / Scope | محدد شهريًا وقابل للتعديل بالمراجعة |
| التسعير / Pricing | ثابت شهري، معلن مسبقًا |
| المدة / Term | التزام واضح مع شروط إنهاء عادلة |
| المراجعة / Review | إيقاع مراجعة نجاح دوري |

## معالجة الاعتراضات / Objection Handling
- "لماذا شهري؟" / "Why monthly?": القيمة مستمرة والتحسين تراكمي.
- "نريد تخفيضًا" / "Discount?": اربط السعر بالنطاق، لا بوعود عائد.
- "نحتاج مرونة" / "Need flexibility": شروط إنهاء واضحة وعادلة.

## السلامة / Safety
- لا ضمان عائد، لا أرقام مفبركة، لا ادعاءات غير مثبتة.
- العقد يدوي ومعتمد من المؤسس بالكامل.

No guaranteed ROI, no fabricated numbers, no unproven claims. The contract is fully manual and founder-approved.

## التسجيل / Recording
سجّل `retainer_proposed` ثم `retainer_started` مع `amount_sar` (القيمة الشهرية) في السجل.
Record `retainer_proposed` then `retainer_started` with monthly `amount_sar` in the ledger.
