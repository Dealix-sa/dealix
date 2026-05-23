# Audit Event Model

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

Every approval, rejection, escalation, kill switch, scorecard refresh,
worker retry, draft, and risk acceptance in Dealix produces an audit
row. The audit ledger is the canonical record of every trust-relevant
decision. This document is the authoritative schema reference.

## File location

The audit ledger lives at
`trust/approval_decisions.csv` in the private ops runtime
(`/opt/dealix-ops-private` or `$PRIVATE_OPS`). It is **never** in the
repository. The file is bootstrapped by
`scripts/bootstrap_private_ops_runtime.py` and written by
`_audit_event()` in `api/routers/founder_console_internal.py`.

## Schema

The CSV header (defined in the bootstrap script and in the router) is:

| Column         | Type        | Required | Description                                                                 |
| -------------- | ----------- | -------- | --------------------------------------------------------------------------- |
| `id`           | UUID v4     | yes      | Unique audit row id. Returned in API responses as `audit_id`.                |
| `ts`           | ISO 8601 UTC| yes      | Timestamp at the moment the audit event was created.                        |
| `actor`        | string      | yes      | Who initiated the action. See actor vocabulary below.                       |
| `action`       | string      | yes      | What was done. See action vocabulary below.                                 |
| `target`       | string      | yes      | The object the action operated on (approval id, agent id, risk id, etc.).   |
| `risk`         | enum        | yes      | `low`, `medium`, `high`, or `critical`. Drives alerting and review cadence. |
| `payload_json` | JSON string | yes      | Free-form structured payload. Must be parseable JSON. UTF-8.                |

The columns are written by the API in exactly this order. Reading
clients must be tolerant to extra columns appearing in future
versions; new columns are appended on the right.

## Actor vocabulary

| Actor                  | When used                                                                 |
| ---------------------- | ------------------------------------------------------------------------- |
| `founder`              | The founder, via the Founder Console UI.                                  |
| `trust_guardian`       | The Trust Guardian agent (policy rule raises, suppression adds).          |
| `distribution_operator`| The Distribution Operator agent (suppression hits, queue refusals).        |
| `proof_safety_agent`   | The Proof Safety Agent (proof gate decisions).                            |
| `finance_copilot`      | The Finance Copilot (payment-term escalations).                           |
| `security_guardian`    | The Security Guardian (incident, export escalations).                     |
| `incident_response_agent`| The Incident Response Agent (incident opens/closes, kill switches).      |
| `eval_guardian`        | The Eval Guardian (eval gate decisions).                                  |
| `worker_orchestrator`  | The worker orchestrator (worker state changes, kill).                     |

Any new actor must be added to `registries/agent_registry.yaml` first.

## Action vocabulary

The router currently emits the actions below. New actions must be
added in pairs: the router emits and the policy file references the
same key.

| Action                       | Risk default | Description                                                          |
| ---------------------------- | ------------ | -------------------------------------------------------------------- |
| `approval_approve`           | medium       | A founder approval is recorded.                                      |
| `approval_reject`            | low          | A founder rejection is recorded.                                     |
| `approval_request_edit`      | low          | A founder asks for an edit before re-review.                         |
| `approval_escalate`          | high         | A founder escalates to another role (legal, security, finance).      |
| `worker_retry`               | low          | A worker retry is requested from the console.                        |
| `agent_disable`              | high         | An agent kill switch is flipped to disabled.                         |
| `agent_enable`               | medium       | An agent kill switch is flipped to enabled.                          |
| `scorecard_refresh`          | low          | A founder-triggered control-plane scorecard refresh.                  |
| `risk_accept`                | high         | The founder accepts a tracked risk with a written justification.     |
| `sovereign_readiness_refresh`| low          | The founder triggers a sovereign readiness recompute.                |
| `campaign_draft`             | low          | The Founder Console records a campaign draft request.                |
| `experiment_draft`           | low          | The Founder Console records a new experiment draft.                  |
| `outreach_draft_suppressed`  | low          | The Distribution Operator refused to queue a draft due to suppression. |
| `policy_change`              | critical     | The policy file was changed; founder approval required.              |
| `data_export`                | critical     | A customer-data export was authorized and executed.                  |

## Payload conventions

`payload_json` is a single JSON object. The conventions:

- Keys are snake_case.
- Values are scalars, arrays, or nested objects.
- A `note` field carries founder-supplied free text where applicable.
- Long text fields are capped at the FastAPI model level
  (typically 5000 chars).
- No secret or token is ever written to the payload.

Examples:

```json
{"note": "Approved after evidence pack 1247 review."}
{"reason": "Drift in cost per draft; pausing pending review.", "incident_id": "inc_2026_05_18"}
{"escalate_to": "founder", "reason": "Customer requested 60-day terms."}
```

## Risk levels and review cadence

| Risk      | Operational meaning                                                  | Cadence                                  |
| --------- | -------------------------------------------------------------------- | ---------------------------------------- |
| `low`     | Routine action. Reviewed in aggregate weekly.                        | Weekly scorecard summary.                |
| `medium`  | Notable. Surfaces in the daily founder brief.                        | Daily founder brief.                     |
| `high`    | Material. Triggers a trust flag if not paired with evidence.         | Same-day review.                         |
| `critical`| Material with downstream consequences. Triggers paging path.         | Immediate.                               |

## Read path

The Founder Console exposes `/api/v1/internal/audit/events`, which
maps each row to a UI-friendly shape:

| Field   | Source column |
| ------- | ------------- |
| `id`    | `id`          |
| `actor` | `actor`       |
| `action`| `action`      |
| `ts`    | `ts`          |
| `risk`  | `risk`        |

The full payload is read directly from the CSV by downstream
analytics. The endpoint does not surface the payload to avoid
accidentally exposing sensitive content via the read path; a future
endpoint will offer a payload view with scoped redactions.

## Append discipline

The ledger is append-only by convention. Properties:

- The router opens the file with mode `"a"`.
- The header row is written exactly once, on file creation, by the
  router or the bootstrap script. Subsequent appends do not rewrite
  the header.
- Editing or deleting rows is itself an action that requires a
  separate record. In practice, no role inside Dealix has approval to
  edit the file.

## Failure modes

| Failure                                | Behavior                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------ |
| Runtime directory unset                | Audit row is still returned to the caller; not persisted. Surface as ops incident. |
| Disk full                              | Append raises; endpoint returns 500; alerting fires.                     |
| Concurrent append                      | File is opened append-only; tail rows may interleave but never overwrite. |
| Schema drift                           | Reader is tolerant to extra columns; mismatched schema in legacy rows is logged. |

## Verifier

`scripts/verify_governance.py` and `scripts/verify_governance_rules.py`
inspect a sample of audit rows for shape and reasonable distributions
of `risk`. Any deviation surfaces as a CI warning.

## Why the ledger is the source of truth

The audit ledger is the only artifact that can prove, after the fact,
that the trust plane held. The policy file says what should have
happened; the audit says what did happen. When the two diverge, the
audit is what we examine first. Everything else is theory.
