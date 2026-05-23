# Revenue Desk — Delivery Playbook

> Custom AI tier. Highest trust posture. Lowest tolerance for ad-hoc.

## Engagement Lifecycle

```
Qualification → SOW → Setup → Monthly cycle → Quarterly review → Renewal or close
```

## Qualification (gate)

Must have all:
- 3+ months Managed Ops with positive trust audit
- Founder approval to offer this tier
- Advisor review (external)
- Customer fits non-prohibited use cases

## SOW (gate)

SOW must include:
- Scope (in / out, explicit)
- Setup deliverables + dates
- Monthly deliverables + cadence
- Custom approval matrix (specific actions, approvers, automation tier)
- DPA with data flows + retention + deletion terms
- Pricing + payment schedule + 60-day notice
- Trust audit cadence + scope
- Incident response SLA (< 4 hr)

## Setup (30–60 days)

- Day 1–7: technical discovery — what's the client's stack, what data, what workflows
- Day 8–21: build/integrate per SOW scope
- Day 22–30: dry runs with founder + advisor + client review
- Day 31–60: phased go-live with daily check-ins for first 2 weeks

## Monthly Cycle (after setup)

Similar to Managed Ops Playbook **plus**:
- Custom-scope deliverables per SOW
- Dedicated approval matrix executed
- Custom evidence pack format
- Monthly client + founder strategic call (60 min, not 30)

## Quarterly Review

- Trust audit (extended scope)
- ROI review with advisor present
- SOW health: is scope still right? Anything to add/remove?
- Renewal conversation if approaching contract end

## Approvals

- Standard outreach: A1 (founder per batch)
- Custom integration changes: A4 (require SOW amendment)
- Public claim about this client: A4 (prohibited without explicit consent + DPA addendum)
- Sharing client data with third parties (e.g., contractor): A4 + client consent

## Trust Risk Inventory

Higher than Managed Ops:
- Integration access to client systems
- Custom data flows
- Potentially regulated data domains (varies by client sector)
- Higher revenue exposure (SAR 5K–25K/mo)

Mitigations:
- DPA + custom approval matrix
- Quarterly external advisor review
- Higher Trust scorecard threshold for renewal (≥ 95)
- Incident response < 4 hr

## Done Definition (per month)

- Standard Managed Ops deliverables shipped
- Custom SOW deliverables shipped
- Approval log complete
- Trust audit pass
- Monthly strategic call attended

## When Things Go Wrong

- L1 (single deliverable late): apologize, fix, log
- L2 (multiple deliverables late or trust audit gap): credit + root cause + advisor briefed
- L3 (integration failure with client downstream impact): immediate engineering response + post-incident review + advisor + possible refund

Every miss → `clients/{client}/delivery_misses.md` + `learning/`.

## Throughput Cap

Max 2 active Revenue Desk engagements at any time this year. Above 2 → must hire delivery analyst before accepting third.

## When To Refuse Revenue Desk

- Client wants to skip productized rungs (revenue temptation, customer fit failure)
- Client wants white-labeling
- Client wants A4 automation
- Founder bandwidth < 30 hr/month free
- Client has prior trust incident
- Sector is outside our proven Tier 1 list
