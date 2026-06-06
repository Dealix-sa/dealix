# reports/delivery — Per-Customer Delivery Summaries

## What lives here

This directory holds per-customer delivery summaries: a short, generated rollup of what a Command Sprint or Managed Ops engagement delivered for one customer. It is the bridge between the customer workspace and the founder's reporting.

Each summary references:

- The customer workspace (`customers/<name>/`) it draws from.
- The delivery log (`09_delivery_log.md`) it summarizes.
- The proof pack (`10_proof_pack.md`) delivered, with its value tiers.
- Whether an upsell recommendation (`11_upsell_recommendation.md`) was queued — only if a real proof pack exists.

## How it is generated

A delivery summary is produced from the customer workspace files at the close of a sprint or monthly cycle. It is a read-only rollup; to change it, fix the underlying workspace file and regenerate. Proof and revenue events are logged to `data/revenue/*.jsonl`, which the revenue board reads.

## Rules

- Every observation carries its value tier; nothing is rounded up.
- No guaranteed return, conversion rate, or ROI stated as fact.
- No PII in the committed summary; anonymized labels only.
- An upsell appears here only when backed by a delivered proof pack.

## Related

- `docs/04_delivery/PAID_SPRINT_HANDOFF.md` — handoff into delivery.
- `docs/04_delivery/DELIVERY_DAILY_RHYTHM.md` — the daily cadence and delivery log.
- `docs/04_delivery/PROOF_TO_UPSELL_PLAYBOOK.md` — proof-to-upsell rule.
- `reports/revenue/README.md`, `reports/customers/README.md` — sibling report directories.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
