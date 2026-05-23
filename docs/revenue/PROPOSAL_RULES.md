# Proposal Rules

> What every proposal Dealix sends must include.
> Enforced by the proposal template + a pre-send checklist.

## When To Send A Proposal

A proposal is sent **only when** all of these are true:
- Prospect has completed a Free Diagnostic OR has a strong warm intro
- Prospect has explicitly asked for one OR a discovery call closed with proposal commitment
- The rung is identified (see `OFFER_LADDER.md`)
- The fit score is ≥ 60
- The founder has approved the send (no auto-send proposals, ever)

## Required Sections

Every proposal must contain — in this order:

1. **Cover** — buyer name, company, date, proposal number, valid-until date (default 14 days)
2. **What you said you want** — restate the prospect's stated need in their language
3. **What we propose** — exact rung from the ladder, no custom variants
4. **Scope (in / out)** — bullets, explicit; "out" matters as much as "in"
5. **Deliverables** — list, each with a checkbox
6. **Timeline** — milestones with dates
7. **Price** — SAR, before VAT, with VAT shown separately
8. **Payment terms** — payment up front, terms link, accepted methods
9. **Trust & approvals** — one paragraph: AI prepares, you approve, we log everything
10. **Evidence pack** — link or attachment to a sanitized prior sample
11. **Next step** — single CTA (sign / pay / kick-off date)
12. **Refund / cancellation** — link to `BILLING_POLICY.md` clause

## Required Refusals (in the proposal itself)

Each proposal explicitly states what we **won't** do, to set expectations:
- Not a full marketing service
- Not autonomous; founder approves all external sends
- Not a long-term contract (Sprint and Data Pack are one-time; retainers are month-to-month with 30-day cancellation)
- Not negotiated below the productized price (politely)

## Banned Language

- "Up to X% increase"
- "Industry-leading"
- "Best in class"
- "Revolutionary"
- "AI will handle everything"
- "Set and forget"
- "Guaranteed results" (unless legally enforceable)
- Any claim that fails `claim_guard.py`

## Approval Flow

1. Agent drafts proposal from template + qualified lead data → A0
2. Founder reviews proposal → A1 approval (or revision request)
3. Trust check: claim_guard pass + suppression check → automated
4. Founder sends → log to `trust/approval_log.csv`
5. Calendar reminder set for 7 days post-send (follow-up)
6. Stage moves: call_booked → proposal_sent

## Pricing Discipline

- Use the rung price as printed in `OFFER_LADDER.md`
- Do not "round down" to make it look cleaner
- Do not bundle two rungs at a discount (sequential only)
- Always show VAT separately
- Always show the cancellation terms

If a buyer asks for a discount mid-negotiation:
- Refer to founding-customer slots (cap of 3) if any remain
- Otherwise: offer the rung below, not a discount on the asked rung
- Document the conversation in `pipeline/objections.md`

## Proposal Quality Checklist (pre-send)

```
[ ] Buyer name + company correct
[ ] Sector + segment match qualification record
[ ] Rung matches offer ladder exactly
[ ] No banned language
[ ] Price + VAT shown
[ ] Valid-until date set (default +14 days)
[ ] Evidence pack link works
[ ] CTA single and clear
[ ] Cancellation clause linked
[ ] PDF rendered cleanly (no template variables left)
[ ] Suppression check passed
[ ] claim_guard.py passed
[ ] founder reviewed within last 24 hours
```

If any box is unchecked, the proposal does not leave.

## What Happens After Send

- Stage moves to proposal_sent
- 7-day follow-up scheduled
- If no reply at day 14: founder-personal follow-up
- If no reply at day 21: explicit "still considering or close?" message
- If declined: log objection in `pipeline/objections.md`, move to closed_lost

## Review Cadence

- Per send: pre-send checklist + founder approval
- Weekly: % proposals that convert (target 35%)
- Monthly: pattern review — which rung wins / loses?

## What This Policy Refuses

- Multi-tier "Bronze/Silver/Gold" proposals (we don't do this)
- Verbal commitments without a written proposal
- Proposals to anyone who hasn't been qualified
- Sending the same proposal to multiple prospects in bulk
