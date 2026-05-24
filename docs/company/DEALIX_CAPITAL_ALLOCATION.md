# Dealix Capital Allocation

Capital is the founder's scarcest input. This doc defines how Dealix
allocates time + money + compute across pools, and how we report on it.

## Budget pools

| Pool | Target % of revenue | Notes |
|---|---|---|
| people | 35 | Founder time + future hires. Time priced at SAR 500/h until first hire. |
| infra | 10 | Railway + Postgres + Redis + S3 + LLM APIs. |
| sales | 20 | Tools, content production, partner referrals (no ads at <SAR 10K MRR). |
| R&D | 25 | New offers, Proof Pack improvements, eval coverage. |
| runway buffer | 10 | Reserve for 3-month operating runway minimum. |

## Reporting

`make capital-allocation` runs `scripts/generate_capital_allocation_report.py`
to emit `data/capital_allocation/<YYYY-MM>.md`. The report shows actual
spend vs target, with the founder making decisions on overages.

## Decision rules

- If `sales` pool > 30% AND no new revenue uplift -> halt new sales tooling.
- If `R&D` pool > 35% -> halt new feature work; ship + bill what exists.
- If `runway buffer` < 10% -> declare hiring + investment freeze.

## Compute budget

| Service | Monthly cap (SAR) |
|---|---|
| Anthropic API | 1,500 |
| OpenAI API | 500 |
| Railway compute | 800 |
| Postgres + Redis (managed) | 400 |

Overruns trigger a `pricing_change` approval through approval_center.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
