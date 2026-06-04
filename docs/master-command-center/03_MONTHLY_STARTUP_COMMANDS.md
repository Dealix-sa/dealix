# مراجعة وقرارات شهرية | Monthly Review & Scaling Decisions

## الغرض | Purpose

**عربي:** يحدد هذا الملف المراجعة الشهرية وقرارات التوسّع في Dealix. مرة كل شهر يتراجع المؤسس خطوة للخلف لتقييم الأداء الكلي واتخاذ القرارات الكبرى: التسعير، التوظيف، التوسّع في قطاع جديد، أو الإطلاق الإعلاني. كل قرار يبقى للمؤسس، وكل تنفيذ خارجي يدوي وبموافقة، ولا إطلاق إعلانات مدفوعة حية تلقائيًا.

**English:** This file defines the monthly review and scaling decisions in Dealix. Once a month the founder steps back to assess overall performance and make the big calls: pricing, hiring, expanding into a new vertical, or launching ads. Every decision stays with the founder, every external action is manual and approved, and there is no automatic live paid-ads launch.

---

## المبدأ الحاكم | Governing Principle

> الذكاء الاصطناعي يُجهّز، المؤسس يوافق، الإجراء يدوي فقط، لا إرسال خارجي تلقائي.
> AI prepares, Founder approves, Manual action only, No automated external sending.

---

## تسلسل المراجعة الشهرية | Monthly Run Sequence

```bash
# 1) صورة الإيراد التراكمي (تشغيل لوحة الإيراد بنطاق شهري)
python scripts/founder_revenue_dashboard.py

# 2) أحدث تقرير مجلس + اتجاه شهري
python scripts/weekly_board_report_generate.py

# 3) موجز ذكاء السوق للشهر
python scripts/market_intelligence_brief_generate.py

# 4) التحقق الشامل من مركز القيادة وأدلته
python scripts/master_startup_command_verify.py
```

---

## محاور المراجعة | Review Dimensions

| المحور Dimension | السؤال Question |
|---|---|
| الإيراد Revenue | هل ينمو بثبات؟ ما الاتجاه؟ |
| التسليم Delivery | هل الجودة والمواعيد مستقرة؟ |
| السعة Capacity | هل الطلب يفوق طاقتي الحالية؟ |
| الإثبات Proof | هل لدي حالات حقيقية موثّقة (بإذن)؟ |
| المخاطر Risk | أي حوادث في `crisis-os`؟ |

---

## قرارات التوسّع | Scaling Decisions

| القرار Decision | متى نعم When Yes | متى لا When No |
|---|---|---|
| رفع السعر Raise price | طلب يفوق السعة + إثبات قيمة | تحويل ضعيف |
| توظيف Hire | تسليم متكرر يتجاوز طاقة المؤسس | تدفق غير مستقر |
| قطاع جديد New vertical | قطاع حالي مستقر ومربح | القطاع الحالي غير ناضج |
| إطلاق إعلان Ad launch | قناة عضوية مثبتة + ميزانية مخصصة | لا إثبات تحويل |

> قرار الإعلان: تخطيط فقط حتى اعتماد المؤسس؛ لا إطلاق مدفوع حي تلقائيًا.

---

## مخرجات المراجعة الشهرية | Monthly Outputs

- قرار تسعير موثّق (إن وُجد).
- قرار توظيف/توسّع موثّق (إن وُجد).
- تحديث الذاكرة التشغيلية بالدروس (`operating-memory-os`).
- تحديث جاهزية التوسّع (`scale-readiness-os`).

---

## حدود السلامة | Safety Boundaries

- لا إطلاق إعلانات مدفوعة حية دون اعتماد صريح. No live paid-ads without approval.
- لا أرقام وهمية ولا ضمان عائد في أي مراجعة. No fake traction / guaranteed ROI.
- لا إرسال آلي، لا كشط، لا أسرار في المخرجات. No automated sending, scraping, or secrets.

> القرارات الكبرى تُسجّل في تقرير الأدلة وتُراجع في الشهر التالي.
