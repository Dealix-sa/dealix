# Revenue Sprint Kit (Public)

> The kit the founder uses to **sell** a Revenue Sprint. Customer-facing language only.

A Revenue Sprint is a **7-day engagement** that delivers one of these named
outcomes, picked from a short menu before the sprint starts:

| Outcome | Deliverable | Who it's for |
|---|---|---|
| **Pipeline Lift** | 25 qualified, named leads + 5 warmed conversations | B2B founders pre-product-market-fit |
| **Outreach Pack** | 25 personalised DMs / emails ready to send + response playbook | B2B founders with a pipeline but no outreach motion |
| **Proof Pack** | Customer-ready sample showing your offer's measurable value | Founders losing deals at the "show me" stage |
| **Pricing Reset** | New price card + objection rebuttal pack + scripts | Founders under-pricing or hearing "too expensive" |
| **Retainer Bridge** | Plan + scripts to convert a one-off project into a retainer | Founders with happy clients and no recurring revenue |

## Kit contents

The kit lives in this directory:

- `founder_dm_pack.md` — drafted DM/email patterns the founder picks from.
- `sample_pack_template.md` — template for the *Proof Pack* outcome.
- `proposal_fast_template.md` — proposal template (fits on one page).
- `client_intake.md` — intake form filled with the client on day 0.
- `delivery_report_template.md` — final report template.
- `qa_checklist.md` — internal QA before anything ships to the client.
- `handoff_template.md` — end-of-sprint handoff.
- `feedback_request.md` — explicit ask for written feedback.
- `retainer_ask.md` — explicit ask for the next engagement.

## Pricing

- **First sprint:** SAR 2,500 (introductory, capped to first 5 clients).
- **Standard:** SAR 7,500.
- **Bundle (2 sprints + retainer):** SAR 18,000.

## What the kit is *not*

- Not a managed service.
- Not custom dev work.
- Not a long-term audit.
- Not a one-hour consult.

If a prospect needs any of the above, surface it in
`founder/decision_queue.md` and move on — do not say yes inside the sprint
scope.

## How it's verified

The verifier `scripts/verify_revenue_sprint_kit.py` enforces that every file in
the "Kit contents" list above exists and is non-empty. The audit fails if any
is missing.

## Related

- `docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md` — how the sprint is delivered.
- `docs/revenue/REVENUE_COMMAND_CENTER.md` — how the sprint is sold.
