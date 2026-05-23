# Account Scoring Model

A composite 0-100 score per Saudi B2B account, refreshed weekly.

## 1. Inputs

- ICP match (segment fit + persona fit).
- Trigger event freshness and confidence.
- Sector ranking.
- Buyer accessibility.
- Compliance posture alignment.
- Data completeness (penalty for fallback fields).

## 2. Composite formula

```
ICP_match        = w_icp * ICP_match_score
trigger          = w_trig * trigger_score * freshness_factor
sector           = w_sec * sector_score
accessibility    = w_acc * accessibility_score
compliance_align = w_comp * compliance_alignment
completeness     = -w_pen * fallback_share

score = clamp(0, 100,
   ICP_match + trigger + sector + accessibility +
   compliance_align + completeness)
```

Default weights (sum to 1.0): `0.30, 0.25, 0.15, 0.15, 0.15` and
penalty `0.20`.

## 3. Tiering

| Tier | Range | Treatment |
|---|---|---|
| A | 80–100 | Founder review weekly. Eligible for the proposal factory. |
| B | 60–79  | Founder reviews monthly. Outbound draft generated. |
| C | 40–59  | Nurture stream; no outbound; review quarterly. |
| D | < 40   | Off the list until a refresh moves them. |

## 4. Output

`growth/account_scores.csv` columns:

```
account_id,company_name,sector_id,segment_id,persona_id,
icp_match,trigger,sector,accessibility,compliance_alignment,
fallback_share,composite,tier,collected_at,source
```

## 5. Guardrails

- No score is published without `account_id` and `source`.
- A composite computed on > 30 % fallback fields is marked `provisional`.
- Tier-A drafts never auto-send. They wait in the approval queue.
- Tier movement of > ±25 points in one cycle pauses the row for review.
