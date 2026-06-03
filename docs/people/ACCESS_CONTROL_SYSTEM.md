# Access Control System

## Purpose
Grant the minimum access needed, log every change, and revoke quickly.

## Access tiers
- **T0 — None**: no access to any Dealix system.
- **T1 — Read public**: public repo + public docs.
- **T2 — Read private (scoped)**: read access to one specific folder of `dealix-ops-private/`.
- **T3 — Write scoped**: write access to one specific folder of `dealix-ops-private/`.
- **T4 — Write production**: write access to operational data stores.
- **T5 — Founder**: full access.

## Default by role
| Role | Tier |
|---|---|
| Visitor | T1 |
| Engineer sub-agent | T1 (PR-only to public repo) |
| Content contractor | T2 (scoped to `content/`) |
| Lead-gen contractor | T3 (scoped to `acquisition/`, `pipeline/` write append-only) |
| Delivery operator | T3 (scoped to assigned client folders) |
| Founder | T5 |

## Process
1. Request access in `people/access_log.csv` with `decision=Pending`.
2. Founder approves or rejects with reason.
3. Access provisioned by founder (no self-grant).
4. Access reviewed at days 30, 60, 90.
5. Access revoked on exit or change of scope.

## Audit
- Monthly: review the access log for stale grants.
- Quarterly: tabletop a credential leak; verify revoke path works.

## Forbidden
- Shared accounts.
- Long-lived API keys without rotation schedule.
- Granting access during sales calls "to demo something".
