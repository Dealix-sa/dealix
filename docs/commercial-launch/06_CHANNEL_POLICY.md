# Channel Policy — سياسة القنوات

> Draft-only. Founder approves. Nothing is sent automatically from this repository.
> مسودات فقط. المؤسس يعتمد. لا شيء يُرسل تلقائيًا من هذا المستودع.

This policy is enforced in code by `config/commercial_channels.json`, the
quality/compliance gates, and `scripts/commercial_safety_audit.py`.

---

## Email — البريد الإلكتروني

- ✅ Draft generation only — توليد مسودات فقط.
- ❌ No SMTP. ❌ No send API. ❌ No bulk sending. ❌ No automatic sequence sending.
- Every draft **must** contain an opt-out line — كل مسودة يجب أن تتضمن خيار إيقاف.
- Before ANY real manual send, the following must exist (out of repo):
  - SPF, DKIM, DMARC
  - Google Postmaster
  - bounce tracking
  - suppression list
  - unsubscribe handling
  - warm-up / ramp plan
  - founder approval

قبل أي إرسال يدوي فعلي يجب توفر SPF/DKIM/DMARC ومراقبة Postmaster وتتبع الارتداد
وقائمة منع وآلية إلغاء اشتراك وخطة إحماء تدريجية وموافقة المؤسس.

---

## LinkedIn — لينكدإن

- ✅ Manual draft only — مسودة يدوية فقط.
- ❌ No scraping. ❌ No bots. ❌ No auto-connect. ❌ No auto-message. ❌ No browser automation.
- The founder copies the message manually — المؤسس ينسخ الرسالة يدويًا فقط.

LinkedIn prohibits unauthorized automation for messaging or for adding/importing
contacts. We respect that fully.

---

## WhatsApp — واتساب

- ❌ No cold outreach — ممنوع التواصل البارد.
- ❌ No outbound automation — ممنوع الأتمتة الصادرة.
- ✅ Inbound / opt-in manual replies only — ردود يدوية على opt-in فقط.
- Any WhatsApp draft is `manual_review_only` — كل مسودة واتساب للمراجعة اليدوية فقط.
- Any number without explicit opt-in = **no-go** — أي رقم بدون opt-in = ممنوع.

WhatsApp requires the customer's number and clear opt-in. We never cold-message
on WhatsApp.

---

## Website / contact forms — نماذج المواقع

- ✅ Draft only — مسودة فقط.
- ❌ No auto-submit. ❌ No browser automation.
- A human copies and submits manually — شخص بشري ينسخ ويرسل يدويًا.

---

## Phone — الهاتف

- Manual only — يدوي فقط.
- ❌ No dialer. ❌ No auto-call. — لا اتصال آلي.

---

## Summary table / جدول ملخص

| Channel | Allowed | Forbidden |
|---------|---------|-----------|
| Email | draft + manual send | SMTP, API send, bulk, sequence automation |
| LinkedIn | manual draft | scraping, bots, auto-connect, auto-message, browser automation |
| WhatsApp | inbound / opt-in manual reply | cold outreach, outbound automation |
| Website form | draft | auto-submit, browser automation |
| Phone | manual call | dialer, auto-call |
