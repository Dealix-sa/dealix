# Dealix Approval Matrix

Every AI-generated artifact crosses one of these five approval levels before it reaches a customer, a bank account, or the public web.

## Purpose
Define a single approval taxonomy so any agent, any contributor, and the founder all use the same vocabulary for who must sign off on what.

## Owner
Sami (Founder, Trust OS).

## Review Cadence
Monthly. Adjust when a new surface appears or after an incident.

## Inputs
- Autonomy policy (`docs/trust/AUTONOMY_POLICY.md`).
- Surface-by-surface risk assessment.
- Recent approval log entries.

## Outputs
- The matrix below.
- Approval log entries (private).
- Trust loop evidence in the scorecard.

## Rules
- Approval level is decided before the agent acts, not after.
- A higher autonomy surface always uses a lower approval level (or stays at `Never`).
- An incident on a surface bumps it down one approval level until re-graduated.

---

## The Five Approval Levels

### A0 — No approval required
- Agent acts immediately. Internal-only artifacts that touch no customer, no money, no public surface.
- Examples: internal scoring drafts, internal dashboards, internal markdown notes.

### A1 — Async founder review
- Agent acts, but a human review is logged within 24 hours.
- Examples: internal proof pack drafts, internal research notes.

### A2 — Founder approves before send
- Agent prepares. Founder reads and approves before anything leaves the building.
- Examples: outbound DMs, outbound emails, proposals, customer reports, public website edits.

### A3 — Founder approves with second signal
- A2 plus a logged second signal (test customer, sample reply, sandbox run).
- Examples: pricing changes, autonomy graduations, new offer rungs, retainer conversions.

### Never — Prohibited
- Surfaces an AI agent must never touch directly, regardless of approval.
- Examples: bank transfers, password changes, irreversible account changes, public claims about customers Dealix has not delivered for.

---

## Mapping To Common Surfaces

| Surface | Approval | Notes |
|---|---|---|
| Internal markdown draft | A0 | Author + reviewer in commit message. |
| Internal dashboard | A0 | Read-only. |
| Lead scoring CSV | A1 | Founder spot-checks weekly. |
| Outreach DM / email | A2 | Founder approves before send. |
| Customer-facing report | A2 | Founder signs the cover. |
| Public landing page | A2 | Same as customer-facing. |
| New offer rung / pricing | A3 | Plus second-signal test. |
| Autonomy upgrade for any surface | A3 | Plus retro from last 4 weeks. |
| Bank / payment changes | Never | Founder only, manually. |
| Production secrets | Never | Founder only, manually. |

## Metrics
- Number of approvals logged per week.
- Number of approvals rejected on first review (signal of AI prep quality).
- Number of `Never` violations attempted (target: zero).

## Evidence
- `dealix-ops-private/trust/approval_log.csv` with one row per approval.
- Weekly review reads the log and updates the scorecard.

## Last Reviewed
2026-05-23
