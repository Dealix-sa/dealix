# Dealix — Daily Operating Loop / حلقة التشغيل اليومية

<!-- Owner: Founder | Cadence: every working day (Sun–Thu) | Status: canonical daily loop -->
<!-- Arabic primary · English secondary -->

> **القاعدة:** شغّل هذه الحلقة كل يوم عمل (الأحد–الخميس) — 3–4 ساعات تركيز.
> ابدأ من **القرارات**، لا من صندوق الوارد.
>
> **Rule:** Run this loop every working day (Sun–Thu) — 3–4 focused hours. Start from **decisions**, not the inbox.

**الحالة الصريحة / Honest baseline:** 0 عملاء يدفعون · الإيراد محجوب حتى اكتمال Moyasar KYC · المسار اليدوي للدفع جاهز (`MANUAL_PAYMENT_SOP.md`) فلا يضيع عميل قال «نعم».

---

## الصباح / Morning (08:00–11:00)

### 08:00 — فحص الأنظمة / Systems check (10 min)
- [ ] GitHub Actions healthcheck يمرّ؟ (آخر تشغيل خلال 15 دقيقة) / passing within 15 min?
- [ ] `web-dealix.up.railway.app/healthz` يرجع 200 في المتصفح؟ / returns 200?
- [ ] أي إشعارات دفع/ردود في بريد المؤسس؟ / any payment or reply notifications?

### 08:10 — فحص CEO اليومي / Daily CEO check (10 min)
شغّل الأسئلة الخمس من [`../operating_rhythm/DAILY_CEO_CHECK.md`](../operating_rhythm/DAILY_CEO_CHECK.md):
أعلى فرصة إيراد · أعلى خطر تسليم · أعلى خطر حوكمة · أي proof يتحسّن · ما لا يستحق الوقت اليوم.

### 08:20 — مراجعة الـ pipeline / Pipeline review (15 min)
- [ ] افتح `docs/ops/pipeline_tracker.csv`
- [ ] كل صف فيه `next_followup ≤ today` → جهّز المتابعة / queue the follow-up
- [ ] أي عميل دفع → انقله إلى قائمة الـ onboarding

### 08:35 — دفعة التواصل الدافئ / Warm outreach batch (2 hrs)
> دكترين: **لا outreach بارد**. كل لمسة دافئة (معرفة سابقة / إحالة / موافقة)، أو تمرّ عبر طابور الموافقة.
- [ ] افتح `docs/ops/launch_content_queue.md` + قائمة الـ 50 الدافئة
- [ ] أرسل 5 رسائل دافئة (من leads الأولوية)
- [ ] أرسل 5 متابعات (يوم +2 / +5 / +10)
- [ ] أرسل 2 رسالة شريك وكالة / agency partner
- [ ] حدّث الـ tracker بـ `sent_at` لكل واحدة

---

## منتصف اليوم / Midday (11:00–14:00)

### 11:00 — معالجة الردود / Reply handling (continuous)
- [ ] رُدّ على كل ردّ خلال 30 دقيقة في ساعات العمل
- [ ] احجز Free Diagnostic عبر رابط Calendly (Rung 0)
- [ ] سجّل «Replied» → «Diagnostic Booked» في الـ tracker

### 12:00 — التشخيص المجاني / Free diagnostics (if booked)
- [ ] اقرأ ملف العميل 10 دقائق قبل المكالمة
- [ ] اتبع سكربت التشخيص: `docs/FIRST_3_DIAGNOSTIC_SCRIPT.md`
- [ ] اختم دائمًا بعرض **Rung 1 — 7-Day Revenue Proof Sprint 499 SAR**
- [ ] بعد المكالمة: أرسل فاتورة Moyasar مستضافة أو تفاصيل التحويل (`MANUAL_PAYMENT_SOP.md`)

### 13:00 — فحص الدفع / Payment check
- [ ] راجع الحساب البنكي + إشعارات STC Pay
- [ ] دفعة وصلت؟ → حدّث الـ tracker + ابدأ الـ onboarding (`CUSTOMER_ONBOARDING_DAY_BY_DAY.md`)

---

## بعد الظهر / Afternoon (14:00–17:00)

