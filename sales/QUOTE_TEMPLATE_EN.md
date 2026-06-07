# Dealix Quote — Template (English)

<!--
Filled by scripts/generate_quote.py or manually.
Fields in {{ }} are replaced automatically.
Governance note: this is a DRAFT — not sent to the client until founder approval (gates G03/G04).
-->

**Client:** {{ client_name }}
**Date:** {{ date }}
**Quote ID:** {{ quote_id }}
**Valid until:** {{ valid_until }}
**Prepared by:** Dealix

---

## 1) Problem We Solve

{{ problem_statement }}

## 2) Proposed Scope

{{ scope_summary }}

## 3) Phases & Pricing

| Phase | Description | Price (SAR, ex-VAT) |
|---|---|---|
{{ line_items }}

**Subtotal (ex-VAT):** {{ subtotal }} SAR
**VAT (15%):** {{ vat_amount }} SAR
**Total (incl. VAT):** {{ total_with_vat }} SAR

> Prices are exclusive of 15% VAT unless stated otherwise (ZATCA).

## 4) Monthly Subscription (Managed OS)

| Item | Details |
|---|---|
| Package | {{ subscription_package }} |
| Monthly fee | {{ monthly_fee }} SAR |
| Included usage | {{ usage_included }} |
| Usage overage | {{ usage_overage }} |
| Minimum term | {{ min_term_months }} months |

> The system does not end at launch — data, users, and operations keep changing. Every Production engagement is tied to a monthly operating plan covering monitoring, improvement, support, and tuning.

## 5) Payment Terms

- On signature: 50%
- After MVP / Pilot: 30%
- On launch: 20%
- Subscription: monthly in advance — minimum {{ min_term_months }} months — setup billed separately.

## 6) Deliverables & Acceptance

{{ deliverables }}

## 7) Risks & Assumptions

{{ assumptions }}

## 8) Next Step

{{ next_step }}

---

<!-- guardrail: margin verified against os/config/margin_guardrails.yml -> {{ margin_check }} -->
*This quote is an internal draft until founder approval and formal delivery.*
