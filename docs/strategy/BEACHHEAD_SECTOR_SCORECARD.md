# Beachhead Sector Scorecard

Saudi B2B is many markets. We pick one beachhead first, prove the loop,
then expand. This scorecard tells us which sector is winning week by week.

## Candidate sectors (starting list)

| Sector | Signal source |
|---|---|
| ERP / CRM implementers | pipeline tracker `sector` column |
| Cybersecurity firms | pipeline tracker |
| B2B agencies | pipeline tracker |
| Consulting / digital transformation | pipeline tracker |
| Logistics / industrial services | pipeline tracker |
| SaaS / software vendors | pipeline tracker |
| Enterprise services | pipeline tracker |

## Scoring per sector (weekly)

| Dimension | Weight | Source |
|---|---|---|
| Leads added this week | 1 | `docs/ops/pipeline_tracker.csv` |
| Positive replies | 2 | `docs/commercial/operations/evidence_events_tracker.csv` |
| Samples / proposals | 3 | evidence tracker |
| Paid revenue | 5 | proof ledger |
| Approved proof events | 2 | proof ledger |
| Friction events | -1 | friction log |

A sector's weekly score is the weighted sum. The four-week rolling average
drives the call.

## Decision rule

| Rolling score vs target | Action |
|---|---|
| ≥ 1.2× | Scale — re-allocate from Capital Allocation reserve |
| 0.8–1.2× | Fix — diagnose the weakest dimension and adjust |
| < 0.8× for 2 weeks | Kill — pause investment, document why |

Decisions go through [`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md).

## Generator

```
make hyper-sectors
```

Runs [`scripts/beachhead_sector_scorecard.py`](../../scripts/beachhead_sector_scorecard.py)
and writes `data/founder_briefs/sector_scorecard_<week>.md`.

## Cross-references

- [STRATEGIC_ACCOUNT_LIST](STRATEGIC_ACCOUNT_LIST.md)
- [`docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`](../founder/STRATEGIC_ASSUMPTIONS_REGISTER.md)
- [`docs/finance/CAPITAL_ALLOCATION_SYSTEM.md`](../finance/CAPITAL_ALLOCATION_SYSTEM.md)
- [`docs/strategy/MARKET_MAP_SAUDI.md`](MARKET_MAP_SAUDI.md)
- [`docs/strategy/VERTICAL_PLAYBOOKS.md`](VERTICAL_PLAYBOOKS.md)

## Non-negotiables

Sector calls are based on real source rows. Kill calls are documented.
See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
