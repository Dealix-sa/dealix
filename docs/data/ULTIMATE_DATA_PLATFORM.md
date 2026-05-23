# Ultimate Data Platform

Three storage tiers:

1. **Private ops CSVs** (`${DEALIX_PRIVATE_OPS}/**`). The source of
   truth today. Never committed.
2. **Postgres** (planned). Same schema as the CSV headers in
   `api.internal.runtime_reader.RUNTIME_FILES`.
3. **Event store** (planned). Append-only `decision_events` with a hash
   chain so the audit log cannot be silently edited.

## Naming convention

- `intelligence/*.csv` — lead/company facts.
- `outreach/*.csv` — drafts, queue, conversation log, suppression.
- `approvals/*.csv` — pending decisions for the founder.
- `trust/*.csv` — decisions + open trust flags.
- `sales/*.csv` — proposals.
- `finance/*.csv` — payment capture + cash collected.
- `runtime/*.csv` — worker state.
- `distribution/*.csv` — channel + sector scorecards.
- `evals/*.csv` — gate suite results.
- `product/*.csv` — productization candidates.
- `security/*.csv` — security control posture.
- `founder/*` — generated reports (scorecard, briefings).

## Governance

Every write that crosses a trust boundary (`outreach`, `approvals`,
`trust`, `sales`, `finance`) must be matched by an `approval_decisions`
row referencing the approval id.
