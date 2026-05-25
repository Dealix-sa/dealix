---
title: Payment Rules
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Payment Rules — قواعد الدفع

## Purpose
Define accepted payment methods, advance percentages, and refund triggers. Designed for KSA SME and enterprise customers.

## Accepted methods

| Method | Notes |
|---|---|
| SAR bank transfer (local) | Default. Mada / SARIE. IBAN provided on invoice. |
| KSA payment gateways | HyperPay, Moyasar, PayTabs. Used for online / card payments. |
| Cheque (SAR) | Accepted on exception only; cleared funds before delivery starts. |
| International wire | Exception only; FX risk and bank fees on client. |

Not accepted: cash, crypto, gift instruments, payment-on-delivery without prior agreement.

## Advance percentages

| Engagement | Advance |
|---|---|
| Sprint | 50% |
| Pilot | 100% |
| Retainer | 100% of monthly fee, in advance |
| Strategic engagement | Per SOW; floor 30% |

## Refund triggers
Refund eligible (full or partial, see [`REFUND_POLICY.md`](REFUND_POLICY.md)):
- Dealix cancels engagement before any deliverable is started.
- Proven service-level breach with no remediation within agreed window.
- Documented misrepresentation in proposal (caught by client).

Not refund eligible:
- Client withdraws after delivery has begun, mid-sprint.
- Output does not lead to client's downstream sales outcome (estimated value is not Verified value).
- Change of strategy on client side.

## Rules
- No work begins until advance cleared in the Dealix account.
- Late payment on retainer pauses delivery from day 8 of overdue, with written notice on day 1 and day 5.
- All payments reconciled within 5 business days of receipt.
- Receipts issued automatically after clearance.

## Operations
- IBAN, gateway links, and pay-to instructions live in `docs/finance/payment_instructions.md` (created on first commercial deal).
- Reconciliation against the invoice register per [`INVOICE_WORKFLOW.md`](INVOICE_WORKFLOW.md).

## Evidence
- Bank statement and gateway export retained.
- Receipt issued and linked to invoice.

## Owner & cadence
- Owner: Founder.
- Cadence: per payment; weekly reconciliation.

## Cross-links
- [`BILLING_POLICY.md`](BILLING_POLICY.md)
- [`REFUND_POLICY.md`](REFUND_POLICY.md)
- [`INVOICE_WORKFLOW.md`](INVOICE_WORKFLOW.md)

---

## القسم العربي

**الوسائل المقبولة:** تحويل بنكي محلي بالريال (افتراضي)، بوابات سعودية (HyperPay/Moyasar/PayTabs)، شيك بالريال (استثناء بعد التحصيل)، تحويل دولي (استثناء).

**غير مقبول:** نقد، عملات رقمية، دفع عند التسليم بدون اتفاق مسبق.

**نسب المقدّم:** سبرنت 50%، تجريبي 100%، Retainer 100% مسبقًا شهريًا، عقد استراتيجي حسب SOW وبحد أدنى 30%.

**محفّزات الاسترداد:** ديلكس تلغي قبل بدء أي مخرج، خرق مستوى خدمة موثق بدون معالجة، تحريف موثق في الاقتراح. لا استرداد إذا انسحب العميل بعد بدء التسليم أو إذا لم يقد المخرج لمبيعات لاحقة (القيمة التقديرية ليست مُتحقَّقة).

**القواعد:** لا عمل قبل وصول المقدّم. تأخر retainer يوقف التسليم من اليوم الثامن مع إشعار في 1 و5.

**المالك:** المؤسس.
