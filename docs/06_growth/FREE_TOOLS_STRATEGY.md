# Free Tools Strategy — Dealix Self-Growth OS

أقوى تكتيك توزيع طويل المدى: **Free Tool Moat** — أداة مجانية صغيرة حول
كل ألم. كل أداة تنتج: **lead + score + recommended offer**، وتقود إلى
**CTA واحد**.

> المصدر الحي للأدوات: [`data/growth/free_tools.json`](../../data/growth/free_tools.json).
> توليد المواصفات: `python3 scripts/growth/generate_free_tool_specs.py`
> → [`reports/growth/FREE_TOOL_SPECS.md`](../../reports/growth/FREE_TOOL_SPECS.md).

---

## لماذا الأدوات المجانية تبيع بدون أن تبيع

العميل يدخل بياناته، يرى **score منخفض**، فيبيع نفسه لنفسه. الخسارة
المحسوبة أقوى من أي وصف. هذا product-led growth حتى لو الخدمة عالية اللمس.

---

## الأدوات (الطبقة المجانية)

| الأداة | الهدف | المخرج | CTA |
|---|---|---|---|
| Business OS Score | جذب عام | score 0–100 + top 3 leaks + next step | ابدأ تشخيص Dealix |
| Revenue Leakage Calculator | نية شرائية | تقدير خطر شهري/سنوي | احصل على Revenue Leakage Score |
| Proof Gap Audit | تموضع الإثبات | Proof Readiness Score | احصل على Proof Register خلال Command Sprint |
| WhatsApp Follow-up Risk Score | ألم واتساب | risk score + top leak | ابدأ تشخيص Dealix |
| AI Governance Checklist | تمييز بالثقة | governance score + open risks | ابدأ تشخيص Dealix |
| Delivery Visibility Score | ألم التسليم | visibility score + top gap | ابدأ تشخيص Dealix |

### مثال مخرج Business OS Score

```
Business OS Score: 42/100
Top 3 leaks:
1. Follow-up leakage
2. Proof gap
3. Command fog
Recommended next step: Dealix Command Sprint
```

### مثال Revenue Leakage Calculator

```
50 فرصة شهريًا × 5,000 ريال × 10% leakage = 25,000 ريال خطر شهري
```

> لا نقول «نضمن نرجعها». نقول: **«هذا تقدير خطر تشغيلي يحتاج تحقق.»**

---

## قواعد الحوكمة (claims guard)

كل أداة في `free_tools.json` تحمل حقل `claims_guard`. القواعد:

- لا benchmark صناعي معروض إلا إذا كان **مصدره موثّق**.
- النتيجة **self-reported** وتُوسم كتقدير.
- لا صياغة «إيراد مضمون قابل للاسترجاع».
- لا cold WhatsApp automation ضمن أداة واتساب — نشخّص فجوة operating rhythm فقط.
- لا ادعاء شهادة/امتثال في AI Governance Checklist.
- كل صفحة نتيجة: **CTA واحد** + disclaimer ثنائي اللغة.

---

## بنية صفحة الأداة

1. عنوان الألم.
2. المدخلات (قصيرة — أقل احتكاك = إكمال أعلى).
3. النتيجة الفورية (score + leaks).
4. الخطوة التالية الموصى بها (offer واحد).
5. التقاط البريد (اختياري) لإطلاق nurture (انظر `NURTURE_SEQUENCES.md`).
6. CTA واحد.

---

## دورة حياة الأداة

```
Visitor → Free Score → Personalized Result → Sample Command Pack
→ Book Diagnostic → Command Sprint
```

كل إكمال أداة = lead في القمع (انظر `WEBSITE_FUNNEL_MAP.md`) وقد يُطلق
تسلسل تربية حسب الـ score (≥70 → diagnostic؛ 40–69 → nurture).

---

## كيف نضيف أداة جديدة

1. أضف عنصرًا في `data/growth/free_tools.json` (slug, name_ar/en, goal,
   route, inputs, output, primary_cta, recommended_offer, claims_guard).
2. شغّل `generate_free_tool_specs.py` للتحقق من ظهورها في التقرير.
3. مرّر النسخة النهائية للصفحة على فحص الادعاءات قبل النشر.
