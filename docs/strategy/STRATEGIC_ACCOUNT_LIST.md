# Strategic Account List

The top-N accounts the CEO personally moves forward. Live data lives in
[`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv); this doc
defines selection criteria, cadence, and exit rules.

## Selection criteria

An account makes the list only if **all** of the following hold:

1. Inside the current beachhead sector ([BEACHHEAD_SECTOR_SCORECARD](BEACHHEAD_SECTOR_SCORECARD.md))
2. Real annual B2B revenue or budget that justifies the offer
3. Known decision-maker reachable through documented integration channels
4. No trust block (clean against approval-center policy checks)
5. Has a falsifiable hypothesis about why they would buy ([`docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`](../founder/STRATEGIC_ASSUMPTIONS_REGISTER.md))

## Cadence

- Monthly: re-select. Accounts that did not move are demoted out of the list.
- Weekly: 30 minutes during [`docs/revenue/PIPELINE_REVIEW_RHYTHM.md`](../revenue/PIPELINE_REVIEW_RHYTHM.md)
- Daily: brief surfaces any strategic account without a next step

## Exit rules

| Trigger | Action |
|---|---|
| No movement in 30 days | Demote to standard pipeline |
| Trust block discovered | Remove immediately; log decision |
| Outside refreshed beachhead | Demote, retain as future re-add candidate |
| Closed-won | Promote to expansion / proof program |
| Closed-lost | Run [`docs/revenue/WIN_LOSS_REVIEW.md`](../revenue/WIN_LOSS_REVIEW.md); decide re-add window |

## Cross-references

- [BEACHHEAD_SECTOR_SCORECARD](BEACHHEAD_SECTOR_SCORECARD.md)
- [`docs/revenue/CLOSE_PLAN_TEMPLATE.md`](../revenue/CLOSE_PLAN_TEMPLATE.md)
- [`docs/enterprise/STAKEHOLDER_MAP.md`](../enterprise/STAKEHOLDER_MAP.md)
- [`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv) — live data

## Non-negotiables

Outreach to listed accounts still flows through the approval-center gates.
Account selection is documented research, not random list-building. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
