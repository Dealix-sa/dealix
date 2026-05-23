# Ultimate Observability + DORA

## What we measure

| Signal | Source |
|---|---|
| Worker last_run + failures_24h | `runtime/worker_state.csv` |
| Approval throughput | `trust/approval_decisions.csv` |
| Trust flag count | `trust/trust_flags.csv` |
| Eval gate blocking failures | `evals/eval_status.csv` |
| Operating scorecard scores | scorecard generator |

## DORA-style metrics (lightweight)

- **Lead time for change** — wall time from commit to merged PR.
- **Deployment frequency** — successful runs of CI.
- **Change failure rate** — PRs that revert or fail required checks.
- **Mean time to restore** — close-time of a `worker_failure` trust flag.

## Where they live

DORA numbers are not (yet) auto-computed in Dealix. The hooks exist
(`trust_flags.csv` for incidents, GitHub Actions for CI events) but the
roll-up is intentionally manual until we move audit to Postgres.
