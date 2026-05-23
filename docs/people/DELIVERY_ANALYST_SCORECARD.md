# Delivery Analyst Scorecard

> Used at 30 / 60 / 90 day check-ins.

## Role Summary

Owns sourcing for active sprints, first-draft deliverables (founder reviews), QA checklist execution, handoff doc preparation.

## Per-Sprint Outputs

| Metric | Day 30 | Day 60 | Day 90 |
|---|---|---|---|
| Sprints supported per week | 1 | 2 | 2–3 |
| First-draft deliverable on time | 100% | 100% | 100% |
| QA failure rate (first pass) | < 20% | < 10% | < 5% |
| Handoff doc completeness | 100% | 100% | 100% |
| Founder review time on drafts | < 90 min | < 60 min | < 45 min |

## Weekly Outputs

| Metric | Day 30 | Day 60 | Day 90 |
|---|---|---|---|
| Hours logged | 20 | 30 | 40 |
| Stakeholder updates timely | 100% | 100% | 100% |
| Issues escalated appropriately | 100% (when warranted) | 100% | 100% |
| Process compliance | per `DELIVERY_PLAYBOOK.md` | per playbook | per playbook |

## Behaviors

- Follows the Delivery Playbook exactly until variation is explicitly approved
- Uses only allow-listed data sources
- Sanitizes any client data appearing in samples per `SAMPLE_GENERATION_SYSTEM.md`
- Runs `claim_guard.py` on every artifact
- Surfaces issues before they affect handoff
- Documents progress daily in `clients/{client}/progress.md`

## Red Flags

- Skips QA checklist boxes "to save time"
- Edits a founder-approved deliverable after approval
- Uses non-allow-listed data sources
- Doesn't run claim_guard
- Pushes a deadline without notice
- Doesn't escalate when uncertain

## Trust Posture

- No A3/A4 approvals (founder only)
- Trust questions always escalate
- Suspected privacy breach → halt + escalate immediately

## Compensation

- Monthly retainer (PT or FT)
- No revenue commission this quarter
- Quarterly bonus tied to delivery on-time + QA score (capped)

## Tools

- Allow-listed enrichment sources
- Pipeline + delivery trackers (private repo)
- Internal agents (sourcing, scoring) — under approval matrix
- Document templates from `docs/delivery/`

## 30/60/90 Decision

- **30 days:** continue, with coaching
- **60 days:** continue, expand to 2 sprints if scorecard green
- **90 days:** continue, expand to 2–3 sprints, OR end relationship

## Onboarding Plan (first 30 days)

- Week 1: read all `docs/delivery/` + shadow one Sprint
- Week 2: support one Sprint under direct founder supervision
- Week 3: lead one Sprint with founder review at each step
- Week 4: lead Sprint with founder review at handoff only

## What This Role Refuses

- Client-facing decisions without founder
- Trust approvals
- Pricing or scope conversations
- Direct contact with clients on sensitive topics
- Sending deliverables to client without founder signoff
