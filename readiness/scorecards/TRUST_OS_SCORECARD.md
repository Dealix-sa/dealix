# Trust OS Scorecard (out of 100)

| Signal | Points | This Week | Notes |
|---|---|---|---|
| Approval log updated 100% | 20 | _____ | no untracked external action |
| Zero A4 violations | 20 | _____ | binary; any = 0 |
| claim_guard pass on every published artifact | 15 | _____ | |
| Suppression list checked on every send | 15 | _____ | code-enforced |
| No SEV-1/SEV-2 incidents this week | 15 | _____ | |
| Daily approval queue cleared (< 48 hr) | 10 | _____ | |
| Quarterly evidence-pack audit current | 5 | _____ | |

**Total:** ____ / 100

## Thresholds
- 95–100 — Excellent (required for Custom AI customers)
- 90–94  — Good (required for Managed Ops customers)
- 80–89  — Acceptable for Sprint customers; remediate
- < 80   — Halt sends; root-cause; founder + advisor

## Trust Drift Triggers

If any of these fire — same-day escalation to founder:
- A4 violation logged
- claim_guard miss surfaced after publish
- Suppression breach detected
- SEV-1 or SEV-2 incident opened
- Audit log gap > 24 hr unexplained
