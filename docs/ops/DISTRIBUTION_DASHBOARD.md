# Dealix — Distribution Dashboard — لوحة التوزيع اليومية
<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** ما لا يُقاس لا يُدار. سجّل اللوحة كل يوم تشغيل — رقم واحد
> فارغ أصدق من رقم مُجمَّل. أي خانة بلا بيان = `insufficient_data`، لا تخمين.

> **تنبيه — لا ضمانات.** هذا المستند يسدّ **البند 3 من سجل الفجوات** في
> [`DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md`](../DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md).
> هو scorecard يومي لقمع التوزيع. كل الأرقام أهداف تشغيلية لا ضمانات تجارية.

---

## 1) الغرض · Purpose

موجز يومي واحد يجيب: هل تحرّك قمع التوزيع اليوم؟ أين العالق؟ ما أولوية الغد؟
يُجمَّع أسبوعياً في [`meetings/WEEKLY_OPERATING_REVIEW.md`](../meetings/WEEKLY_OPERATING_REVIEW.md).

```text
رسائل ──▶ متابعات ──▶ ردود ──▶ demos ──▶ scopes ──▶ فواتير ──▶ مدفوع ──▶ Proof Packs
                                                                              │
                              محادثات شركاء · leads affiliate · مخاطر محجوبة ──┘
```

---

## 2) بطاقة النتائج اليومية · Daily Scorecard

تُملأ مرّة كل يوم تشغيل. القيمة الافتراضية لأي خانة غير معلومة = `insufficient_data`.

| المقياس · Metric | اليوم | ملاحظة |
|------------------|-------|--------|
| رسائل مُرسَلة · Messages sent | | تواصل دافئ موافَق عليه فقط |
| متابعات · Follow-ups | | متابعة واحدة مهذّبة لكل lead |
| ردود · Replies | | ردود حقيقية لا إيصالات قراءة |
| demos مُجراة · Demos | | مكالمة 12 دقيقة |
| scopes مُقدَّمة · Scopes | | عرض نطاق Sprint |
| فواتير مُرسَلة · Invoices sent | | روابط دفع Moyasar |
| مدفوع · Paid | | حدث `invoice_paid` |
| Proof Packs مُسلَّمة · Proof packs delivered | | حزمة 14 قسماً |
| محادثات شركاء · Partner conversations | | محادثات وكالات/شركاء |
| leads من affiliate · Affiliate leads | | إحالات بإفصاح ([الحوكمة](../growth/AFFILIATE_GOVERNANCE.md)) |
| مخاطر محجوبة · Blocked risks | | ما يوقف القمع اليوم (مثل Moyasar غير مُفعَّل) |
| أفضل رسالة · Best message | | أعلى رسالة تحويلاً اليوم |
| أسوأ قناة · Worst channel | | أدنى قناة عائداً اليوم |
| أولوية الغد · Tomorrow's priority | | إجراء واحد محدّد للغد |

---

## 3) قواعد التشخيص · Diagnostic Rules

اقرأ القمع لا الخانة المفردة. عند تحقّق نمط، طبّق التغيير ثم أعد القياس 5–7 أيام.

| النمط الملحوظ · Pattern | التشخيص | الإجراء |
|--------------------------|----------|---------|
| **7 أيام بلا ردود** | الشريحة أو الرسالة خاطئة | غيّر الشريحة المستهدفة أو الرسالة — لا تزد الحجم |
| **ردود لكن بلا demos** | الـCTA ضعيف أو غامض | غيّر الـCTA؛ اجعله طلباً واحداً واضحاً |
| **demos لكن بلا مدفوع** | العرض أو السعر أو الإثبات لا يُقنع | غيّر العرض/السعر/الإثبات — راجع Sample Proof Pack |
| **مخاطر محجوبة مستمرّة** | قيد بنيوي (مثل Moyasar) | صعّد للمؤسس فوراً — القمع متوقّف حتى الحلّ |
| **أسوأ قناة تتكرّر 5 أيام** | القناة لا تستحقّ الوقت | أوقف القناة مؤقتاً، ضاعف القناة الأعلى عائداً |

> Read the funnel, not the cell. A pattern over 5–7 days triggers one change at
> a time — then re-measure. No number presented as a guarantee.

---

## 4) الإيقاع · Cadence

- **يومياً:** املأ بطاقة النتائج في نهاية يوم التشغيل.
- **أسبوعياً:** جمّع الأرقام السبعة في [`WEEKLY_OPERATING_REVIEW.md`](../meetings/WEEKLY_OPERATING_REVIEW.md)؛
  راجع قواعد التشخيص وقرّر تغييراً واحداً.
- **حدود:** هذه اللوحة تقيس فقط — كل إرسال خارجي وفاتورة يبقى موافقة-أولاً عبر المؤسس.

---

## فهرس مراجع الريبو — Repo Cross-reference Index

| الموضوع | الملف المعتمد |
|---------|----------------|
| سجل الفجوات الأصلي (البند 3) | [DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md](../DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md) |
| المراجعة التشغيلية الأسبوعية | [meetings/WEEKLY_OPERATING_REVIEW.md](../meetings/WEEKLY_OPERATING_REVIEW.md) |
| الخطة الأم (الجزء G — المقاييس) | [MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md](../MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md) |
| خطة عمليات الإيراد والمال | [REVENUE_OPS_AND_MONEY_PLAN.md](../REVENUE_OPS_AND_MONEY_PLAN.md) |
| حوكمة الـAffiliate | [growth/AFFILIATE_GOVERNANCE.md](../growth/AFFILIATE_GOVERNANCE.md) |
| خطة 90 يوم التنفيذية | [90_DAY_BUSINESS_EXECUTION_PLAN.md](../90_DAY_BUSINESS_EXECUTION_PLAN.md) |

---

*Version 1.0 | Closes Gap #3 of the Distribution Gap Register | Daily
distribution-funnel scorecard | Measure-only — sends stay approval-first | No
guaranteed claims | Missing data = insufficient_data.*
