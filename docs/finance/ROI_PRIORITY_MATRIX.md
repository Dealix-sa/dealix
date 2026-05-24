# ROI Priority Matrix

A score-based rubric the CEO uses to rank any spend or hour-bet above a
threshold. Drives the bucket calls in
[CAPITAL_ALLOCATION_SYSTEM](CAPITAL_ALLOCATION_SYSTEM.md).

This matrix records intent only and never commits to payment terms.

## When to use

- Any cash spend > 2,000 SAR/month
- Any contractor engagement
- Any new automation project longer than one week of CEO time
- Any partnership requiring written commitments
- Any campaign with a budget over 1,000 SAR

## Scoring dimensions (1–5 each)

| Dimension | 1 | 5 |
|---|---|---|
| **Revenue impact within 90 days** | No clear path | Direct line to paid pipeline |
| **Leverage on CEO time** | Costs me hours | Removes hours, returns them as Move |
| **Compounding** | One-off benefit | Builds an asset that compounds (data, brand, proof) |
| **Reversibility** | Hard to reverse without cost | Reversible within a week, low cost |
| **Trust risk** | Could break a non-negotiable | Strengthens trust posture |

## Score interpretation

- **Total ≥ 20** — Approve, allocate
- **Total 15–19** — Approve as a time-boxed test with a kill-trigger
- **Total < 15** — Decline, or rework until ≥ 15

## Recording

Every ROI-matrix run that results in a decision is appended to
[`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md)
with `expected_outcome` and `kill_trigger`.

## Cross-references

- [CAPITAL_ALLOCATION_SYSTEM](CAPITAL_ALLOCATION_SYSTEM.md)
- [FOUNDER_HOUR_ROI](FOUNDER_HOUR_ROI.md) — pricing CEO time as input to the Leverage dimension
- [HIRE_VS_AUTOMATE_VS_PARTNER](HIRE_VS_AUTOMATE_VS_PARTNER.md) — three-way comparison framework
- [`docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`](../founder/STRATEGIC_ASSUMPTIONS_REGISTER.md) — backing assumptions

## Non-negotiables

The matrix records intent only and is never used to commit to refunds,
discounts, or payment terms with customers. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
