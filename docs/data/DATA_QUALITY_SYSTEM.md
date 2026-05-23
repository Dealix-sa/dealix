# Data Quality System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust · Focused on Results.

The Data Quality (DQ) System is the discipline that keeps the
operating data trustworthy. Without DQ, the scorecards lie, the
diagnostics chase ghosts, and the founder's decisions degrade. DQ is
the property that every number a worker emits should be the number an
auditor would compute from the same sources.

## Scope

DQ covers three layers:

| Layer              | DQ concern                                                                |
| ------------------ | ------------------------------------------------------------------------- |
| Postgres           | Schema, foreign keys, row counts, constraints, replication lag.            |
| Private ops CSVs   | Header drift, column types, row count anomalies, monotonicity.             |
| Derived snapshots  | Freshness, internal consistency, reconciliation with source counts.        |

DQ does not cover content correctness in free-text fields (e.g.,
draft body). That is the eval gate's job.

## Checks

DQ runs a closed list of checks. New checks must be added to this
list with an owner.

### Schema checks

| Check                       | Target                        | Failure means                                            |
| --------------------------- | ----------------------------- | -------------------------------------------------------- |
| `csv_header_matches_bootstrap` | every CSV in the runtime    | The schema drifted; a worker is writing the wrong shape. |
| `csv_no_empty_required_col`  | every CSV with required cols   | A worker wrote a row missing a required field.           |
| `postgres_schema_pinned`     | Postgres                       | A migration was applied outside Alembic.                 |
| `postgres_unique_keys_unique`| Postgres                       | A duplicate slipped past a constraint.                   |

### Freshness checks

| Check                              | Target                                  | Failure means                                |
| ---------------------------------- | --------------------------------------- | -------------------------------------------- |
| `scorecard_refreshed_within_24h`   | `founder/operating_scorecard.md`        | The nightly worker stopped running.          |
| `worker_state_updated_within_24h`  | `runtime/worker_state.csv`              | A worker is hung.                            |
| `eval_status_in_last_pass`         | `evals/eval_status.csv`                  | The eval runner is silent.                   |

### Reconciliation checks

| Check                                          | Target                                                                       | Failure means                          |
| ---------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------- |
| `cash_collected_csv_matches_finance_app`        | `finance/cash_collected.csv` vs Postgres `payments`                          | The cash CSV is stale.                 |
| `proposal_queue_matches_pipeline`               | `sales/proposal_queue.csv` row counts vs Postgres `deals`                    | A proposal slipped.                    |
| `audit_count_monotonic`                         | `trust/approval_decisions.csv` row count over time                            | The ledger was edited or truncated.    |
| `suppression_list_monotonic`                    | `outreach/suppression_list.csv` row count over time                          | Suppressions were silently removed.    |

### Trust-aware checks

| Check                                          | Target                                                                 | Failure means                                                              |
| ---------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `no_audit_action_outside_vocabulary`            | `trust/approval_decisions.csv` action column                            | An unrecognized action appeared; new code did not update the doc.          |
| `every_high_risk_audit_has_payload`              | `trust/approval_decisions.csv`                                          | A high-risk action was recorded without a payload.                         |
| `suppression_match_type_in_vocabulary`           | `outreach/suppression_list.csv` match_type column                       | An invalid match type was appended.                                        |

## DQ score

The DQ score is a 0..1 number summarizing the latest check pass:

```
dq_score = checks_passed / checks_total
```

The score is written to `data/dq_score.csv` with timestamp. The
Founder Console exposes it via `GET /api/v1/internal/data/summary`.

| dq_score band       | Operating posture                                                |
| ------------------- | ---------------------------------------------------------------- |
| 1.0                  | Green. No action.                                                |
| 0.95 ≤ dq < 1.0      | Yellow. Investigate within 24 hours.                             |
| 0.80 ≤ dq < 0.95     | Orange. Pause non-critical experiments; investigate immediately. |
| dq < 0.80            | Red. Trust flag opened; pause all draft writes pending fix.      |

## Pipeline failure log

`data/pipeline_failures.csv` records each failing check pass:

| Column         | Notes                                          |
| -------------- | ---------------------------------------------- |
| `ts`           | When the check failed.                          |
| `check_id`     | The named check.                                |
| `target`       | The CSV path or Postgres table affected.        |
| `details`      | One-line description of the failure.            |
| `owner`        | The agent or human responsible.                 |
| `resolved`     | Boolean.                                        |
| `resolved_ts`  | When resolved.                                  |

## Owners

| Concern                          | Owner agent                |
| -------------------------------- | -------------------------- |
| CSV schema drift                  | Worker that writes the CSV |
| Postgres schema                   | Engineering                |
| Audit ledger monotonicity         | Trust Guardian             |
| Suppression list monotonicity     | Trust Guardian             |
| Scorecard freshness               | CEO Copilot                 |
| Eval status freshness             | Eval Guardian               |

## Cadence

| Activity                  | Cadence  |
| ------------------------- | -------- |
| Run all checks            | Daily    |
| DQ score written           | Daily    |
| Pipeline failure review    | Daily (in the founder brief) |
| Schema drift audit         | Monthly  |
| Check vocabulary review    | Quarterly|

## Failure modes the DQ system intentionally surfaces

- A CSV with extra columns: tolerated; flagged as informational.
- A CSV with missing required columns: hard fail.
- A CSV that shrinks (audit/suppression): hard fail, incident opened.
- A Postgres table with row count anomalies: investigated; not an
  automatic fail (legitimate seasonality exists).
- A worker that has not updated `worker_state.csv` in 24 hours:
  treated as hung.

## Recovery playbook

1. The DQ worker writes a row to `data/pipeline_failures.csv`.
2. The Trust Guardian (for audit/suppression issues) or the worker
   owner (otherwise) is notified via the founder brief.
3. The owner runs the bootstrap script (`--force` only on
   deliberate schema migrations).
4. A new check pass is run; the score is recomputed.
5. If a fix requires editing existing data, the change is itself
   audited.

## Verifier

`scripts/verify_governance.py`, `scripts/verify_dealix_ready.py`,
and the broader verifier bundle cover schema posture in CI. A future
`scripts/verify_data_quality.py` will add the DQ check pass into the
verifier bundle.

## Discipline

1. Every CSV has a known schema.
2. Every snapshot has a known freshness expectation.
3. Every failure has an owner.
4. The audit ledger and suppression list never shrink without an
   audited destructive-operation approval.
5. The DQ score is read in every founder brief.
