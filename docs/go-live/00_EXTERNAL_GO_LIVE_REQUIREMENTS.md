# External Go-Live Requirements — متطلبات الإطلاق الخارجي

What must be true before Dealix sends a single external message. Going live is gated: email infrastructure, suppression, privacy/legal, payment/booking, and incident handling must all pass before the first manual send.

ما يجب أن يكون صحيحًا قبل أن يرسل ديليكس أي رسالة خارجية. الإطلاق مشروط: البنية البريدية، والاستبعاد، والخصوصية والقانون، والدفع والحجز، ومعالجة الحوادث — كلها تجتاز قبل أول إرسال يدوي.

## Governing rule — القاعدة الحاكمة

**AI drafts, ranks, and recommends. Founder reviews, approves, and sends manually. The system never sends externally.**

Go-live makes manual sending safe; it never enables automated external sending.

## Readiness gates — بوّابات الجاهزية

| # | Gate | Document | Status |
|---|---|---|---|
| 1 | Domain & email auth | [01_DOMAIN_EMAIL_READINESS.md](01_DOMAIN_EMAIL_READINESS.md) | [ ] |
| 2 | Manual outreach ramp | [02_MANUAL_OUTREACH_RAMP.md](02_MANUAL_OUTREACH_RAMP.md) | [ ] |
| 3 | Suppression process | [03_SUPPRESSION_PROCESS.md](03_SUPPRESSION_PROCESS.md) | [ ] |
| 4 | Privacy & legal | [04_PRIVACY_LEGAL_READINESS.md](04_PRIVACY_LEGAL_READINESS.md) | [ ] |
| 5 | Payment & booking | [05_PAYMENT_BOOKING_READINESS.md](05_PAYMENT_BOOKING_READINESS.md) | [ ] |
| 6 | Incident & complaint | [06_INCIDENT_AND_COMPLAINT_PROCESS.md](06_INCIDENT_AND_COMPLAINT_PROCESS.md) | [ ] |

All six must be checked before the first external message. A failed gate blocks go-live.

## Hard stops — توقفات صارمة

- No send before SPF, DKIM, and DMARC pass and are verified.
- No send to any address on the suppression list.
- No send before the privacy policy, terms, and DPA are published and reviewed.
- No automated external send, ever — every send is a manual action after founder approval.
- No scraping, no purchased lists, no cold WhatsApp automation, no LinkedIn automation.

## Channel boundary — حدود القناة

Business email and explicitly opted-in channels only. WhatsApp boundary: [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md). Channel policy: [../05_governance_os/CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md).

## Forbidden — ممنوع

No "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", or fabricated urgency in any outbound material.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
