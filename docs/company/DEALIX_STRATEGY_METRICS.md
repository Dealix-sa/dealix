# Dealix Strategy Metrics

This is the scorecard the founder owns. Updated weekly via
`make strategy-scorecard`.

## North-star metric

**Verified Operating Capability Delivered (VOCD)** — the SAR-weighted sum
of Proof Pack scores delivered in the period.

```
VOCD = Σ (proof_pack_score * engagement_value_sar) / 1000
```

A north-star above 35 in any 30-day window indicates the company is
producing real, audited operating capability for paying customers.

## Input metrics (leading)

| Metric | Cadence | Source |
|---|---|---|
| Diagnostics shipped | Weekly | Sales pipeline export |
| Sprints sold | Weekly | Moyasar invoices |
| Proof Packs delivered (score >= 70) | Weekly | `dealix/execution_assurance/` |
| Capital Assets registered | Weekly | `dealix/registers/` |
| Approval queue median age | Daily | approval_center metrics |
| Doctrine violations | Daily | governance audit log |

## Output metrics (lagging)

| Metric | Cadence | Source |
|---|---|---|
| MRR (SAR) | Monthly | Moyasar |
| Net retention | Quarterly | Customer roster |
| Customer count (paying) | Monthly | Moyasar |
| Average Proof Pack score | Monthly | Proof Pack store |

## Cadence

- Daily: input metrics auto-refresh from the daily brief.
- Weekly: scorecard generated + reviewed in weekly review.
- Monthly: output metrics added to executive review.
- Quarterly: strategy session — north-star + input metric review.

## Tracking

Output: `data/strategy_scorecard/<YYYY-MM>.md`.

The scorecard is read-only intelligence — no targets are auto-enforced.
The founder makes the calls.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
