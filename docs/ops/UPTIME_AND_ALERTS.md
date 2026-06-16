# Uptime Monitoring + Alerting

## Monitors
| Service | Endpoint | Interval | Alert threshold |
|---------|----------|----------|-----------------|
| UptimeRobot | /healthz | 5 min | 2 min downtime |
| UptimeRobot | /api/v1/pricing/plans | 15 min | 5 min downtime |
| Better Stack (optional) | full status | 1 min | any fail |

## Alert Channels
- Email (primary): sami.assiri11@gmail.com
- SMS (critical): founder phone
- Slack: #dealix-alerts (when workspace exists)

## Response SLA
- Critical (site down): 15 min acknowledgment
- High (feature broken): 1 hour
- Medium (degraded): 4 hours
- Low (cosmetic): 24 hours

## Setup Guide
See Issue #85 for UptimeRobot setup steps.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
