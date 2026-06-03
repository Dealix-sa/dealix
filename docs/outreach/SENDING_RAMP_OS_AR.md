# نظام تشغيل الإرسال التدريجي
# Sending Ramp Operating System

**الجمهور:** المؤسس + مشغّل مسار الإرسال  
**المراجع التقنية:** `auto_client_acquisition/email/compliance.py` · `auto_client_acquisition/channel_policy_gateway/email.py` · `auto_client_acquisition/safe_send_gateway/doctrine.py` · `auto_client_acquisition/approval_center/`  
**الوثائق ذات الصلة:** [SENDING_RAMP_PLAN_AR.md](SENDING_RAMP_PLAN_AR.md) · [FOUNDER_APPROVAL_QUEUE_AR.md](FOUNDER_APPROVAL_QUEUE_AR.md) · [EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md)  
**التقارير:** `reports/outreach/SENDING_BATCH_PLAN.md` · `reports/outreach/DOMAIN_HEALTH_REVIEW.md` (يُولَّدان تلقائياً — غير موجودَين بعد)

---

## ١. مبدأ الدُّفعات المتدرّجة

**لا إرسال جماعي (bulk send) في أي مرحلة.**  
الدُّفعات الصغيرة المتباعدة زمنياً تُقلّل المخاطر وتُتيح التدخّل السريع عند ظهور مشكلة.

كل إرسال خارجي يمرّ بثلاث بوابات متسلسلة:

```
(1) بوابة الامتثال — compliance.py → check_outreach()
        ↓ allowed=True فقط
(2) بوابة القناة — channel_policy_gateway/email.py
        ↓ live_gate_true=True + human_approved=True فقط
(3) بوابة الإرسال الآمن — safe_send_gateway/middleware.py → enforce_consent_or_block()
        ↓ is_safe_to_send=True فقط
إرسال الرسالة
```

---

## ٢. حقول `sending_batch`

كل دُفعة إرسال مُسجَّلة بالحقول التالية:

```
sending_batch {
  batch_id        -- معرّف فريد للدُّفعة (مثال: batch_20260602_001)
  account         -- معرّف حساب البريد المُستخدَم
  domain          -- نطاق الإرسال (مثال: mail.dealix.me)
  sector          -- القطاع المستهدف (مثال: real_estate, automotive)
  sequence_step   -- رقم خطوة التسلسل (1 = الرسالة الأولى، 2 = المتابعة، ...)
  batch_size      -- عدد الرسائل في الدُّفعة
  risk_level      -- low | medium | high | blocked
  approved_at     -- طابع زمني موافقة المؤسس
  send_window     -- نافذة الإرسال (مثال: 09:00-12:00 AST)
  status          -- pending | approved | sending | sent | paused | cancelled
}
```

---

## ٣. بوابة "لا تُرسِل إذا" — DO NOT SEND IF

يتوقف الإرسال تلقائياً إذا انطبق أي مما يلي:

| الشرط | المصدر |
|---|---|
| لا يوجد رابط إلغاء اشتراك في نص الرسالة | `compliance.py → append_opt_out_line()` |
| لا توجد موافقة مؤسس مُسجَّلة | `approval_center` → `status != approved` |
| الرسالة تفتقر إلى تخصيص — اسم مستلم أو شركة غائبان | فحص نص المسوّدة |
| المستلم في قائمة الاستثناء | `compliance.py → email_suppressed / domain_suppressed` |
| المستلم ألغى الاشتراك سابقاً | `compliance.py → contact_opt_out_true` |
| نطاق الإرسال في حالة `blocked` أو `founder_action_needed` | `deliverability_check.py → overall_status` |
| ارتفاع الارتداد فوق 5% في الدُّفعة الأخيرة | مراجعة تلقائية بعد كل دُفعة |
| معدل الشكاوى يتجاوز 0.3% خلال 24 ساعة | Google Postmaster مراقبة |
| الوقت خارج نافذة الإرسال المحددة | `send_window` في سجل الدُّفعة |
| `risk_level=blocked` على أي مسوّدة في الدُّفعة | `compliance.py → risk_score > 50` |

---

## ٤. نوافذ الإرسال المُوصى بها

نوافذ الإرسال مُحسَّنة لساعات النشاط السعودية وتجنّب ساعات الذروة:

