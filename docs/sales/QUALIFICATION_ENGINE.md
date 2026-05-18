# Qualification Engine — محرك التأهيل
<!-- Authoritative lead scoring. Canonical ladder: docs/OFFER_LADDER_AND_PRICING.md -->

**قبل** أي عرض سعر أو فتح ملف مشروع، شغّل هذا المحرك. العملاء غير المناسبين يستهلكون الوقت ويخفضون الجودة — أفضل المؤسسين يعرفون **لمن لا نبيع**.

**Run this before quoting or opening a project folder.** Bad-fit clients drain time and quality.

---

## 1. النقاط — Score (100 points)

| المعيار — Criterion | النقاط — Points |
|---------------------|----------------:|
| ألم واضح — Pain is clear and named | 20 |
| ميزانية / مسار شراء — Budget or a real buying path | 20 |
| صاحب قرار حاضر — Decision owner present | 15 |
| بيانات أو عملية موجودة — Data or process exists | 15 |
| يناسب ICP — Fits ICP (Saudi B2B SME, 5–50 staff, 500K–10M SAR revenue) | 15 |
| يقبل المراجعة / الموافقة — Accepts review + approval governance | 10 |
| لا يطلب ممنوعات — Wants safe methods (no scraping / spam / guarantees) | 5 |
| **المجموع — Total** | **100** |

The 8-question intake (`qualification.qualify(...)`) maps onto this rubric:
pain_clear, owner_present, data_available, accepts_governance, has_budget,
wants_safe_methods, proof_path_visible, retainer_path_visible.

---

## 2. نطاقات القرار — Decision bands

| النقاط — Score | القرار — Decision | الإجراء — Action |
|----------------|-------------------|------------------|
| **80–100** | ACCEPT — تابع | اعرض الدرجة المناسبة من السلم (عادةً Rung 1 — 499 SAR Sprint). |
| **60–79** | DIAGNOSTIC_ONLY | ابدأ بـ Free AI Ops Diagnostic؛ لا عرض مدفوع قبل التشخيص. |
| **40–59** | REFRAME / NURTURE | أعد صياغة النطاق أو ضع في المتابعة؛ لا عرض الآن. |
| **< 40** | REJECT / REFER_OUT | استبعد بأدب، أو حوّل لجهة أنسب. |

---

## 3. مستبعِدات فورية — Hard disqualifiers

أي واحد من هذه = REJECT بغض النظر عن النقاط:

- يطلب cold WhatsApp / أتمتة LinkedIn / scraping / قوائم مشتراة.
- يطلب ضمان مبيعات أو نتائج ("اضمنوا لي X صفقة").
- يطلب تجاوز الحوكمة (إرسال بدون موافقة، بيانات بلا سند).
- لا يوجد صاحب قرار ولا مسار وصول إليه.
- لا توجد بيانات ولا عملية يمكن البناء عليها.

**صياغة الرفض الآمن — Clean refusal:** "Dealix لا تقدّم [scraping / cold WhatsApp / أتمتة LinkedIn / ضمان مبيعات]. البديل الآمن هو [مخرجات draft-only / تواصل قائم على الموافقة / فرص مُثبتة بالأدلة]. أرغب أن أجهّز لك العرض البديل؟"

---

## 4. التسجيل — Recording

النتيجة + القرار يُسجَّلان في CRM / حقل القرار في
[`../operations/REQUEST_INTAKE_SYSTEM.md`](../operations/REQUEST_INTAKE_SYSTEM.md).

**تنبيه مزامنة:** هذا الملف هو المرجع الوحيد لتسجيل النقاط. [`QUALIFICATION_SCORE.md`](QUALIFICATION_SCORE.md) يشير إليه — حدّث هذا الملف فقط عند تغيير الأوزان.

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
