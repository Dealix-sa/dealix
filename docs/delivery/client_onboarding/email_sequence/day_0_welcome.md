# Day 0 — Welcome email (bilingual)

> **Doctrine:** This is a draft template, not an auto-send. Render through
> `core/email/invites.py` pattern; founder approves before delivery.

**Merge fields:** `{{customer_name}}`, `{{company_name}}`, `{{sprint_id}}`,
`{{kickoff_url}}`, `{{founder_name}}`, `{{calendly_url}}`.

---

## Subject (AR primary, EN secondary)
- AR: مرحبًا بك في Dealix · انطلاقة Sprint السبع أيام
- EN: Welcome to Dealix — your 7-day Sprint kickoff

---

## Body — Arabic

أهلًا {{customer_name}}،

نشكرك على ثقتك في Dealix. تم تأكيد طلب Sprint السبع أيام لشركة **{{company_name}}**
(رقم الـ Sprint: `{{sprint_id}}`).

**ما الذي يحدث الآن؟**

1. **اليوم 0–1:** مكالمة kickoff قصيرة (٢٠ دقيقة) لمراجعة الأهداف. احجز
   الموعد المناسب: [{{calendly_url}}]({{calendly_url}}).
2. **اليوم 1:** سترسل لنا قائمة بمصادر البيانات (CSV عملاء، CRM export،
   أو تكامل HubSpot). تفاصيل في رسالة اليوم 1.
3. **اليوم 3:** نشاركك معاينة Top-10 prospects + Data Quality Report.
4. **اليوم 5:** drafts proof pack أولية + رسائل outreach للمراجعة.
5. **اليوم 7:** Proof Pack نهائي ثنائي اللغة + توصيات subscription.

**التزاماتنا الصريحة:**
- كل رسالة خارجية تمر بموافقتك أولًا — لا إرسال تلقائي.
- بياناتك تخضع لـ PDPL السعودي ولا نشاركها مع أي طرف ثالث بدون
  اتفاقية DPA موقعة.
- كل رقم في Proof Pack مدعوم بحدث في الـ proof ledger — لا أرقام
  مخترعة.

للأسئلة العاجلة: WhatsApp مباشر مع {{founder_name}}.

شكرًا،
{{founder_name}}
Dealix

---

## Body — English

Hello {{customer_name}},

Thank you for choosing Dealix. Your 7-day Sprint for **{{company_name}}**
is confirmed (Sprint ID: `{{sprint_id}}`).

**What happens now?**

1. **Day 0–1:** Kickoff call (20 min) to align on goals. Book a slot:
   [{{calendly_url}}]({{calendly_url}}).
2. **Day 1:** We'll request your data sources (customer CSV, CRM export,
   or HubSpot connection). Details in the Day 1 email.
3. **Day 3:** You'll preview the top-10 prospect ranking + a Data
   Quality Report.
4. **Day 5:** Draft proof pack + outreach drafts for your review.
5. **Day 7:** Final bilingual Proof Pack + subscription
   recommendations.

**Our explicit commitments:**
- Every outbound message passes your approval — no autonomous sends.
- Your data is governed by Saudi PDPL and is never shared without a
  signed DPA.
- Every number in the Proof Pack ties to a recorded proof-ledger event
  — no invented figures.

For urgent questions: direct WhatsApp with {{founder_name}}.

Thanks,
{{founder_name}}
Dealix

---

## Internal review checklist (before send)

- [ ] `customer_name` + `company_name` merged from CustomerRecord
- [ ] `sprint_id` from sprint_runner.start
- [ ] `kickoff_url` resolves
- [ ] `calendly_url` is valid + matches founder's availability
- [ ] No invented metrics added
- [ ] Saved draft via `core.email.invites.send_invite_email`
- [ ] Founder explicit approval before send
