# Delivery Playbook

> Step-by-step. Detailed enough that another competent operator can
> follow it.

## §1 Intake (Day 0)

1. Customer signs scope.
2. Payment / PO received.
3. Create `dealix-ops-private/clients/<client_id>/` directory.
4. Copy `CLIENT_INTAKE.md` template, fill it.
5. Schedule onboarding call.

## §2 Onboarding (Day 1)

See `docs/client_success/ONBOARDING.md` for the canonical script.

Outputs:
- Confirmed ICP definition.
- Confirmed signal preferences.
- Confirmed tone (Arabic + English).
- Confirmed delivery channel (CRM, spreadsheet, email).

## §3 Research (Days 2–3)

1. Pull initial lead universe from approved data sources.
2. Run AI-01 (Lead Scorer) on the universe.
3. Add manual enrichment for top-150 candidates (founder + analyst).
4. Save per-account research file with evidence links.

Audit gate: every claim in research is traceable to source.

## §4 Deduplication (Day 4)

1. Run dedupe across:
   - Within current Sprint lead set.
   - Against customer's existing CRM (if shared).
   - Against accounts the customer flagged "do not contact".
2. Resolve conflicts (same legal entity, different domain).

## §5 Scoring (Days 4–5)

Apply `SCORING_RULES.md`.
- A-priority: ≥ 20/25.
- B-priority: 14–19.
- C-priority: 8–13.
- Disqualified: < 8.

Output: ranked spreadsheet.

## §6 Outreach Pack (Days 6–8)

For each A and B-priority account:

- Personalised DM (LinkedIn) — 4–6 sentences.
- Personalised email — 6–10 sentences.
- Bilingual (Arabic + English).
- Each message references the specific signal that triggered the score.
- AI-02 produces drafts; founder + analyst review.

## §7 Executive Memo (Day 9)

One-page memo: see `REPORT_TEMPLATE.md`.

- Segment summary.
- Notable patterns.
- 3 highest-leverage opportunities.
- Unknowns and caveats.

## §8 QA (Day 10)

Run `QA_CHECKLIST.md`. Fix any fail.

## §9 Approval (Day 11)

Founder T2 sign-off on:
- The Proof Pack as a whole.
- Each outreach draft if the customer asked us to send on their behalf.

## §10 Handoff (Day 12)

Run the handoff call. See `HANDOFF_TEMPLATE.md`.

## §11 Feedback + Retainer Ask (Days 13–14)

- Send feedback request.
- Send retainer proposal.
- Log in `dealix-ops-private/client_success/retainer_asks.csv`.

## Mid-Sprint Change Orders

If the customer asks for scope change mid-Sprint:

- If it adds < 2 hours of work and is reasonable: founder approves
  in writing; no price change.
- If it adds > 2 hours: written change order, additional fee, signed
  before work proceeds.

## Sprint Close

- Update `sprint_register.csv` (delivered date, paid status, retainer
  outcome).
- Update friction log with any process pain.
- Update capital asset registry.
