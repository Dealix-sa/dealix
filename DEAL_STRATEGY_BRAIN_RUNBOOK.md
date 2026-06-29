# Deal Strategy Brain — Runbook

## Purpose

Takes a client message and account context, combines conversation intelligence with deal scoring, and returns a complete strategy: best offer, pricing range, negotiation position, must-ask questions, proof to show, and explicit do-not-do list.

## What It Returns

| Field | Description |
|-------|-------------|
| deal_score | 0–100 score based on stage, sentiment, urgency, objection, missing info |
| close_probability_band | low / medium / high / very_high |
| best_offer | Recommended offer from the 6-rung ladder |
| pricing_range | SAR range for the suggested offer |
| recommended_discount_policy | Max discount, requires approval, never auto-commit |
| negotiation_position | Stance, message, concession order, never-do list |
| must_ask_questions | Up to 4 prioritized discovery questions |
| next_best_action | One concrete action for the founder to take |
| do_not_do | Explicit forbidden actions for this deal |
| approval_gates | Gates that must be triggered before any sensitive action |
| proof_to_show | Evidence items most likely to advance this deal |

## Probability Bands

- `low` (0–24): nurture, no proposal yet
- `medium` (25–49): discovery phase, need more info
- `high` (50–74): ready for qualified proposal
- `very_high` (75–100): close-ready, optimize for conversion

## Offer Ladder

1. free_diagnostic — 0 SAR, 30 min
2. micro_sprint_499_sar — 499 SAR, 1 week
3. data_pack_1500_sar — 1,500 SAR, one-time
4. managed_ops_2999_4999_sar_monthly — 2,999–4,999 SAR/mo
5. transformation_diagnostic_sprint_7500_25000_sar — 7,500–25,000 SAR
6. custom_enterprise_system — 25,000–100,000+ SAR

## Forbidden Commitments

- guaranteed_revenue
- final_price_without_scope
- fake_case_studies
- legal_commitments
- uncontrolled_outreach

## Usage

```bash
python deal_strategy_brain.py
```

```python
import deal_strategy_brain as dsb

strategy = dsb.build_strategy(
    account='Alpha Trading',
    sector='Retail',
    message='كم السعر؟',
)
print(strategy['next_best_action'])
print(strategy['close_probability_band'])
```

## Safety Rules

- Discount always requires approval
- No auto-commit on any price
- No guaranteed revenue or ROI claims
- Probability bands only — no precise percentages
