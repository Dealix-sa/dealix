# DORA Metrics Policy

> Engineering health, measured. Aligned to DORA (DevOps Research and Assessment).

## The Four Metrics

1. **Deployment frequency** — how often we ship to production.
2. **Lead time for changes** — time from "code committed" to "running in prod".
3. **Change failure rate** — % of deployments that cause incidents.
4. **Mean time to restore** — time to recover after a failed deployment.

## Targets (current stage)

We are pre-PMF and small. Realistic targets:

| Metric | Target |
|--------|--------|
| Deployment frequency | ≥ weekly (any business-critical change) |
| Lead time for changes | ≤ 24 hours from merge → prod |
| Change failure rate | ≤ 15% |
| Mean time to restore | ≤ 1 hour |

Stretch targets (DORA "Elite" benchmarks) are recorded but not yet
required.

## How we measure

- `dealix-ops-private/engineering/dora.csv`: one row per deployment with
  timestamp, change reference, success/failure, restore time if failed.
- CI workflows tag deployments.
- Failures are logged in `INCIDENT_RESPONSE.md` if customer-facing.

## Review

- Weekly in the CEO review (one row per metric).
- Monthly in `ENGINEERING_HEALTH_REVIEW.md`.

## Anti-Patterns

- Optimising deployment frequency at the cost of change failure rate.
- Counting a deployment as successful when it was rolled back later that
  day.
- Reporting only the green metric.

## Use of DORA in Capital Allocation

- If change failure rate is above target for 2 consecutive months,
  engineering hours shift from new features to reliability.
- If deployment frequency is below target, the constraint is identified
  (review delay, test brittleness, infra) and addressed before new
  features.
