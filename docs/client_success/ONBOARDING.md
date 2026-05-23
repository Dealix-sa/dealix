# Client Onboarding

> The first 7 days of every engagement.
> Same shape for Sprint, Data Pack, Managed Ops; scope adjusts.

## Day 0 — Payment + Welcome (≤ 1 hr)

- Confirm payment received → log in `revenue/cash_collected.csv`
- Send welcome email:
  - Confirm the rung + scope (link to OFFER.md)
  - Confirm timeline
  - Calendar invite for kickoff call (Day 1 ideally)
  - Trust posture one-liner: every external send needs your approval
- Create `clients/{client_name}/` from `_template/` (private repo)

## Day 1 — Kickoff Call (≤ 1 hr call + 30 min prep)

Agenda:
1. Confirm understanding of their goals (re-state)
2. Walk through scope (in/out, explicit)
3. Confirm data we'll collect + where it lives (privacy)
4. Confirm approval workflow (founder approves; we never send on their behalf during Sprint/Pack)
5. Confirm point of contact + cadence
6. Confirm logistics (handoff date, time zone, holidays in window)

Fill `CLIENT_INTAKE.md` during/after the call.

## Day 2–6 — Active Delivery

- Execute per `DELIVERY_PLAYBOOK.md` for the engagement type
- Daily progress note in `clients/{client}/progress.md` (private)
- Weekly Friday-pre-update if engagement spans > 1 week

## Day 7 — Handoff Call (≤ 30 min)

- Walk through deliverables
- Capture feedback live (`CASE_STUDY_CAPTURE.md`)
- Discuss next steps (rung upsell, soft)
- Schedule any follow-up

## Trust Posture (set in week 1)

- Client data stays in private repo only
- Approval matrix applied
- Suppression list honored
- All claims pass `claim_guard.py`
- Trust questions answered transparently

## Onboarding Quality Bar

The onboarding "passes" if:
- All 5 onboarding artifacts created (welcome email, calendar invite, intake doc, progress thread, handoff invite)
- Kickoff call completed on Day 1 (or Day 2 max)
- Intake document complete before Day 3
- Client confirms understanding of scope in writing
- No scope drift introduced during onboarding

## Common Onboarding Issues

- Client wants to expand scope mid-onboarding → "Yes, that's the next rung. Let's complete this and discuss."
- Client wants different deliverables → revisit `OFFER.md`, do not customize this quarter
- Client asks for written confidentiality → send NDA template from `legal/nda_template.md` (private)
- Client asks for DPA → send DPA template (required for Managed Ops month 2+ and Revenue Desk)

## Onboarding Cadence

- Same flow every time, no improvisation
- Variation = playbook update, not ad-hoc
- Founder owns onboarding personally until first hire

## What This Refuses

- Skipping the kickoff call ("we can just start")
- Verbal-only scope confirmation
- Starting work before payment received
- Custom onboarding for "VIP" clients
