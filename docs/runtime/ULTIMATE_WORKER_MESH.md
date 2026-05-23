# Ultimate Worker Mesh

The worker mesh is the union of orchestrated jobs that hydrate the
private ops tree. They run on whatever scheduler exists (cron, GH
Actions, Railway), and all of them are read-only or audit-only.

## Mesh map

| Worker | Inputs | Outputs |
|---|---|---|
| ceo_summary | private ops + scorecard | founder/operating_scorecard.md |
| sales_funnel | outreach + conversations + proposals | sector_scorecard, channel_scorecard |
| trust_flags | trust_flags, approval_decisions | trust roll-up |
| finance_summary | cash_collected, payment_capture_queue | finance summary |

## Failure rule

A worker failure is not a silent event. The orchestrator must:

1. Increment `failures_24h` in `worker_state.csv`.
2. Open a trust flag with category `worker_failure` when failures > 0.
3. Surface the flag through `/api/v1/internal/trust/flags`.