### 14:00 — المحتوى / Content (Sun / Tue / Thu)
- [ ] انشر منشورًا واحدًا من `launch_content_queue.md`
- [ ] تفاعل مع 10 حسابات مستهدفة (تعليق / إعجاب)

### 15:00 — حركة الشركاء / Partner motion
- [ ] أرسل 2–3 رسائل وكالة دافئة
- [ ] رُدّ على أي استفسار شريك + حدّث عمود الـ tracker

### 16:00 — تجهيز الغد / Prep for tomorrow
- [ ] أي 10 leads للغد؟ ابحث وخصّص الرسائل
- [ ] احجز خانات التشخيص في التقويم

---

## المساء / Evening (17:00–18:00)

### 17:00 — لوحة النتائج اليومية / Daily scorecard
عبّئ كتلة «Day N» في [`daily_scorecard.md`](daily_scorecard.md) — أرقام صلبة فقط، لا انطباعات.

### 17:30 — تحسين / Improve
- [ ] رسالة حصلت على 0 ردود في 10 إرسالات؟ → أعد كتابتها
- [ ] رسالة حصلت على ردود متعددة؟ → ضاعِف استخدامها

### 18:00 — توقّف / STOP
أغلق اللابتوب. التعافي = استراتيجية.

---

## أهداف 7 أيام / 7-Day target

| اليوم / Day | لمسات / Touches | متابعات / Follow-ups | تشخيص / Diagnostics | مدفوع / Paid 499 |
|-------------|-----------------|----------------------|---------------------|------------------|
| 1 | 10 | 0 | 0 | 0 |
| 2 | 10 | 3 | 0 | 0 |
| 3 | 10 | 3 | 1–2 | 0 |
| 4 | 10 | 5 | 1–2 | 0 |
| 5 | 10 | 5 | 2 | 0–1 |
| 6 (جزئي) | 5 | 5 | 1 | 0–1 |
| 7 | إجازة | 0 | 0 | 0 |
| **الأسبوع** | **55** | **21** | **5–7** | **0–1** |

**النتيجة الواقعية للأسبوع 1 / Realistic Week-1 outcome:** أول Sprint 499 مُغلق أو مجدول (Day 7 هدف خطة الـ 90 يوم).

---

## أهداف 30 / 60 / 90 يوم — مُوحّدة مع خطة الـ 90 يوم

> الأرقام هنا **مطابقة** لـ [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md) — لا تستخدم أرقامًا أخرى.
> هذه أهداف تشغيلية، **لا ضمانات**.

| المقياس / Metric | يوم 30 / Day 30 | يوم 60 / Day 60 | يوم 90 / Day 90 |
|------------------|-----------------|-----------------|-----------------|
| تشخيصات / Diagnostics (تراكمي) | 6 | 12 | 20 |
| Pilots مدفوعة (499) | ~2–3 | 5 | 10 |
| Proof Events موثقة | 3 | 8 | 15 |
| عملاء Managed Ops (Rung 3 retainer) | 0 | 2 | 3 |
| MRR (SAR) | ~998 | ~5,998 | ~8,997–14,997 |
| Case studies منشورة | 1 | 2 | 3 |

تفاصيل المعالم الكاملة في [`POST_LAUNCH_SCORECARD.md`](POST_LAUNCH_SCORECARD.md) §«30/60/90 Milestone Scorecard».

---

## إشارات الاختناق / Bottleneck signals

عالِج أضيق نقطة في القمع أولًا:

- معدل الرد < 2% → أعد كتابة الافتتاحية
- حجز تشخيص < 20% من الردود → اختصر الطلب
- حضور التشخيص < 60% → أضف تأكيدًا قبل 24 ساعة
- إغلاق Sprint < 10% → أصلح سكربت التشخيص أو السعر
- اكتمال الدفع < 60% → بسّط الـ checkout (بعد تفعيل Moyasar)

---

## الأسبوعي / Weekly handoff

كل أسبوع، تتغذّى مخرجات هذه الحلقة في **الاجتماع التشغيلي الأسبوعي**:
[`../operating_rhythm/WEEKLY_OPERATING_MEETING.md`](../operating_rhythm/WEEKLY_OPERATING_MEETING.md)
(3 قرارات CEO · 3 التزامات · 1 مخاطرة مُخفّضة · 1 proof مُقوّى · 1 شيء مُوقَف · مراجعة friction log).
</content>
