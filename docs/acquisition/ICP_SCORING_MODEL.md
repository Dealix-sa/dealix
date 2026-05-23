# ICP Scoring Model

> The weights used by `dealix/agents/` (scoring_agent) to score every lead 0–100.
> Updated quarterly based on actual win/loss patterns.

## Current Weights (Q1)

| Signal | Weight | Source |
|---|---|---|
| In Tier 1 sector | 25 | Enrichment |
| Revenue SAR 5M – 50M | 20 | Enrichment / public estimate |
| Founder/CEO contactable directly | 15 | LinkedIn + intro check |
| Has > 100 leads/month visible | 10 | Hiring pages / job ads / sector benchmark |
| Recent CRM purchase or SDR hire | 10 | LinkedIn + public news |
| Has English + Arabic ops | 5 | Website / LinkedIn presence |
| Active in sector we have proof in | 10 | Internal case-study match |
| Warm intro available | 5 | Network check |

**Total possible:** 100

## Score Thresholds

| Score | Action | SLA |
|---|---|---|
| 90–100 | Founder-drafted outreach this week | within 5 days |
| 75–89 | Agent-drafted + founder-approved outreach next week | within 10 days |
| 60–74 | Standard outreach, agent-drafted | within 14 days |
| 40–59 | Nurture only (content + newsletter) | n/a |
| 0–39 | Suppression — do not contact | enforced in code |

## Scoring Inputs (must be cited)

Every score comes with the inputs that produced it:
```yaml
score: 78
breakdown:
  sector_tier1: 25 (source: linkedin company sector field)
  revenue_band: 20 (source: zawya company profile, public)
  founder_contactable: 15 (source: linkedin profile + intro from {name})
  lead_volume_signal: 0 (no signal found)
  crm_or_sdr_signal: 10 (source: job posting URL)
  bilingual_ops: 5 (source: company website)
  proven_sector: 0 (no internal proof yet)
  warm_intro: 3 (partial — soft intro via {name})
```

A score with no breakdown is invalid. The agent refuses to emit unbacked scores.

## Hard Rules (override score)

- Auto-suppress if on suppression list
- Auto-suppress if disqualifier hit (see `QUALIFICATION_RULES.md`)
- Auto-flag if a previous incident logged for this contact / company
- Auto-down-weight by 30 if no real buyer name found (anonymous companies)

## Recalibration

Quarterly:
1. Pull closed-won and closed-lost from last 90 days
2. Regress: which weight signals actually predicted close-won?
3. Adjust weights ± 5 per signal based on data
4. Lock new weights in this file
5. Note recalibration in `DEALIX_EXECUTION_LEDGER.md`

If weights drift > 30% in any quarter → ICP itself may be wrong; revisit `ICP_STRATEGY.md`.

## What Scoring Won't Do

- Use private data (purchased, leaked, scraped)
- Score on proxy demographics (age, gender, etc.)
- Score in absence of evidence (no guessing)
- Be the sole determinant of contact decision (human approves)

## What Scoring Will Do

- Be transparent (every score → cited breakdown)
- Be reproducible (same inputs → same score)
- Be auditable (logged with timestamp + agent version)
- Be improved (recalibrated quarterly on actual outcomes)

## Review Cadence

- Weekly: distribution of new scores — is it skewed?
- Monthly: spot-check 10 random scores against reality
- Quarterly: full recalibration
