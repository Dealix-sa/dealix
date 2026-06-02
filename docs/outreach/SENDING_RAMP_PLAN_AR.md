# خطة الإحماء التدريجي للإرسال
# Sending Ramp Plan — Warmup Schedule

**الجمهور:** المؤسس + مشغّل البنية التحتية  
**المرجع التقني:** `auto_client_acquisition/email/deliverability_check.py` · `auto_client_acquisition/email/compliance.py`  
**الوثائق ذات الصلة:** [EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md) · [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) · [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md)

---

## ١. لماذا الإحماء التدريجي ضروري

نطاق الإرسال الجديد ليس له سمعة لدى مزوّدي البريد الإلكتروني. الإرسال المفاجئ بأعداد كبيرة يُشغّل مرشّحات الـ spam ويُلحق ضرراً بالسمعة يصعب تعافيها في أسابيع. الإحماء التدريجي يبني الثقة مع مزوّدي البريد عبر الوقت بإثبات أن المستلمين يتفاعلون بإيجابية.

**المبدأ الثابت:** 250 مسوّدة/يوم مسموحة في جميع المراحل. الإرسال الفعلي يتدرّج حسب صحة النطاق وأداء المقاييس.

---

## ٢. مخطط الإحماء الأسبوعي

| المرحلة | الأسبوع | المسوّدات اليومية | الإرسال الفعلي اليومي | الشرط للانتقال |
|---|---|---|---|---|
| صفر — هوية فقط | الأسبوع 0 | 250 | 0 – 20 (اختبار) | DNS جاهز + قائمة استثناء + إلغاء اشتراك + موافقة مؤسس |
| واحد — إحماء خفيف | الأسبوع 1 | 250 | 25 – 50 | bounce أقل من 3% + spam أقل من 0.1% + لا تحذيرات مزوّد |
| اثنان — إحماء متوسط | الأسبوع 2 | 250 | 50 – 100 | bounce أقل من 2% + spam أقل من 0.1% + رد إيجابي يتحسّن |
| ثلاثة — توسّع محكوم | الأسبوع 3 | 250 | 100 – 150 | bounce أقل من 2% + spam أقل من 0.1% + unsubscribe مُراقَب |
| أربعة — اكتمال | الأسبوع 4 | 250 | 150 – 250 | **فقط إذا كانت جميع المقاييس صحيّة** — انظر البوابة أدناه |

**تحذير:** 250 إرسالاً فعلياً/يوم ليس هدفاً تلقائياً. الوصول إليه مشروط بجميع بوابات الصحة في الأسبوع الرابع.

---

## ٣. بوابات الصحة — Health Gates

### ٣.١ بوابات الانتقال بين المراحل

يجب اجتياز **جميع** البنود للانتقال إلى المرحلة التالية:

| المقياس | الأسبوع 0→1 | الأسبوع 1→2 | الأسبوع 2→3 | الأسبوع 3→4 |
|---|---|---|---|---|
| معدل الارتداد | أقل من 5% | أقل من 3% | أقل من 2% | أقل من 2% |
| معدل الشكاوى | أقل من 0.3% | أقل من 0.1% | أقل من 0.1% | أقل من 0.1% |
| تحذيرات مزوّد البريد | لا يوجد | لا يوجد | لا يوجد | لا يوجد |
| معدل إلغاء الاشتراك | مُراقَب | مُراقَب | أقل من 1% | أقل من 0.5% |
| معدل الرد الإيجابي | لا يُشترط | مُراقَب | تحسّن مرئي | أعلى من 1% |
| موافقة المؤسس على كل دُفعة | مطلوبة | مطلوبة | مطلوبة | مطلوبة |
| صحة DNS (SPF/DKIM/DMARC) | صالح | صالح | صالح | صالح |
| نطاق التتبع | نشط | نشط | نشط | نشط |

### ٣.٢ بوابة الأسبوع الرابع — اكتمال الإحماء

الانتقال إلى 250 إرسالاً/يوم يتطلب إضافةً للبوابات السابقة:

- لا ارتداد صلب خلال آخر 7 أيام يتجاوز 1%
- لا تحذير نشط من Google Postmaster أو Outlook Postmaster
- معدل الشكاوى ثابت تحت 0.1% لمدة 14 يوماً متتاليين
- المؤسس يُوافق صراحةً على الانتقال إلى 250 إرسالاً

---

