# Client Health Score System

The Client Health Score is a 0-10 composite that summarises a client's current relationship state. It is a leading indicator for renewal and a triage signal for Customer Success.

**Source of truth:** `$PRIVATE_OPS/client_health_score.csv`
**Owner:** Customer Success Lead
**Trust gate:** A1 — score weights and thresholds are reviewed quarterly by founder.

## Inputs

| Input | Weight | Source |
|-------|--------|--------|
| Engagement utilisation | 0.20 | Delivery state (`docs/delivery/ULTIMATE_DELIVERY_OS.md`) |
| Sentiment from sessions | 0.15 | Working-session notes |
| Response latency | 0.10 | Reply routing log |
| Payment timeliness | 0.10 | Payment ledger (`docs/finance/PAYMENT_CAPTURE_OS.md`) |
| Open risk severity | 0.15 | Risk register |
| Outcome trend | 0.15 | Value Ledger (`docs/08_value_os/VALUE_LEDGER.md`) |
| Executive engagement | 0.10 | Founder digest attendance |
| Renewal posture | 0.05 | Quarterly review note |

Sum to 1.00. Each input is normalised to 0-10. The composite is the weighted sum, rounded to one decimal.

## Score bands

| Band | Score | Posture |
|------|-------|---------|
| Strong | 8.0-10.0 | Renewal candidate, referral candidate |
| Healthy | 6.5-7.9 | Maintain cadence |
| Watch | 5.0-6.4 | CS Lead intervention plan within 7 days |
| At-risk | 3.0-4.9 | Founder review within 3 days |
| Critical | 0.0-2.9 | Founder owns recovery within 24 hours |

## Read cadence

- Weekly: CS Lead reads the score for every active client.
- Monthly: Founder reads the distribution.
- Quarterly: Weights are reviewed against actual renewal outcomes.

## Calibration

The Health Score is calibrated by comparing predicted band against actual renewal in a rolling 12-month window. If a band predicts renewal materially worse than expected, the input weights are re-tuned. Calibration is logged in `$PRIVATE_OPS/health_score_calibration.csv`.

## Failure modes

- **False green:** a client scored Healthy churns. Detection: post-churn review. Recovery: identify the missing signal; consider new input.
- **Flapping score:** the score moves more than 2 points week-over-week. Detection: nightly job. Recovery: investigate; usually a noisy input source.
- **Missing input:** a required source is unavailable. Detection: nightly job. Recovery: score is held at last known value and flagged stale; not silently recomputed on missing data.

## Recovery path

If the Health Score system fails (data pipeline outage), CS Lead falls back to weekly qualitative read by client. No automated alarms fire on stale scores; the founder is notified that the system is in manual mode.

## Metrics

- Distribution of Health Scores across active clients.
- Stale-score count (scores not refreshed in 7+ days).
- Calibration accuracy: predicted vs actual renewal by band.

## Disclaimer

The Health Score is a triage signal, not a guarantee of renewal. Dealix does not guarantee retention. Estimated value is not Verified value.
