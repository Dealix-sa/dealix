# Capital Allocation System

How the CEO decides where the company's money and time go each quarter.

This system records intent only. Customer money movement is handled by
[`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md) + Moyasar
verifier; this layer never carries funds and never commits to refunds.

## Buckets

| Bucket | Definition | Default % of available capital |
|---|---|---|
| **Demand** | Outbound, content, sector campaigns, partner enablement | 30% |
| **Supply** | Sample factory, proposal factory, delivery operators | 25% |
| **Trust** | Brand, proof, customer trust center, security review packets | 15% |
| **Product** | Differentiated tooling and automations | 15% |
| **Talent** | Hiring, contractors, coaching | 10% |
| **Reserve** | Runway protection | 5% |

The percentages above are starting defaults; the CEO re-grades them every
quarter using [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md) as the rubric.

## Gates

Every quarter, for each bucket:

1. **Keep** — bucket showed clear signal; same allocation
2. **Increase** — bucket compounded above expectation; +5% from Reserve or from a Cut bucket
3. **Decrease** — bucket underperformed; –5% to Reserve or to an Increase bucket
4. **Kill** — bucket showed no signal across two consecutive quarters; allocation goes to 0%

Every gate decision is appended to
[`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md)
with `type: bet` or `type: cut`, and the assumption(s) backing it are linked
from [`docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`](../founder/STRATEGIC_ASSUMPTIONS_REGISTER.md).

## CSV layout

Stored at `$DEALIX_OPS_PRIVATE/ceo/capital_allocations.csv`.

| Column | Notes |
|---|---|
| `quarter` | `2026Q2`, `2026Q3`, ... |
| `bucket` | One of: demand, supply, trust, product, talent, reserve |
| `allocated_sar` | Planned spend |
| `actual_sar` | Updated at quarter close |
| `roi_estimate` | Score from [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md) |
| `owner` | `ceo` or named operator |
| `notes` | Free text — assumptions, gate decision |

## Generator

```
make hyper-capital
```

Runs [`scripts/capital_allocation_snapshot.py`](../../scripts/capital_allocation_snapshot.py)
which reads the CSV and produces `data/founder_briefs/capital_allocation_<quarter>.md`.
When PRIVATE_OPS is disabled the script emits the standard bilingual note
and exits 0.

## API

- `GET /api/v1/founder/capital-allocation/quarterly` — current quarter view
- `GET /api/v1/founder/capital-allocation/roi-matrix` — open initiatives scored

## Cross-references

- [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md) — the scoring rubric for any bucket decision
- [HIRE_VS_AUTOMATE_VS_PARTNER](HIRE_VS_AUTOMATE_VS_PARTNER.md) — Talent bucket decisions
- [`docs/enterprise/CAPITAL_LEDGER_V2.md`](../enterprise/CAPITAL_LEDGER_V2.md) — capital asset ledger
- [`docs/operating_finance/`](../operating_finance/) — accounting reconciliation

## Non-negotiables

This system records intent only; actual money movement flows through
[`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md) and the Moyasar
verifier. The CEO layer never carries customer funds. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
