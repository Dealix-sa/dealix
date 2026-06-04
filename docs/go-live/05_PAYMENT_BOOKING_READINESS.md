# Payment & Booking Readiness — جاهزية الدفع والحجز

The booking and payment path a client uses to schedule a diagnostic and pay for an offer. It must work end to end, in SAR, before go-live.

مسار الحجز والدفع الذي يستخدمه العميل لجدولة تشخيص ودفع قيمة العرض. يجب أن يعمل من البداية للنهاية، بالريال، قبل الإطلاق.

## Booking — الحجز

- A booking link (e.g., Calendly or equivalent) for diagnostics and discovery calls.
- Confirmation and reminder emails are sent from the authenticated domain. See [01_DOMAIN_EMAIL_READINESS.md](01_DOMAIN_EMAIL_READINESS.md).
- Booking confirmations are transactional, not outreach; still authenticated and logged.
- Time zone set correctly for Saudi clients.

## Payment / checkout — الدفع

- A checkout path priced in SAR that maps to the offer ladder.
- Invoicing for higher tiers (Pilot, Department OS, Retainer, Enterprise).
- Clear statement of what is included and excluded before payment.

## Offer ladder prices (SAR) — أسعار سُلَّم العروض

| Offer | Range |
|---|---|
| Audit / Diagnostic | 499–2,500 |
| Pilot | 5,000–25,000 |
| Department OS | 25,000–150,000 |
| Retainer | 3,000–25,000 / month |
| Enterprise | 150,000+ |

Prices shown to the client must match the signed scope. No surprise charges.

## Receipts and records — الإيصالات والسجلات

- Every payment generates a receipt and a record linked to the engagement.
- Realized revenue is recorded as `realized_revenue_sar` per [../analytics-os/01_EVENT_TAXONOMY.md](../analytics-os/01_EVENT_TAXONOMY.md).
- Refund/cancellation terms are stated in the terms of service.

## Go-live checklist — قائمة الإطلاق

- [ ] Booking link live, confirmations sending from the authenticated domain.
- [ ] Checkout works in SAR for the Audit tier.
- [ ] Invoicing ready for higher tiers.
- [ ] Inclusions/exclusions shown before payment.
- [ ] Receipts generate and link to the engagement.
- [ ] Refund/cancellation terms published.

## Boundaries — الحدود

Booking confirmations are transactional. Any non-transactional outreach still follows the manual-send, founder-approval rule. No fabricated urgency in pricing or booking copy.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
