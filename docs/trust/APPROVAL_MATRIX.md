# Approval Matrix

The five-tier approval system that decides who must sign off on any action before it leaves Dealix.

## Purpose
Replace ad-hoc judgement with a written matrix. Every action that touches the outside world maps to exactly one tier — A0, A1, A2, A3, or Never. The matrix is the contract between the AI and the founder.

## Owner
Sami (Founder).

## Review Cadence
Monthly, against the approval log.

## Inputs
- The action queue prepared by AI.
- Customer-facing artifact drafts.
- Outbound message drafts.
- Payment / refund / contract events.

## Outputs
- A tier classification for every action.
- A signed entry in `trust/approval_log.csv` (private ops) for every action above A0.
- A blocked-action log for every "Never" attempt the system caught.

## Rules
- Every action is classified before execution. No action runs unclassified.
- A0 actions are logged but not approved.
- A1 actions require self-review by the founder, logged.
- A2 actions require founder plus one peer reviewer, both logged.
- A3 actions require founder, customer, and legal/financial sign-off where applicable.
- Never actions are blocked at the agent layer and produce an immediate alert.

## Metrics
- Number of actions per tier per week.
- Number of Never-tier attempts caught.
- Average approval latency per tier.
- Number of unclassified actions caught by verifier (target: 0).

## Evidence
- `trust/approval_log.csv` (private ops).
- Blocked-action log.
- Friction log entries for misclassifications.

## The Five Tiers

### A0 — No approval needed (logged only)
- Internal drafts, research notes, prompt iterations.
- Document edits that are not customer-facing.
- AI scratch work.

### A1 — Founder self-review (one signature)
- Outbound DMs and emails to known leads.
- Proposals under 5,000 SAR.
- Public LinkedIn posts under 200 words.
- Internal Slack-style messages to known partners.

### A2 — Founder + one peer (two signatures)
- Public statements and articles over 200 words.
- Proposals 5,000–25,000 SAR.
- New partnership outreach.
- Pricing changes to the offer ladder.

### A3 — Founder + external sign-off (three+ signatures)
- Contracts and master service agreements.
- Refunds and credit notes.
- Public partnerships and joint announcements.
- Proposals over 25,000 SAR.
- Any data-sharing commitment with a customer.

### Never — Forbidden actions (blocked at the agent layer)
- Cold scraping or unconsented data collection.
- Mass DMs or automated mass cold outreach.
- Automated payment without explicit founder approval.
- Public claims without a verified source.
- Customer data leaving the private boundary.

## Last Reviewed
2026-05-23