## ٤. ما يُوقف الإحماء أو يُعيده للوراء — Pause / Rollback

### توقف فوري — Immediate Pause

يوقف الإرسال فوراً في أي مرحلة إذا حدث أي من:

- معدل ارتداد يتجاوز 5% في دُفعة واحدة
- معدل شكاوى يتجاوز 0.3% في يوم واحد
- تحذير نشط من مزوّد البريد (Gmail Postmaster أو Outlook)
- إيقاف تعليق نطاق الإرسال من مزوّد DNS أو البريد
- رسائل bounce جماعية تشير إلى خطأ في التهيئة

### تراجع للمرحلة السابقة — Rollback

يعود الإرسال لحد المرحلة السابقة إذا:

- ارتفع معدل الارتداد بنسبة 50% أو أكثر عن المرحلة الحالية
- ارتفع معدل الشكاوى فوق 0.1% لأكثر من 3 أيام متتالية
- أصبح معدل إلغاء الاشتراك أعلى من 1% في أسبوع واحد

### استئناف بعد التوقف

- حدّد وعالج السبب الجذري
- انتظر 48 ساعة بعد المعالجة
- أعد فحص DNS وقائمة الاستثناء بالكامل
- استأنف من حد المرحلة السابقة وليس المرحلة الحالية

---

## ٥. مرحلة الصفر — التهيئة الأساسية

قبل إرسال أي رسالة فعلية، حتى 20 رسالة اختبارية:

- [ ] SPF صالح على `mail.dealix.me`
- [ ] DKIM صالح على `selector._domainkey.mail.dealix.me`
- [ ] DMARC صالح على `_dmarc.mail.dealix.me` (ليس `p=none`)
- [ ] نطاق التتبع `track.dealix.me` نشط ومختبر
- [ ] ترويسة `List-Unsubscribe` + `List-Unsubscribe-Post` تعمل
- [ ] قائمة استثناء نشطة في `compliance.py`
- [ ] معالجة الارتداد مُفعَّلة
- [ ] Google Postmaster Tools مُسجَّل للنطاق
- [ ] موافقة المؤسس الصريحة مُسجَّلة في `approval_center`
- [ ] 20 رسالة اختبارية أُرسلت وتحققنا من وصولها (وليس spam folder)

---

## ٦. مراقبة يومية خلال الإحماء

خلال فترة الإحماء، راجع يومياً:

| المقياس | أين تجده | ما تبحث عنه |
|---|---|---|
| معدل الارتداد | Google Postmaster Tools | أقل من 5% |
| معدل الشكاوى | Google Postmaster Tools | أقل من 0.1% |
| Inbox placement | Postmaster أو أداة بديلة | تحسّن متواصل |
| الردود الإيجابية | [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) | نمو تدريجي |
| حجم قائمة الاستثناء | [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md) | لا ارتفاع مفاجئ |
| تحذيرات مزوّد البريد | لوحة تحكم مزوّد البريد | صفر تحذيرات |

---

## EN Mirror — Sending Ramp Plan

**Audience:** Founder and infrastructure operator

### Why Warmup Matters

A new sending domain has no reputation with inbox providers. Sending large volumes from day one triggers spam filters and creates reputational damage that can take weeks to reverse. The warmup schedule builds provider trust incrementally.

### Ramp Schedule

- **Week 0:** 0–20 live sends/day (identity test only). All DNS, suppression, unsubscribe, and approval gates must pass before any live send.
- **Week 1:** 25–50/day. Gates: bounce < 3%, spam < 0.1%, no provider warnings.
- **Week 2:** 50–100/day. Gates: bounce < 2%, spam < 0.1%, positive reply rate improving.
- **Week 3:** 100–150/day. Gates: bounce < 2%, spam < 0.1%, unsubscribe monitored.
- **Week 4:** 150–250/day. ONLY if all Week 3 gates pass AND no bounce spike AND spam complaint stable below 0.1% for 14 consecutive days AND founder explicitly approves the volume increase.

250 live sends/day is not an automatic target. It requires all Week 4 health gates to pass.

### What Pauses or Rolls Back the Ramp

Immediate pause: single-batch bounce > 5%, daily spam complaint > 0.3%, any active provider warning, or domain suspension.  
Rollback to prior level: sustained bounce increase of 50%+, spam complaint above 0.1% for 3+ consecutive days, unsubscribe rate above 1% in a single week.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
