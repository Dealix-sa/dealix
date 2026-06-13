# ICP Scoring System (100 points)

> **Status:** Default rubric. Calibrate after the first 10 deals.
> **Executable:** `scripts/icp_score_dry_run.py` + `schemas/launch/icp_score.schema.json` + `templates/launch/icp_score.example.json`.

## The 10 criteria

| Criterion | Max | What it measures |
| --- | --- | --- |
| `urgency` | 20 | How soon do they need a fix? (Lost a deal, end of quarter, scaling pain.) |
| `lost_revenue_visibility` | 15 | Can they see the leak? (Aware of the gap vs blind.) |
| `process_chaos` | 15 | Is the chaos measurable? (WhatsApp overload, missed follow-ups, no CRM hygiene.) |
| `decision_maker_access` | 10 | Can we reach the decision maker in 2 steps? (Owner / GM / head of sales reachable.) |
| `ability_to_start_small` | 10 | Will they take a 3–5 day audit? (Openness to a low-commitment first step.) |
| `proof_speed` | 10 | Can we show a result in ≤14 days? |
| `budget_likelihood` | 10 | Have they paid for a SaaS or a service in the last 90 days? |
| `repeatability` | 5 | Same shape as 100 other accounts? |
| `referral_potential` | 5 | Will they refer 2+ peers? |
| `compliance_delivery_risk` | -20 (negative) | Industry regulation, data residency, PII sensitivity. |

**Total: 100 (max), 0 (min).** A negative score is possible.

## The thresholds

| Score | Action |
| --- | --- |
| 80+ | pursue today |
| 65–79 | warm sequence (nurture for 14 days) |
| 50–64 | low-touch nurture (LinkedIn only, monthly check-in) |
| below 50 | ignore |
| any critical compliance risk flagged | manual review before send |

## How to score an account

For each criterion, give the actual score. Sum. Apply the action.

Example:

```json
{
  "account_id": "agency_x_riyadh",
  "scores": {
    "urgency": 18,
    "lost_revenue_visibility": 12,
    "process_chaos": 14,
    "decision_maker_access": 9,
    "ability_to_start_small": 9,
    "proof_speed": 8,
    "budget_likelihood": 8,
    "repeatability": 4,
    "referral_potential": 4,
    "compliance_delivery_risk": 0
  },
  "total": 86,
  "action": "pursue_today"
}
```

The script `scripts/icp_score_dry_run.py` reads this and prints the action.

## When to recalibrate

Every 30 days, look at the conversion data:

- Did the 80+ cohort convert at > 30%? If yes, the rubric is right.
- Did the 65–79 cohort convert at < 10%? If yes, raise the bar to 70+.
- Did any < 50 cohort convert? If yes, the rubric missed something. Investigate.

Re-score the last 30 days of accounts and see if the new rubric would have re-prioritized them.

## The signals that override the rubric

| Signal | Override |
| --- | --- |
| Account is in the **founder's existing network** | bump +10 on `decision_maker_access`, send warm intro |
| Account has a **named case study competitor** (already lost a deal to a similar offer) | bump +5 on `urgency` |
| Account is in a **regulated sector** (health, legal, finance) | apply compliance risk BEFORE scoring; if risk > 8, manual review |
| Account has **never paid for a SaaS or service** | drop `budget_likelihood` to 2 |
| Account's **decision maker just changed** | drop `urgency` to 5; new buyer is learning |

These overrides are logged in the same JSON under `overrides[]`.

## How ICP fits the vertical selection

The vertical matrix (`SAUDI_VERTICAL_SELECTION_MATRIX_AR.md`) is the **macro** decision (which sector to pursue). The ICP score is the **micro** decision (which specific account to pursue in that sector).

Use both:

1. Pick the vertical (default: agencies).
2. Score 30 accounts in that vertical using the ICP rubric.
3. Pursue the top 5–10 in week 1.
4. Re-score at the end of week 2 based on reply rate.

## The data sources (allowed)

You can score an account from these sources:

- LinkedIn profile (manual view).
- Company website (manual read).
- Google Maps listing (manual view).
- Public review sites (manual read).
- Referral intro (manual).
- Inbound inquiry (they came to you).
- Event follow-up (you met them).
- Newsletter / content engagement (they subscribed).

You **cannot** score from:

- Scraped lists.
- Purchased databases.
- Cold WhatsApp numbers from a third party.
- Any data the account has not consented to share.

If the data source is "I found their email via a tool that scrapes LinkedIn", that is not allowed. Use a manual approach or don't pursue the account.

## When to drop an account

- ICP score drops below 50 after a re-score.
- 3+ touchpoints with no reply.
- 1 explicit "not interested" reply.
- The founder's network rating drops (e.g. a mutual contact says "avoid this one").

Drop = move to a `paused` list, do not delete. Re-score in 90 days.
