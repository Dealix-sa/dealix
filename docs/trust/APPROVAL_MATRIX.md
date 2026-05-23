# Approval Matrix

> The canonical table of who/what approves which actions.
> Enforced in code by `dealix/trust/approval_matrix.py`.

## Tiers

- **A0** — Internal-only artifact (drafted, never shared externally). No approval needed.
- **A1** — External action with a specific individual recipient. Founder approval required per item until volume justifies batch approval.
- **A2** — External action with a defined audience. Founder approval per batch.
- **A3** — Public claim (LinkedIn, web, case study). Founder + evidence pack required.
- **A4** — Prohibited from automation. Founder + advisor for execution; never agent-only.

## Matrix

| Action class | Default tier | Founder required? | Advisor required? | Notes |
|---|---|---|---|---|
| Internal lead scoring | A0 | no | no | Agent-executable |
| Lead enrichment from allow-listed sources | A0 | no | no | Agent-executable |
| Message draft generation | A0 | no | no | Agent-executable |
| Sending first outreach DM | A1 | yes | no | Per-item until 50/wk sustained |
| Sending follow-up in active thread | A2 | yes | no | Batch-approvable |
| Sending proposal | A1 | yes | no | Per-item, always |
| Sending invoice | A1 | yes | no | Per-item, always |
| Pricing change (any rung) | A2 | yes | no | Logged in pricing_experiments |
| Refund / credit | A4 | yes | yes | Never auto |
| Contract change | A4 | yes | yes | Never auto |
| Public claim — generic post | A3 | yes | no | claim_guard pass + founder |
| Public claim — case study | A3 | yes | yes | + client signoff |
| Compliance / regulated claim | A4 | yes | yes | Prohibited automation |
| Sharing client data externally | A4 | yes | yes | DPA + client consent required |
| Onboarding contractor with data access | A4 | yes | yes | NDA + scoped access only |
| Suppression list removal | A4 | yes | yes | Almost never |
| Outreach to suppression-list contact | A4 | — | — | Blocked in code |
| Sending on Saudi public holiday | A4 | — | — | Blocked in code |
| Cold WhatsApp | A4 | — | — | Blocked in code |

## Enforcement

- Code path: `dealix/trust/approval_matrix.py`
- Every external-facing function imports `approval_matrix.tier_for(action)` and `approval_matrix.require_approval(action, approver, evidence)`
- If approval missing → raises `ApprovalRequired` exception
- All decisions logged to `trust/approval_log.csv` (private repo)

## Audit

- Daily: review yesterday's `approval_log.csv` for any A4 (should be 0)
- Weekly: spot-check 5 random A1/A2 entries — did the founder really approve?
- Monthly: full count by tier; trend over time
- Quarterly: re-validate matrix against actual incidents

## Changes To The Matrix

A matrix entry can only change with:
- PR titled `[MATRIX] {action_class}: {from_tier} → {to_tier}`
- Cited reason (incident, data, advisor input)
- Founder approval
- Update to test suite in `tests/trust/test_approval_matrix.py`
- Note in `DEALIX_DECISION_RULES.md` changelog

## What This Matrix Refuses

- Implicit approvals ("we always do this, no need to check")
- Bulk approvals via UI without per-item review for A1
- Lowering a tier to ship faster
- Adding new action classes without explicit tier assignment
- Treating "no rule yet" as "do whatever" — the default for an unknown action is A4
