# Diagnostic Delivery — تسليم التشخيص

The Audit tier (SAR 499–2,500). Its job is to demonstrate methodology and surface evidenced opportunities — not to make outcome claims. Operational runbook detail lives in [03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md); this document is the offer-level contract.

التشخيص هو أول درجة في السُّلَّم. وظيفته إثبات المنهجية وكشف فرص مُثبتة بأدلة، لا إطلاق وعود.

## Inputs — المدخلات

- Completed intake: company, sector, city, named workflow owner.
- One business question the client wants answered.
- A data sample owned by the client (CRM export or CSV — never scraped, never a list Dealix sourced externally).
- Languages required (AR, EN, or both).

## Outputs — المخرجات

- A bilingual diagnostic: problem framing, hypothesis tree, two to four evidenced opportunities, and one recommended next step.
- A Source Passport stub describing the data handled.
- A Pilot proposal sized to the findings.

## Timeline — الجدول الزمني

- Audit (499): 7 days.
- Extended diagnostic (up to 2,500): 10 working days.
- One mid-point check-in with the workflow owner.

## Acceptance criteria — معايير القبول

Delivered only when: Source Passport stub exists; founder approval is logged; bilingual file is sent; the engagement record is set to `diagnostic_delivered`. Anything less is in-flight.

## Human approval boundary — حدود الموافقة البشرية

The diagnostic is `draft_only` until the founder explicitly approves it via the governance ledger. No external send precedes that approval.

## Security boundary — حدود الأمان

Client data is used for diagnostic purposes only (`allowed_use=diagnostic_only`), retained 30 days by default, and contains no PII in the delivered body — counts, not names. See [04_data_os/ALLOWED_USE_POLICY.md](../04_data_os/ALLOWED_USE_POLICY.md).

## Handover — التسليم

PDF + editable Markdown, AR first. Includes the evidenced-opportunities list, the methodology used, and explicit limitations. See [06_HANDOVER_TEMPLATE.md](06_HANDOVER_TEMPLATE.md).

## Upsell path — مسار الترقية

Diagnostic → Pilot. The recommended next step in the diagnostic is always a scoped Pilot, never a vague "let's talk." See [07_EXPANSION_PLAYBOOK.md](07_EXPANSION_PLAYBOOK.md).

## Retainer trigger — مُحفِّز الاشتراك الشهري

A diagnostic does not trigger a retainer directly. It can flag a retainer candidate when the finding is "this is a recurring workflow problem, not a one-time fix" — that note carries forward to the Pilot.

## Client success metrics — مقاييس نجاح العميل

- Time to delivery (target: within the committed window).
- Number of evidenced opportunities surfaced.
- Diagnostic-to-Pilot conversion (tracked, never promised).
- Client confirmation that the business question was answered.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
