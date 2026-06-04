# External Go-Live Requirements (out of repo) — متطلبات الإطلاق الخارجي

> These items live **outside** this repository and must be completed **manually**
> before ANY real external sending. This repository remains draft-only regardless.
> هذه العناصر خارج المستودع ويجب تنفيذها يدويًا قبل أي إرسال حقيقي.

This repository (the Commercial Launch OS) never sends anything. It generates
review-only drafts. To move from "approved draft" to "manual send", the founder
must first complete everything below — outside this repo.

## Email deliverability — جاهزية البريد

Google and other major mailbox providers require authenticated, well-reputed
senders. Before sending:

- [ ] Domain DNS configured — تهيئة DNS للنطاق
- [ ] **SPF** record
- [ ] **DKIM** signing
- [ ] **DMARC** policy
- [ ] **Google Postmaster Tools** monitoring
- [ ] Bounce tracking — تتبع الارتداد
- [ ] Suppression process — قائمة منع
- [ ] Unsubscribe handling — معالجة إلغاء الاشتراك
- [ ] **Warm-up / ramp plan** — رفع الإرسال تدريجيًا
- [ ] Sender reputation monitoring — keep spam rate well **below 0.30%**

> Large senders must authenticate with SPF/DKIM/DMARC, monitor reputation, ramp
> gradually, and avoid reaching a spam rate of 0.30% or higher.

## Commercial / operations — التجاري والتشغيلي

- [ ] Manual CRM sheet or CRM pipeline (for tracking only, never auto-send)
- [ ] Calendly (or equivalent) for booking
- [ ] Payment / checkout (if applicable)
- [ ] Manual approval owner named — مالك الاعتماد البشري
- [ ] Reply / suppression logging process

## Legal & privacy — القانوني والخصوصية

- [ ] Privacy policy
- [ ] Terms
- [ ] DPA (Data Processing Agreement) for business customers
- [ ] PDPL alignment (KSA Personal Data Protection Law)
- [ ] Incident / complaint handling process

## Channel-specific — حسب القناة

- [ ] WhatsApp: customer number + explicit opt-in on file (no opt-in = no-go)
- [ ] LinkedIn: manual sending only — no automation, no scraping
- [ ] Website forms: manual human submission only — no auto-submit

## Gate / البوابة

Until every box above is checked **and** the founder approves, the status of
external sending remains **NO-GO**. The draft factory may continue running — it
only ever produces review-only drafts.
