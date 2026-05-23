# Incident Response System

## Purpose
Define how Dealix detects, contains, and recovers from security and reliability incidents.

## Severity levels
| Level | Definition | Example |
|---|---|---|
| SEV-1 | Customer data exposure or revenue-critical outage | Production DB unreachable; credentials leaked |
| SEV-2 | Significant degradation, no data exposure | API 5xx > 5% for 15 minutes |
| SEV-3 | Limited impact, single feature degraded | Background worker stuck; one tenant impacted |
| SEV-4 | Cosmetic / minor | Stale dashboard tile |

## Phases
1. **Detect** — alerts from health checks, error rates, customer reports.
2. **Triage** — within 15 min for SEV-1/2 confirm scope, assign owner.
3. **Contain** — stop the bleeding (rotate keys, disable feature, flip flag).
4. **Eradicate** — remove the root cause.
5. **Recover** — restore service; verify with healthcheck + smoke test.
6. **Learn** — post-incident review within 5 business days.

## Communication
- SEV-1: founder posts public status update within 30 min; customer email within 4 hours.
- SEV-2: customer email if any customer is affected.
- SEV-3/4: internal only unless reported by customer.

## Artifacts produced per incident
- Incident ticket / log entry in `dealix-ops-private/trust/approval_log.csv`.
- Timeline (UTC) of events.
- Root cause analysis.
- Action items with owners and due dates.

## On-call
- Founder is primary on-call until first hire.
- Secondary: TBD upon first contractor with production access.

## Drills
- Quarterly restore drill (DB + private ops).
- Annual tabletop simulation of a SEV-1 data-exposure event.
