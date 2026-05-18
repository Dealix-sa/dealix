# Dealix — Launch Gates Checklist (للتنفيذ الفوري)

**القاعدة:** لا توجد "launch partial". إما كل الـ gates مغلقة أو الـ launch غير مكتمل.
**المدة المتوقعة:** 2-4 ساعات من وقتك الفعلي، موزّعة على 72 ساعة.

**Doctrine:** This checklist conforms to [`../MONEY_LADDER.md`](../MONEY_LADDER.md)
and [`../NARRATIVE_STANDARD.md`](../NARRATIVE_STANDARD.md). The launch sells
Rung 0 (Free Revenue Diagnostic) → Rung 1 (499 SAR 7-Day Revenue Intelligence
Sprint). There is no "1 SAR pilot". Payment is verified in Moyasar test mode
only — no live charge is created for verification.

---

## Gate 1 — Backend Deploy (10 دقائق)

### الخطوات:
- [ ] افتح `https://railway.com/project/54bb60b4-d059-4dd1-af57-bc44c702b9f0`
- [ ] اختر خدمة `dealix`
- [ ] Settings → Deploy → Start Command → **اتركه فارغاً** (أو اكتب `/app/start.sh`)
- [ ] Variables → Raw Editor → الصق محتوى `dealix_railway_vars.txt` من workspace
- [ ] احفظ
- [ ] انتظر Deploy Status = `Active` (2-3 دقائق)
- [ ] Settings → Networking → Generate Public Domain

### Definition of Done:
```bash
curl https://<your-domain>.up.railway.app/api/v1/pricing/plans
# يجب أن يرجع: JSON مع plans (Starter, Growth, Scale)
```

**إذا Failed:** أرسل screenshot من Railway Deployments → Logs

---

## Gate 2 — Moyasar Webhook (5 دقائق)

### الخطوات:
- [ ] افتح `https://dashboard.moyasar.com/webhooks`
- [ ] اضغط `+ Add Webhook`
- [ ] **URL:** `https://<your-domain>.up.railway.app/api/v1/webhooks/moyasar`
- [ ] **Events:** اختر `payment_paid`, `payment_failed`, `payment_refunded`
- [ ] **Secret:** انسخ قيمة `MOYASAR_WEBHOOK_SECRET` من `dealix_railway_vars.txt`
- [ ] احفظ
- [ ] Send Test Event من Moyasar

### Definition of Done:
- [ ] Test event في Moyasar يظهر `Delivered`
- [ ] Railway logs تظهر `moyasar webhook received`

---

## Gate 3 — Test-Mode Payment Verification (15 دقائق)

**الهدف:** التحقق من مسار الدفع→التسليم بالكامل في **وضع اختبار Moyasar فقط**.
لا تُنشئ أي رسوم حقيقية للتحقق. السعر الحيّ المعروض على العملاء هو **Sprint
إثبات الإيراد بـ 499 ريالًا** (الدرجة 1 في [`../MONEY_LADDER.md`](../MONEY_LADDER.md)).
سعر الـ "1 ريال" القديم مُلغى ولا يُستخدم في أي اختبار أو تسويق.

### الخطوات:
- [ ] تأكد أن مفاتيح Moyasar في الـ env هي مفاتيح **test mode** (تبدأ بـ `test_`).
- [ ] أنشئ invoice اختباري للدرجة 1 (Sprint 499 SAR) عبر checkout في وضع الاختبار.
- [ ] افتح رابط الدفع في المتصفح.
- [ ] ادفع ببطاقة Moyasar test:
  - Card: `4111 1111 1111 1111`
  - CVV: `123`
  - Expiry: `12/30`
  - OTP: `1234`
- [ ] ارجع وتحقق من وصول الـ webhook ومن تسجيل العملية.

### Definition of Done:
- [ ] Payment يظهر في Moyasar dashboard في وضع الاختبار (status: `paid`).
- [ ] Webhook event في Railway logs (`moyasar webhook received`).
- [ ] Record جديد للعملية في DB (سأعطيك SQL للفحص).
- [ ] `payment_succeeded` event في PostHog.
- [ ] لا توجد أي رسوم حقيقية — كل ما سبق في وضع الاختبار.

**ملاحظة:** قبل أول عميل حقيقي، يُحوَّل Moyasar إلى live mode، وتُطبَّق فوترة
50/50 على الدرجة 1 (نصف عند البدء، نصف عند تسليم Proof Pack).

