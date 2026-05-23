# Suppression System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The suppression system is a first-class trust object. It is the
mechanism by which the Distribution Operator agent refuses to queue
outreach to identities that have opted out, requested deletion, been
flagged for risk, or are otherwise off-limits. A missed suppression
check is a critical incident, not a near miss.

## File and schema

The suppression list lives in the private ops runtime at
`outreach/suppression_list.csv`. The schema is bootstrapped by
`scripts/bootstrap_private_ops_runtime.py`:

| Column        | Type   | Notes                                                                     |
| ------------- | ------ | ------------------------------------------------------------------------- |
| `id`          | string | UUID. Stable across the row's lifetime.                                   |
| `match_type`  | enum   | `email`, `domain`, `phone`, `linkedin_handle`, `company`, `regex`.         |
| `match_value` | string | The literal value or regex pattern, normalized to lowercase where applicable. |
| `reason`      | string | Why suppressed. Free text, but constrained to a controlled vocabulary.    |
| `added_by`    | string | `founder`, `trust_guardian`, `customer_request`, `incident_response`.     |
| `added_at`    | ISO ts | UTC timestamp when the row was added.                                     |

The file is append-only. Rows are never deleted; suppressions can be
revoked by appending an inverse row tagged with the original id (see
`Lifecycle` below).

## Match types

| Type             | Semantics                                                                      | Example                        |
| ---------------- | ------------------------------------------------------------------------------ | ------------------------------ |
| `email`          | Exact match on the lowercased local part + lowercased domain.                  | `unsubscribed@acme.sa`         |
| `domain`         | Match any email whose domain matches (lowercased, sans subdomain stripping).   | `acme.sa`                      |
| `phone`          | Match phone numbers normalized to E.164.                                       | `+966555555555`                |
| `linkedin_handle`| Match a LinkedIn vanity slug, lowercased.                                      | `johndoe`                      |
| `company`        | Match a normalized company name (lowercased, trimmed, punctuation stripped).   | `acme industries`              |
| `regex`          | Reserved for incident response. Owner must be `trust_guardian` or `founder`.   | `(?i)riyadh-group-.*`          |

Match precedence (most specific wins): `email` > `phone` >
`linkedin_handle` > `domain` > `company` > `regex`. If any match
returns true the target is suppressed.

## How agents must consult the list

Every outreach draft must call the suppression check before the row
is appended to any outreach queue. The check sets
`suppression_check_ts` on the draft. The eval gate's
`suppression_compliance` suite asserts that this field is present
for every outreach draft. The policy adapter's
`no_suppressed_outreach` rule refuses the queue write when the
context carries `target_suppressed: true`.

The check is performed in the Distribution Operator worker. It runs
inside the worker because:

1. The full list is private and lives only in the runtime.
2. The check must be deterministic and auditable.
3. A network-side check (e.g., a remote API) is not allowed; the
   list is the source of truth.

## Lifecycle

Suppressions move through five states:

1. **Pending add.** A draft suppression row is created (e.g., from a
   customer reply containing an unsubscribe phrase). The Trust
   Guardian raises a trust flag.
2. **Active.** After review, the row is appended to
   `outreach/suppression_list.csv` and the trust flag is closed.
3. **Honored.** Every subsequent outreach draft against the matching
   identity is refused, and the refusal is recorded in
   `trust/approval_decisions.csv`.
4. **Revoke requested.** If a suppression must be lifted (e.g., the
   contact explicitly re-opts in), the Trust Guardian raises a new
   approval. The founder approves.
5. **Revoked.** A new row is appended with the same `id` and a reason
   prefix `revoke:`. The check honors the most recent state for the
   id.

The Trust Guardian agent is the only path that adds or revokes
suppression rows. The Distribution Operator only reads.

## How suppressions are added

There are four canonical sources:

| Source                      | Trigger                                                              |
| --------------------------- | -------------------------------------------------------------------- |
| Customer reply              | A reply contains an opt-out phrase in Arabic or English.             |
| Customer request            | A direct request via email, support form, or contract clause.        |
| Incident response           | A trust incident requires the identity to be removed from outreach.  |
| Founder discretion          | The founder marks an identity as off-limits for any reason.          |

Each source records the originating evidence (link, message id, or
incident id) in the trust flag that precedes the row.

## Match auditing

When the Distribution Operator detects a suppression hit, it records
an audit row with:

- `actor`: `distribution_operator`
- `action`: `outreach_draft_suppressed`
- `target`: the normalized match value
- `risk`: `low`
- `payload`: the draft summary, the matching row id, and the
  `match_type`.

The Founder Console surfaces these in the `/audit/events` feed so the
founder can monitor for false positives.

## Failure modes

| Failure                                            | Response                                                                 |
| -------------------------------------------------- | ------------------------------------------------------------------------ |
| Suppression file missing                           | The Distribution Operator stops queueing. It does not fail-open.         |
| Malformed row                                      | The row is skipped, a trust flag is raised at `severity: high`.          |
| Match across multiple types                        | The most specific match wins. The audit row records all matches.         |
| Regex with catastrophic backtracking               | The check times out per-row and treats the row as a hit (fail-closed).   |
| Concurrent writer                                  | Append-only; readers are tolerant to partially written tail rows.        |

## Operational discipline

- The suppression file is backed up in the same cadence as the rest of
  the private ops runtime. See `BACKUP_AND_RESTORE_OS.md`.
- The file is never exported off-host. Sharing the list externally is
  a data export and is policy-gated by
  `data_export_requires_escalation`.
- The file is reviewed monthly by the Trust Guardian. Stale `regex`
  rows are candidates for narrowing.

## What the suppression system is not

It is not a "do not contact" marketing preference list. It is a
trust artifact that overrides every other targeting decision. If a
sector targeting model recommends an account that is suppressed, the
suppression wins. If a referral arrives from a partner pointing at a
suppressed identity, the suppression wins. There is no escalation
path that bypasses suppression silently; revoking a suppression
requires a separate, audited approval.