| النافذة | التوقيت (بتوقيت الرياض) | ملاحظة |
|---|---|---|
| الصباح | 09:00 – 12:00 | موصى به للرسائل الأولى |
| بعد الظهر | 14:00 – 17:00 | موصى به للمتابعات |
| ممنوع | 20:00 – 08:00 | ساعات الهدوء — `quiet_hours_active=True` |
| يوم الجمعة | 13:00 – 15:00 | تجنّب — وقت الصلاة |
| يوم السبت والأحد | إرسال مخفَّض | النشاط التجاري أقل |

`safe_send_gateway/middleware.py` يرفع `SendBlocked(reason_code="quiet_hours")` خارج هذه النوافذ.

---

## ٥. حدود الإرسال لكل نطاق

| مرحلة الإحماء | الحد اليومي لكل نطاق | حجم الدُّفعة الواحدة | الفاصل الزمني بين الدُّفعات |
|---|---|---|---|
| 0 (اختبار) | 20 | 5 – 10 | 120+ دقيقة |
| 1 | 50 | 10 – 15 | 90+ دقيقة |
| 2 | 100 | 15 – 25 | 90+ دقيقة |
| 3 | 150 | 20 – 30 | 90+ دقيقة |
| 4 (مكتمل) | 250 | 25 – 50 | 90+ دقيقة |

`compliance.py` يفرض `batch_cooldown` عند `seconds_since_last_batch < (INTERVAL_MIN_DEFAULT * 60)` حيث `INTERVAL_MIN_DEFAULT=90`.

---

## ٦. التحقق من التخصيص قبل الإرسال

الرسائل غير المُخصَّصة (plain template بدون تعديل) لا تُرسَل. الحد الأدنى للتخصيص:

- اسم الشركة المستهدفة حاضر في النص
- لا استخدام لـ `{{first_name}}` أو `{{company_name}}` كـ placeholders غير مُعبَّأة
- موضوع الرسالة يشير إلى القطاع أو نشاط الشركة

---

## ٧. تسلسل الخطوات قبل الإرسال

المؤسس يُنجز هذا التسلسل قبل كل دُفعة:

1. افتح `reports/outreach/DOMAIN_HEALTH_REVIEW.md` — تأكد أن `health_status=healthy`
2. افتح `reports/outreach/SENDING_BATCH_PLAN.md` — راجع الدُّفعة المقترحة
3. قرّر على كل مسوّدة في [FOUNDER_APPROVAL_QUEUE_AR.md](FOUNDER_APPROVAL_QUEUE_AR.md)
4. وافق على الدُّفعة في `approval_center` → `status=approved`
5. حدّد `send_window` في سجل الدُّفعة
6. النظام يُرسل خلال النافذة المحددة — لا إرسال يدوي إضافي مطلوب

---

## ٨. إجراء ما بعد الإرسال

بعد كل دُفعة مُرسَلة:

- راجع الارتدادات خلال 4 ساعات
- راجع الردود في [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md)
- حدّث `email_account.health_status` إذا تغيّرت المقاييس
- إذا تجاوزت الارتدادات 5% → أوقف الدُّفعات التالية فوراً وأعلم المؤسس

---

## EN Mirror — Sending Ramp Operating System

**Audience:** Founder and outbound pipeline operators

### Graduated Batches, Not Bulk

Every live send passes three sequential gates:
1. `compliance.py → check_outreach()` — compliance gate
2. `channel_policy_gateway/email.py` — requires `live_gate_true=True` and `human_approved=True`
3. `safe_send_gateway/middleware.py → enforce_consent_or_block()` — final consent gate

### Sending Batch Fields

Each batch is recorded with: `batch_id`, `account`, `domain`, `sector`, `sequence_step`, `batch_size`, `risk_level`, `approved_at`, `send_window`, `status`.

### DO NOT SEND IF

The send is blocked if any of the following are true: no unsubscribe link in message body; no founder approval on record; no personalization (placeholder fields unfilled); recipient in suppression list; recipient previously opted out; sending domain status is `blocked` or `founder_action_needed`; last-batch bounce rate above 5%; spam complaint rate above 0.3% in last 24 hours; send window has not opened or has closed; `risk_level=blocked` on any draft in the batch.

### Send Windows

Recommended: 09:00–12:00 and 14:00–17:00 Riyadh time. Blocked: 20:00–08:00 (quiet hours). `safe_send_gateway` raises `SendBlocked(reason_code="quiet_hours")` outside active windows.

### Per-Domain Daily Caps by Ramp Stage

See the table in Section 5. The 90-minute minimum batch interval is enforced in `compliance.py` via `batch_cooldown`.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