**إذا الـ DB check غير ممكن من الواجهة:** OK، نعتمد على Moyasar + Webhook logs فقط للـ MVP.

---

## Gate 4 — Monitoring (45 دقيقة)

### PostHog Verification (15 دقيقة):
- [ ] افتح `https://app.posthog.com` (أو self-hosted)
- [ ] تأكد project key نفسه في `POSTHOG_PROJECT_KEY` env var
- [ ] من Railway logs، تأكد أن الـ backend يرسل events
- [ ] شاهد "Live events" في PostHog — يجب ظهور events كل دقائق

### Sentry Verification (15 دقيقة):
- [ ] افتح `https://sentry.io`
- [ ] Trigger خطأ عمداً (مثلاً: `curl <domain>/api/v1/nonexistent`)
- [ ] تحقق Sentry استلم الخطأ
- [ ] أنشئ Alert Rule: Email me on any 5xx error

### UptimeRobot Setup (15 دقيقة):
- [ ] أنشئ حساب مجاني على `https://uptimerobot.com`
- [ ] Add Monitor:
  - Type: HTTPS
  - URL: `https://<your-domain>.up.railway.app/health`
  - Interval: 5 دقائق
- [ ] أضف Alert Contacts: Email + SMS
- [ ] Send Test Alert

### Definition of Done:
- [ ] PostHog: يظهر live events من الـ backend
- [ ] Sentry: alert email وصل لبريدك
- [ ] UptimeRobot: test alert وصل على الجوال

---

## Gate 5 — First Real Lead (20 دقيقة)

### الخطوات:
- [ ] افتح `dealix_personalized_messages.md`
- [ ] اقرأ الرسالة المخصصة لـ **عبدالله العسيري / Lucidya**
- [ ] افتح LinkedIn
- [ ] ابحث عن: `Abdullah Asiri Lucidya`
- [ ] افتح profile → Connect → Add a note
- [ ] الصق الرسالة (مع قراءتها مرة أخيرة)
- [ ] اضغط Send
- [ ] سجّل في tracking sheet:

### Tracking Sheet Format:
```
| # | التاريخ | الشركة | الاسم | القناة | الحالة | ملاحظات |
|---|---------|---------|-------|---------|---------|----------|
| 1 | 2026-04-24 | Lucidya | عبدالله العسيري | LinkedIn | Sent | قرابة الاسم |
```

### Definition of Done:
- [ ] LinkedIn يُظهر ✓✓ (double check mark = delivered)
- [ ] الرسالة في tracking sheet
- [ ] Calendar reminder: Follow up after 3 days if no reply

---

## كل شي مُغلق — Launch Status: LIVE

بعد إكمال الـ 5 gates:

### ما تحقق:
- Backend يقبل traffic حقيقي
- مسار الدفع→التسليم مُتحقَّق منه في وضع الاختبار
- Monitoring + Alerting نشط
- أول رسالة outreach مُرسلة يدويًا من المؤسس
- Pipeline بدأ على الدرجة 0 → الدرجة 1 (Sprint 499 ريالًا)

### ما يجب أن يحدث تلقائياً:
- كل lead جديد → PostHog event
- كل error → Sentry + Email
- كل downtime → UptimeRobot SMS
- كل payment → Moyasar webhook → DB

### الخطوة التالية الأوتوماتيكية:
- اليوم 1: انتظر رد عبدالله
- اليوم 2: أرسل للـ 2 التاليين (Ahmad Al-Zaini, Nawaf Hariri)
- اليوم 3-4: أرسل للـ 2 الأخيرين (Hisham Al-Falih, Ibrahim Manna)
- اليوم 5-7: متابعة لمن لم يرد

---

## إذا علقت في أي gate

أرسل لي:
1. **رقم الـ gate** (1-5)
2. **Screenshot من الـ error**
3. **وصف ما جربته**

أحلّها خلال دقائق.

---

## Final Rule

**لا تقل "Dealix launched" قبل الـ 5 gates كلها مُغلقة.**

Pre-launch = الحالة الحالية
Launching = الآن وأنت تنفّذ
Launched = كل الـ 5 gates DONE

**إذا ما نفّذت هذه في 72 ساعة:** لا يوجد حجة.
إما هناك blocker تقني حقيقي (نحلّه) أو تسويف (يجب مواجهته).

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
