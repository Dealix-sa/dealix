# Automation Permission Matrix

## Purpose
Decide what an automation is allowed to do without human confirmation.

## Categories
- **Read-only**: query files, summarize data, render reports.
- **Write-local**: write to `dealix-ops-private/` (private only).
- **Write-public**: commit to the public repo.
- **External-read**: fetch public URLs.
- **External-write**: send messages, post content, call APIs that change external state.

## Default permissions per actor
| Actor | Read-only | Write-local | Write-public | External-read | External-write |
|---|---|---|---|---|---|
| Founder | Y | Y | Y | Y | Y |
| Engineer sub-agent | Y | Y | Y (via PR) | Y | N |
| Sales sub-agent | Y | Y | N | Y | N |
| Delivery sub-agent | Y | Y | N | N | N |
| Content sub-agent | Y | Y | Y (via PR) | Y | N |
| Background cron | Y | Y | N | Y | N |

## Escalation rules
- An action that would change permissions logs the request in `people/access_log.csv` with `decision=Pending`.
- The founder explicitly approves before permissions widen.

## Audit
- Monthly: review `people/access_log.csv` for anomalies.
- Quarterly: tabletop a permission-escalation attempt.

## Forbidden
- Granting External-write to any sub-agent.
- Granting Write-public bypassing PR review.
- Caching credentials in agent state across sessions.
