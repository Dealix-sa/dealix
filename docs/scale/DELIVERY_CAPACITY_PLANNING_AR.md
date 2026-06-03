# تخطيط طاقة التسليم
# Delivery Capacity Planning

---

## المبدأ — Principle

لا نقبل Sprint جديد إذا كانت الطاقة ممتلئة. التسليم السيئ أسوأ من رفض الفرصة.

We do not accept a new Sprint if capacity is full. Poor delivery is worse than declining an opportunity.

---

## نموذج الطاقة الأساسي — Base Capacity Model

### طاقة Sprint واحد

| نوع Sprint | وقت التنفيذ (ساعات) | وقت المراجعة (ساعات) | إجمالي ساعات المؤسس |
|-----------|-------------------|---------------------|---------------------|
| Sprint 499 (رتبة 2) | 3–5 ساعات | 1–2 ساعات | 4–7 ساعات |
| Data Intelligence Pack (رتبة 3) | 5–7 ساعات | 1–2 ساعات | 6–9 ساعات |
| Sprint Managed Ops شهري (رتبة 4) | 8–12 ساعة/شهر | 2–4 ساعات/شهر | 10–16 ساعة/شهر |

### الحد الأقصى الشهري (Solo Founder)

| الحالة | الطاقة المتاحة | الحد الأقصى |
|--------|--------------|------------|
| Solo Founder فقط | ~80 ساعة/شهر إنتاجية | 5–8 Sprints شهرياً |
| Solo + وكيل واحد مُفوَّض | ~120 ساعة/شهر | 10–12 Sprint شهرياً |
| فريق صغير (2–3 أشخاص) | ~240 ساعة/شهر | 20–25 Sprint شهرياً |

---

## معيار الرفع — When to Add Resources

رفع الطاقة عند تحقق شرطين في آن واحد:

**الشرط الأول — الطلب:**
- 3 Sprints مرفوضة في شهر واحد بسبب طاقة ممتلئة
- Delivery Health Score ينخفض تحت 75 بسبب الحمل الزائد

**الشرط الثاني — الاستقرار:**
- Delivery Health Score ≥ 80 لشهرين متتاليين
- Agent Governance Score ≥ 90 باستمرار
- 3 عملاء Managed Ops نشطين على الأقل (إيراد متكرر ثابت)

**لا ترفع الطاقة** إذا لم يتحقق الشرط الثاني — النمو قبل الاستقرار يُفسد الجودة.

---

## قرار القبول أو الرفض — Accept/Decline Decision

لكل Sprint مقترح جديد، أجب على هذه الأسئلة:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
قرار القبول — Capacity Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

الساعات المتاحة هذا الأسبوع: ___ ساعة
الساعات المحجوزة (Sprints نشطة): ___ ساعة
الساعات المتبقية: ___ ساعة

Sprint المقترح يحتاج: ___ ساعة

هل الطاقة كافية؟
[ ] نعم — اقبل Sprint
[ ] لا — ادرس الخيارات أدناه

الخيارات:
[ ] تأجيل Sprint بأسبوعين (أخبر العميل الآن)
[ ] رفض وتوصية ببديل
[ ] قبول جزئي (تقليص نطاق بموافقة العميل)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## جدول الطاقة الأسبوعي — Weekly Capacity Dashboard

```
الأسبوع: _______________

الساعات الإنتاجية المتاحة: ___ ساعة
(المُستخدَم للحلقة اليومية والإدارة: ~10 ساعة)
(المتبقي للتسليم الفعلي: ___ ساعة)

Sprints النشطة:
1. [اسم Sprint] — العميل: ___ — ساعات متبقية: ___
2. [اسم Sprint] — العميل: ___ — ساعات متبقية: ___
3. [اسم Sprint] — العميل: ___ — ساعات متبقية: ___

إجمالي المحجوز: ___ ساعة
المتاح لـ Sprint جديد: ___ ساعة

الحالة: [ ] متاح  [ ] شبه ممتلئ  [ ] ممتلئ — لا قبول جديد
```

---

## مراجعة الطاقة الشهرية — Monthly Capacity Review

التقرير: `reports/scale/DELIVERY_CAPACITY_REVIEW.md`

يتضمن:
- الطاقة الإجمالية مقابل الطاقة المستخدمة
- نسبة الاستخدام (Utilization Rate)
- عدد Sprints المرفوضة بسبب الطاقة
- قرار: هل حان وقت رفع الطاقة؟

---

## الوثائق المرتبطة — Related Documents

- [`docs/finance/STARTER_SPRINT_MARGIN_MODEL_AR.md`](../finance/STARTER_SPRINT_MARGIN_MODEL_AR.md)
- [`reports/scale/DELIVERY_CAPACITY_REVIEW.md`](../../reports/scale/DELIVERY_CAPACITY_REVIEW.md)
- [`reports/delivery/DELIVERY_PIPELINE_STATUS.md`](../../reports/delivery/DELIVERY_PIPELINE_STATUS.md)
- [`docs/operating_factory/ROLE_OWNERSHIP_AR.md`](../operating_factory/ROLE_OWNERSHIP_AR.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
