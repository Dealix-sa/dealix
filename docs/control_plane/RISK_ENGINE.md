# Risk Engine

The Risk Engine maps boolean and numeric signals to a typed `Risk` list.

## Risk Areas

- `Revenue`
- `Delivery`
- `Trust`
- `Product`
- `Founder`
- `Legal/Compliance`
- `Reputation`

## Severities

`Low` → `Medium` → `High` → `Critical`.

`Critical` risks always escalate to the founder and to
`founder/risk_log.md` in the private ops repo.

## Signal Mapping

| Signal | Area | Severity |
|---|---|---|
| `payment_fallback_missing` | Revenue | High |
| `qa_checklist_missing` | Delivery | High |
| `public_repo_contains_leads` | Trust | Critical |
| `a3_action_attempted` | Trust | Critical |
| `ci_failing_on_main` | Product | High |
| `pending_founder_approvals > 15` | Founder | High |
| `public_safety_failures > 0` | Reputation | High |
| `overdue_client_deliveries > 0` | Delivery | Medium |

## Output Format

Each `Risk` carries `area`, `severity`, `title`, `detail`, `mitigation`,
and `as_of`. The risk log is regenerated, not appended, on each evaluation
so the log always reflects current signals.
