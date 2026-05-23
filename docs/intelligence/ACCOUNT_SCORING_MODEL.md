# Account Scoring Model

The account scoring model collapses sector rank, ICP fit, persona
authority, trigger recency, and operating signals into a single number per
account. That number drives the order in which the team and the
Distribution War Machine work. This document defines the features, weights,
calibration cadence, and CSV output.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. What the score represents

The score is the answer to one question:

> "If we have one hour of operator attention this week, which named account
> should it go to?"

It is not a prediction of revenue. It is not a probability of close. It is
a ranking signal — defensible, reproducible, and re-calibrated against
outcomes.

## 2. Features

Each account receives a score on the following features:

1. `sector_rank_norm` — normalised sector weighted_total from
   `growth/sector_targets.csv` (0..1).
2. `icp_tier_score` — T1 = 1.0, T2 = 0.6, T3 = 0.3, none = 0.
3. `persona_authority_score` — primary persona authority shape:
   decides = 1.0, signs = 0.9, influences = 0.6, blocks = 0.3,
   unknown = 0.2.
4. `trigger_recency_score` — derived from `growth/trigger_events.csv` per
   the bonus structure in `TRIGGER_EVENT_SYSTEM.md`.
5. `warm_path_score` — strongest known warm path: partner = 1.0,
   founder content = 0.7, mutual connection = 0.6, none = 0.
6. `engagement_score` — engagement on Dealix-owned channels in the last
   30 days, normalised 0..1.
7. `proof_fit_score` — whether Dealix can produce a credible proof
   artefact for this account within 30 days; 1.0 if yes, 0.4 if maybe,
   0.0 if no.
8. `delivery_capacity_score` — whether the next 6 weeks of delivery
   capacity can absorb this account if it converts; 1.0 yes, 0.5 partial,
   0.0 no.
9. `trust_risk_penalty` — penalty 0..1 for sensitive data, regulator
   exposure, or unresolved escalations.
10. `disqualifier_flag` — boolean. If true, the score is forced to 0.

## 3. Weight table

| Feature | Weight |
|---|---|
| sector_rank_norm | 0.15 |
| icp_tier_score | 0.18 |
| persona_authority_score | 0.10 |
| trigger_recency_score | 0.15 |
| warm_path_score | 0.12 |
| engagement_score | 0.08 |
| proof_fit_score | 0.10 |
| delivery_capacity_score | 0.07 |
| trust_risk_penalty (subtracted) | 0.05 |
| | Total positive: 0.95 |

Final score formula:

```
raw = sum(weight_i * feature_i) - 0.05 * trust_risk_penalty
score = 0 if disqualifier_flag else clamp(raw, 0, 1) * 100
```

The score is rounded to one decimal place and stored 0..100.

## 4. Score bands

- 80–100: priority. Goes into the next operator review and the
  Distribution War Machine queue.
- 60–79: rotation. Enters the standard rotation with bounded volume.
- 40–59: warm queue. Eligible for content-to-demand only.
- 0–39: parked. No outreach drafts generated; re-scored next cycle.

Band membership is recomputed every time underlying features change.

## 5. Calibration cadence

| Cadence | Activity |
|---|---|
| Daily | Recompute scores; refresh trigger recency |
| Weekly | Manual review of top 20 scores by Founder + Growth Strategist |
| Monthly | Compare top-quartile scores against pipeline outcomes |
| Quarterly | Re-tune weights; bounded at +/-0.02 per feature per quarter |

Quarterly re-tuning uses the previous 90 days of pipeline outcomes (sample
sent, proposal sent, deal closed, deal lost, deal stalled). Each weight is
adjusted to better reflect signal-to-outcome correlation. The change is
logged in `growth/scoring_calibration.md` with the before/after weights
and the rationale.

## 6. CSV output schema

`growth/account_scores.csv`:

- `account_id`
- `account_name`
- `sector_id`
- `icp_id`
- `primary_persona_id`
- `sector_rank_norm`
- `icp_tier_score`
- `persona_authority_score`
- `trigger_recency_score`
- `warm_path_score`
- `engagement_score`
- `proof_fit_score`
- `delivery_capacity_score`
- `trust_risk_penalty`
- `disqualifier_flag`
- `score` — 0..100
- `band` — priority | rotation | warm | parked
- `last_scored_at`
- `notes`

## 7. Inputs

- `growth/sector_targets.csv`
- `growth/icp_segments.csv`
- `growth/personas.csv`
- `growth/icp_persona_matrix.csv`
- `growth/trigger_events.csv`
- `growth/account_universe.csv`
- `distribution/channel_scorecard.csv`
- `sales/proposal_queue.csv` (for outcomes)
- `trust/trust_flags.csv` (for risk penalties)
- `outreach/suppression.csv` (forces disqualifier flag)

## 8. Outputs

- Primary: `growth/account_scores.csv`.
- Audit: append-only entries in the trust ledger for every score change
  that crosses a band threshold.
- Brief: `founder/operating_scorecard.md` includes the top accounts by
  band with a one-line reason each.

## 9. Saudi-specific overlays

- The warm_path_score weight is intentionally high. In Saudi B2B, warm
  introduction outperforms cold-but-fit accounts at a rate that justifies
  this weighting.
- The disqualifier_flag is hard. Suppression, opt-out, or trust flag means
  the account does not appear in the priority band, regardless of other
  features.
- Distress triggers do not raise the score; they may set the trust risk
  penalty if circumstances warrant.

## 10. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console for weight changes.
- Auditor: Trust Guardian — every disqualifier and trust risk penalty is
  ledgered.
- Reviewer: Performance Analyst — runs the monthly score-vs-outcome view.

## 11. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Score-outcome mismatch | Quarterly weight retune; targeted feature audit |
| Disqualifier ignored | Block in Distribution War Machine; ledger entry |
| Stale features | Daily recompute job alerts on > 7-day staleness |
| Source vanished | Feature value set to 0; ledger entry |
| Top accounts never advance | Force manual operator review; reset rotation |

## 12. Non-negotiables

- The score is not a sales forecast. It is a queue.
- "Guaranteed" or probability-of-close language does not appear in any
  account brief that references this score.
- The score does not trigger external action. It seeds drafts for an
  approval queue.
- A3 is banned. Only A1 (draft) and A2 (assist with approval) apply.

A score that does not change in response to outcomes is not intelligence —
it is decoration. This model gets retuned, by design.
