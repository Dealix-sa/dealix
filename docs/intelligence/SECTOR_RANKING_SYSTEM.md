# Sector Ranking System

This document defines how Dealix ranks Saudi B2B sectors before it spends
operator attention on them. Every sector is scored against the same rubric.
The ranking is a forcing function — it stops the team from chasing the
loudest sector and forces a defensible choice.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. The rubric (11 dimensions)

Each sector is scored 0 to 5 on each dimension. 0 = unfit. 5 = exceptional.

1. Saudi relevance — concentration of decision-makers in KSA, presence of
   local procurement, sensitivity to local trust signals.
2. B2B fit — the sector buys business-to-business at the relevant ticket
   size and decision velocity.
3. High-ticket — average contract value supports a six-figure SAR retainer
   path within 12 months.
4. Buyer clarity — the buyer can be named, found, and reached without
   guesswork; titles map to authority.
5. Pain urgency — there is a dated, business-cost pain that ranks above
   normal noise (regulation, growth, leakage).
6. Outreach fit — the sector responds to the channels Dealix actually
   operates: warm intros, founder content, partner referrals, structured
   email and LinkedIn drafts that pass our trust gate.
7. Proof fit — Dealix can produce a credible proof artefact for this
   sector within 30 days (sample, diagnostic, pilot output).
8. Partner potential — there exist named, reachable partners (agencies,
   consultancies, system integrators) that can route deals.
9. Delivery complexity — Dealix can deliver the work without overextending
   the operating model. Lower complexity = higher score.
10. Trust risk — sensitive data, regulated workloads, or political
    exposure. Lower risk = higher score.
11. Priority — operator judgement on whether this sector should be in the
    current quarter. This is the only weighted-by-judgement dimension.

## 2. Weight table

| # | Dimension | Weight |
|---|---|---|
| 1 | Saudi relevance | 0.14 |
| 2 | B2B fit | 0.10 |
| 3 | High-ticket | 0.12 |
| 4 | Buyer clarity | 0.10 |
| 5 | Pain urgency | 0.12 |
| 6 | Outreach fit | 0.08 |
| 7 | Proof fit | 0.08 |
| 8 | Partner potential | 0.08 |
| 9 | Delivery complexity (inverted) | 0.06 |
| 10 | Trust risk (inverted) | 0.06 |
| 11 | Priority | 0.06 |
| | Total | 1.00 |

Weights sum to 1.00. A perfect sector scores 5.00. The threshold for
sectors that enter the active operating list is 3.40. Sectors between 3.00
and 3.40 are kept as "watchlist" and re-scored monthly.

## 3. Scoring procedure

1. Growth Strategist pulls the sector list from
   `docs/intelligence/SAUDI_B2B_MARKET_MAP.md`.
2. Each sector is scored on each dimension. The score is supported by at
   least one named source. No source, no score.
3. The weighted sum is computed and rounded to two decimals.
4. The result is written to `growth/sector_targets.csv` with the schema
   below.
5. A delta report is appended to `growth/sector_targets_delta.md` showing
   what moved and why.
6. The Founder Console surfaces sectors above the active threshold; any
   change in tier requires founder acknowledgement.

## 4. CSV output schema

`growth/sector_targets.csv` columns:

- `sector_id` — slug, lower_snake_case.
- `sector_name` — human readable.
- `score_saudi_relevance`
- `score_b2b_fit`
- `score_high_ticket`
- `score_buyer_clarity`
- `score_pain_urgency`
- `score_outreach_fit`
- `score_proof_fit`
- `score_partner_potential`
- `score_delivery_complexity` (raw; inverted before weighting)
- `score_trust_risk` (raw; inverted before weighting)
- `score_priority`
- `weighted_total`
- `tier` — active | watchlist | parked
- `notes`
- `last_scored_at` — ISO date
- `scored_by` — agent or operator id
- `source_refs` — pipe-delimited source identifiers

## 5. Tier definitions

- Active: weighted_total >= 3.40. Goes into the Distribution War Machine
  rotation and the proof factory backlog.
- Watchlist: 3.00 to 3.39. Re-scored monthly; partner conversations only.
- Parked: under 3.00. No operator attention. Re-scored quarterly.

## 6. Calibration cadence

| Cadence | Activity |
|---|---|
| Weekly | Re-score any sector where a trigger event fires |
| Monthly | Re-score watchlist sectors |
| Quarterly | Re-tune dimension weights against pipeline outcomes |

Quarterly weight re-tuning compares ranked sectors against actual revenue
and pipeline performance. If a dimension shows little signal in the data,
its weight is reduced. If a low-weight dimension explains a lot of pipeline
variance, its weight is increased. The change is bounded at +/-0.02 per
dimension per quarter to avoid swing.

## 7. Sources and ethics

Allowed sources:
- Public sector reports with named author and date.
- Founder content engagement metrics (Dealix-owned channels).
- Partner-introduced signals attributed in writing.
- Internal pipeline outcomes from the Revenue Factory.

Banned sources:
- Scraped competitor data.
- Personal contact lists obtained without consent.
- Recordings without explicit recorded consent.
- Anything that cannot be re-traced to a named, dated origin.

If a source is later found to be unattributable, the score it supports is
re-derived from a clean source or removed.

## 8. Owners and approval

- Owner: Growth Strategist (`growth_strategist`, approval class max A2).
- Approver: Founder Console, on any tier change.
- Auditor: Trust Guardian; all scoring decisions are appended to the
  trust ledger.

## 9. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Score with no source | Trust Guardian quarantines the row; rescored |
| Sector ranked high but converts low | Quarterly calibration; weight retune |
| Dimension drift (e.g. proof fit always 5) | Reset dimension; require 2 sources |
| Operator override loop | Priority dimension capped; cannot exceed 5 |
| Stale ranking (>30 days) | Performance Analyst raises stale flag |

## 10. Non-negotiables

- No external send is triggered by this layer.
- No "guaranteed" sector outcome appears in any ranking document.
- Every score is traceable.
- A3 approvals are not used. Only A1 (observe/draft) and A2 (assist with
  approval) apply.

The ranking is not a story we tell investors. It is the queue order for
the next quarter of operator attention. Treat it as such.
