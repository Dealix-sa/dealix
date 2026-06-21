# مصنع حزم الدليل — Dealix Proof Pack Factory

هذا الملف يحدّد **محتويات حزمة الدليل** وتعريفات **مستويات الدليل L0–L5**. الكيان `proof_pack` يحمل الحقول حرفياً: `id`, `customer_id`, `current_process`, `leakage_points`, `quick_win`, `before_after`, `measurement_method`, `evidence_level`, `risk`, `recommended_pilot`.

This file defines the **proof pack contents** and the **evidence levels L0–L5**. The `proof_pack` entity carries the fields above verbatim.

روابط / Related: [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) · [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) · [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md)

---

## محتويات حزمة الدليل / Proof pack contents

| العنصر / Item | الحقل / Field | الوصف / Description |
|---|---|---|
| العملية الحالية / Current process | `current_process` | كيف يعمل العميل اليوم. / How the customer works today. |
| نقاط التسرّب / Leakage points | `leakage_points` | أين تُفقَد الفرص أو الكفاءة. / Where opportunities or efficiency leak. |
| مكسب سريع / Quick win | `quick_win` | تحسين قابل للتطبيق فوراً. / An immediately actionable improvement. |
| قبل/بعد / Before–after | `before_after` | مقارنة موثَّقة لا وعد. / A documented comparison, not a promise. |
| طريقة القياس / Measurement method | `measurement_method` | كيف قِيس الأثر. / How impact was measured. |
| مستوى الدليل / Evidence level | `evidence_level` | L0–L5 (انظر أدناه). / L0–L5 (see below). |
| المخاطر / Risk | `risk` | حدود وقيود الدليل. / Caveats and limits of the evidence. |
| الـ Pilot الموصى به / Recommended pilot | `recommended_pilot` | الدرجة التالية المناسبة من [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md). / The right next rung. |

> كل رقم في `before_after` يجب أن يقترن بـ`measurement_method` و`evidence_level`؛ لا رقم بلا مصدر قياس. / Every number in before–after must carry a measurement method and an evidence level; no number without a measurement source.

---

## مستويات الدليل / Evidence levels (L0–L5)

| المستوى / Level | التعريف / Definition | أمثلة الاستخدام / Use |
|---|---|---|
| **L0** | لا دليل — فرضية أو تقدير فقط. / No evidence — hypothesis or estimate only. | عميل `new`، فرضية ألم. / New prospect, pain hypothesis. |
| **L1** | إشارة نوعية — ملاحظة من العميل أو مراجعة عيّنة. / Qualitative signal — customer remark or sample review. | تشخيص مجاني، Diagnostic مبدئي. |
| **L2** | تحليل موثَّق — بيانات العميل بعد تنظيف/تسجيل. / Documented analysis — cleaned/scored customer data. | Sprint، Data Pack، Top 50. |
| **L3** | نتيجة مقيسة — قبل/بعد بطريقة قياس واضحة. / Measured result — before/after with a clear method. | Pilot، Proof pack تشغيلي. |
| **L4** | نتيجة متكرّرة — أثر مقيس عبر دورات/عملاء. / Repeated result — measured across cycles/customers. | RevOps OS مستمر، أنماط مؤكَّدة. |
| **L5** | نتيجة مُتحقَّق منها مستقلاً — تحقّق خارجي/تدقيق. / Independently verified — external check/audit. | حالة مرجعية موثَّقة بالكامل. |

> القاعدة: لا ادعاء يتجاوز مستواه. الأرقام (تحويل/عائد/توفير) تُذكَر فقط من **L3 فأعلى** ومع `measurement_method`. ما دون ذلك يُصاغ كـ«فرصة تقديرية». / Rule: no claim beyond its level. Numbers appear only at **L3+** with a measurement method; below that, framed as an "estimated opportunity".

---

## كيف تُستخدَم المستويات / How levels are used

- **في المسودات:** [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) يمنع أي ادعاء رقمي دون L3. / Drafts: numeric claims blocked below L3.
- **في العروض:** `evidence_level` على `proposal` يحكم لغة القيمة. / Proposals: evidence level governs value language.
- **في الترقية:** [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md) يربط كل درجة بحد أدنى من المستوى. / Ladder: each rung ties to a minimum level.
- **في الدراسات:** أي حالة بلا عميل حقيقي تُوسَم «نموذج افتراضي آمن». / Case studies: any case without a real customer is labeled "Hypothetical / case-safe template".

---

## قواعد ملزمة / Binding rules

1. لا PII في حزمة الدليل؛ تُستخدَم تسميات مجهَّلة. / No PII in the proof pack; anonymized labels.
2. لا رقم بلا `measurement_method` و`evidence_level`. / No number without a measurement method and an evidence level.
3. لا ادعاء يتجاوز المستوى المسجَّل. / No claim beyond the recorded level.
4. `before_after` مقارنة موثَّقة، لا وعد ولا ضمان. / Before–after is documented, never a promise or guarantee.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
