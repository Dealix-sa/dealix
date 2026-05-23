# Managed Ops Pilot — Delivery Playbook

> Monthly cycle. Cannot deviate without logging in `clients/{client}/delivery_notes.md` (private).

## Pre-Month Setup (last week of prior month)

- Confirm month invoice paid → no payment, no month
- Update sector playbook with last month's learnings
- Refresh suppression list
- Confirm approval matrix is current for this client

## Week 1 — Sourcing + Scoring

- Source 100 new prospects (allow-listed sources only)
- Score using `dealix/agents/scoring_agent.py`
- Filter / enrich top 60 (fit ≥ 65)
- Founder QA spot-check 10 random rows
- Add to client's prospect tracker (private)

## Week 1 (parallel) — Outreach Drafts Batch 1

- Pull sector playbook patterns
- Draft 25 personalized outreach messages (AR + EN as appropriate)
- Run `claim_guard.py` on all
- Send for founder approval
- On approval: hand off to client to send (we don't send)

## Week 2 — Outreach Drafts Batch 2 + Bi-Weekly Report 1

- Draft next 25 outreach messages
- Compile bi-weekly report:
  - Pipeline metrics (replies, calls, proposals from prior outreach)
  - Trends (sector, timing, message variants)
  - 3 recommendations for next 2 weeks
  - Trust check status
- Founder review + send

## Week 3 — Outreach Drafts Batch 3 + Sample Artifact

- Draft next 25 outreach messages
- Refresh sector sample artifact (one per month per client sector)
- Founder approval
- Hand off to client

## Week 4 — Outreach Drafts Batch 4 + Bi-Weekly Report 2 + Trust Audit + Founder Session

- Draft final 25 outreach messages
- Compile second bi-weekly report
- Trust audit:
  - Approval log complete?
  - Any claim_guard fails?
  - Any suppression breaches?
  - Any incidents to log?
- 30-min monthly working session with client (founder leads)
- Capture client feedback live

## Monthly Wrap

- All deliverables shipped
- All approvals logged
- Client invoice for next month sent (5 days before due)
- Update `clients/{client}/monthly_summary-{month}.md` (private)
- Append to `DEALIX_EXECUTION_LEDGER.md` — one row per client per month

## Time Per Month (founder hours)

~14 hr/client/month. Cap: 3 active Managed Ops at founder-only execution → 42 hr/month. Above 3 → contractor (see HIRING_TRIGGERS).

## Approvals

- Outreach drafts: A1 per batch (founder approves)
- Sample artifacts: A2 (founder approves)
- Public claims about this client: A4 (prohibited without client consent)
- Sharing client data: A4 (prohibited without client consent)

## Risk Flags

- Month 1 client adoption low (not sending the drafts) → schedule unscheduled check-in week 2
- Client wants scope expansion mid-month → "Yes, that's a custom add; let's price it for next month"
- Client wants white-labeling → refuse, escalate
- Trust audit fail → halt next month's work until root-caused

## Done Definition

Monthly delivery is "done" when:
- 6 deliverables shipped on time
- All approvals logged
- Trust audit clean
- Next-month invoice issued
- Working session completed
- Monthly summary written

## When Things Go Wrong

- L1 (single deliverable late): apologize, fix in 24 hr, log
- L2 (≥ 2 deliverables late or trust audit fail): credit + root cause + advisor review
- L3 (incident affecting client externally): immediate stop + refund pending review

Every miss → `clients/{client}/delivery_misses.md` + aggregated to `learning/`.
