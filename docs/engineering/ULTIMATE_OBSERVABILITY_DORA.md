# Ultimate Observability and DORA

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Focused on Results.

This document defines the observability surfaces Dealix maintains and
the DORA-style engineering metrics we hold ourselves to. The goal is
operational: shipping safe changes fast and detecting regressions
before they reach the founder.

## Observability surfaces

Dealix observability is split into four surfaces, each with a
defined owner.

| Surface                       | Source                                                       | Owner                  | Reader                                           |
| ----------------------------- | ------------------------------------------------------------ | ---------------------- | ------------------------------------------------ |
| Application logs              | Structured JSON logs from the FastAPI application.            | Engineering            | Aggregated log pipeline; queried via tooling.    |
| Application metrics           | Counters, histograms, gauges exported from the application.   | Engineering            | Time-series store; reviewed weekly.              |
| Worker state                  | `runtime/worker_state.csv`                                   | Worker Orchestrator    | Founder Console `/workers/health`.               |
| Trust observability            | `trust/approval_decisions.csv`, `trust/trust_flags.csv`, `trust/incidents.csv`   | Trust Guardian          | Founder Console; founder brief.                  |

The four surfaces together give the founder a complete picture: code
behavior, infrastructure behavior, agent behavior, and trust posture.

## Application logs

Logs follow these conventions:

| Convention                  | Example                                            |
| --------------------------- | -------------------------------------------------- |
| Structured JSON              | `{"ts": "...", "level": "INFO", "msg": "...", ...}` |
| Stable field names           | `request_id`, `endpoint`, `actor`, `audit_id`.     |
| No secrets                   | Tokens never written.                              |
| One log per request          | Plus per-mutation logs that reference the audit id. |
| UTC timestamps               | All times in ISO 8601 UTC.                         |

Logs are read in incidents, in deploy reviews, and in DQ failures.
They are not the source of truth for any business decision.

## Application metrics

The metrics surface is intentionally small. The canonical metrics:

| Metric                                              | Type      | Notes                                                  |
| --------------------------------------------------- | --------- | ------------------------------------------------------ |
| `http_request_duration_seconds`                     | histogram | Per endpoint.                                          |
| `http_request_count_total`                          | counter   | Per endpoint, status code.                             |
| `internal_api_token_missing_total`                  | counter   | Production 401s.                                       |
| `policy_denial_total`                               | counter   | Per rule id.                                           |
| `audit_event_total`                                 | counter   | Per action.                                            |
| `worker_run_duration_seconds`                       | histogram | Per worker.                                            |
| `worker_failure_total`                              | counter   | Per worker.                                            |
| `eval_gate_blocking_failures_total`                 | counter   | Per suite.                                             |
| `runtime_read_source_total`                         | counter   | `csv`, `missing`, `no-runtime`.                        |

The metric surface is part of the production posture check
(`docs/security/PRODUCTION_SECURITY_GATE.md`).

## DORA metrics

We track the four DORA metrics with operational thresholds. The
target bands reflect a small-team, trust-heavy operating posture.

| Metric                       | Target band      | Owner        | Notes                                                                 |
| ---------------------------- | ---------------- | ------------ | --------------------------------------------------------------------- |
| Deployment frequency         | Daily or better  | Engineering  | One deploy per day to the application; private ops bootstrap as needed. |
| Lead time for changes        | < 24 hours       | Engineering  | From commit to production.                                            |
| Change failure rate          | < 10%            | Engineering  | Failure = revert, hotfix, or rollback.                                |
| Mean time to restore         | < 2 hours        | Engineering  | From incident open to service restored.                                |

We deliberately do not chase "elite" thresholds beyond these bands.
The trust posture (founder approvals, eval gate, policy adapter) is
the constraint, not deploy frequency.

## DORA measurement

| Metric                       | Measurement source                                                   |
| ---------------------------- | -------------------------------------------------------------------- |
| Deployment frequency         | CI deploy log; counted weekly.                                       |
| Lead time for changes        | Commit ts vs. deploy ts in CI artifact.                              |
| Change failure rate          | Count of reverts + hotfixes / total deploys, per month.               |
| Mean time to restore         | Incident open ts vs. close ts in `trust/incidents.csv`.              |

## Trust observability metrics

These metrics are operating concerns, not engineering concerns, but
they are surfaced in the same review cadence:

| Metric                                       | Source                                            |
| -------------------------------------------- | ------------------------------------------------- |
| Open approval count                          | `approvals/approval_queue.csv`                    |
| Eval gate blocking failures (rolling 7-day)  | `evals/eval_status.csv`                           |
| Trust flag count by severity                 | `trust/trust_flags.csv`                           |
| Incident count (open + closed last 30 days)  | `trust/incidents.csv`                             |
| Policy denial count by rule (rolling 7-day)   | `trust/approval_decisions.csv` action filter      |

## Founder Console surfaces

| Endpoint                                  | What it shows                                                |
| ----------------------------------------- | ------------------------------------------------------------ |
| `GET /workers/health`                     | Worker statuses, last run, failure count.                    |
| `GET /trust/flags`                        | Active trust flags.                                          |
| `GET /audit/events`                       | Recent audit events.                                          |
| `GET /security/status`                    | Secrets scan, dependency scan, PDPL review.                  |
| `GET /evals/status`                       | Eval gate state, last pass.                                  |
| `GET /control/scorecard`                  | Four-pillar scorecard.                                       |

## Review cadence

| Activity                       | Cadence  | Audience           |
| ------------------------------ | -------- | ------------------ |
| Founder brief                  | Daily    | Founder.           |
| Trust flag review              | Daily    | Trust Guardian.    |
| DORA scorecard refresh         | Weekly   | Engineering.       |
| Incident post-mortem           | Per incident | Engineering + founder. |
| Metrics surface audit          | Monthly  | Engineering.       |

## SLOs

Application SLOs are documented in `docs/SLO.md`. The internal API has
no public SLO because it is internal-only. The application SLO is the
customer-facing posture.

## Alerting

Alerts are owned by Engineering. Alert rules are configured to
trigger on:

- Sustained `http_request_count_total{code=5xx}` rises.
- Policy denial rate spike on `no_a3_auto`.
- Worker `failure_count` exceeding thresholds.
- Eval gate blocking failure persisting >30 minutes.
- Disk usage on the private ops volume.

Paging policy and on-call rotation live in `docs/ops/ON_CALL.md` and
`docs/ops/ON_CALL_ROTATION.md`.

## Incidents

Incident handling is documented in
`docs/security/INCIDENT_RESPONSE_OS.md`. The observability
contribution is:

1. Logs and metrics establish the timeline.
2. The audit ledger documents who decided what.
3. The trust flags document what the system noticed.
4. The incident row documents the human-led recovery.

## Discipline

1. Logs are structured, secret-free, UTC.
2. Metrics are few and stable.
3. DORA metrics are tracked weekly, not chased monthly.
4. Trust observability is on par with engineering observability.
5. The Founder Console is the single observability surface for the
   founder. Engineering has additional tooling; the founder reads
   one console.
