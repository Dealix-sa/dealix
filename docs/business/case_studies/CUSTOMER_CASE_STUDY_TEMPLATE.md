# Dealix — Customer Case Study Template — نموذج دراسة حالة عميل

> Hypothetical / case-safe template. Replace `{{ ... }}` only after written customer consent. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### العميل
- التسمية الآمنة: `{{ anonymized_label }}` (مثال: A1).
- القطاع: `{{ sector }}`.
- الحجم: `{{ size_band }}` (مثل: 50-100 موظف).
- البلد: المملكة العربية السعودية.
- التسمية الحقيقية: تُكشَف فقط بموافقة كتابية.

### القبل (Before)
- المشكلة بثلاث جمل.
- المؤشّر المرجعي قبل البدء (قياس أصلي).
- ما جرَّبوه قبلنا.

### الفعل (Action)
- العرض المختار: `{{ offer_id }}` (من [`OFFER_CATALOG.json`](../OFFER_CATALOG.json)).
- مدّة التنفيذ: `{{ duration }}`.
- وكلاء مُسجَّلون: `{{ agent_count }}`.
- مستوى المخاطر الأعلى المُستخدَم: T0 / T1 / T2 / T3.

### المخرَج (Output)
- Evidence Packs مُولَّدة: `{{ count }}`.
- موافقات مُسجَّلة: `{{ count }}`.
- حوادث Tool Permission Matrix: 0 (متطلَّب).
- إرسالات خارجية بدون موافقة: 0 (متطلَّب).

### النتيجة (Outcome) — case-safe
- المؤشر بعد: `{{ after_metric }}` (تقديري حتى تربط Evidence Packs).
- Verified Revenue: `{{ verified_sar }}` ريال.
- Estimated Pipeline: `{{ estimated_sar }}` ريال (مفصول).
- ساعات المؤسس المُوفَّرة: `{{ hours }}` ساعة/شهر (قياس قبل/بعد).

### الدرس (Learning)
- ما الذي عمل (بأدلة).
- ما الذي لم يعمل (بأمانة).
- توصية للقطاع.

### التالي (Next)
- المرحلة المقبلة.
- توسعة وكلاء؟
- ترقية حزمة؟

### الموافقات والإفصاح
- العميل وافق على نشر: `{{ yes | no }}` بتاريخ `{{ date }}`.
- اسم العميل الفعلي: `{{ disclosed | redacted }}`.
- ملخّص قانوني: تمت مراجعة هذه الدراسة قبل النشر.

---

## English

### Customer
- Safe label: `{{ anonymized_label }}` (e.g., A1).
- Sector: `{{ sector }}`.
- Size: `{{ size_band }}` (e.g., 50-100 employees).
- Country: Kingdom of Saudi Arabia.
- Real name: disclosed only with written consent.

### Before
- The problem in three sentences.
- The baseline metric prior to start (original measurement).
- What they tried before us.

### Action
- Selected offer: `{{ offer_id }}` (from [`OFFER_CATALOG.json`](../OFFER_CATALOG.json)).
- Duration: `{{ duration }}`.
- Agents registered: `{{ agent_count }}`.
- Highest risk tier used: T0 / T1 / T2 / T3.

### Output
- Evidence Packs produced: `{{ count }}`.
- Approvals recorded: `{{ count }}`.
- Tool Permission Matrix incidents: 0 (required).
- External sends without approval: 0 (required).

### Outcome — case-safe
- After-metric: `{{ after_metric }}` (estimated until Evidence Packs link it).
- Verified Revenue: `{{ verified_sar }}` SAR.
- Estimated Pipeline: `{{ estimated_sar }}` SAR (separated).
- Founder hours saved: `{{ hours }}` hours/month (before/after measurement).

### Learning
- What worked (with evidence).
- What did not work (honestly).
- Recommendation for the sector.

### Next
- Next phase.
- More agents?
- Package upgrade?

### Approvals and Disclosure
- Customer consented to publication: `{{ yes | no }}` on `{{ date }}`.
- Actual customer name: `{{ disclosed | redacted }}`.
- Legal review: reviewed before publication.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
