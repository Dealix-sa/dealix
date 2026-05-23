# Revenue Sprint Delivery Playbook

The 7-day operating manual for delivering a paid Revenue Intelligence Sprint (Offer Rung 2 / 499 SAR).

## Purpose
Give the delivery team (founder + AI sub-agents) a day-by-day recipe to take a paid customer from kickoff to a signed proof pack in exactly 7 days.

## Owner
Sami (Founder, Delivery OS).

## Review Cadence
After every delivered sprint. Update Rules section if a new failure mode appears.

## Inputs
- Signed Rung 2 proposal and payment reference.
- Customer kickoff form (company, ICP, current motion).
- Source data passport from the customer.
- Sub-agent capacity (data_os, governance_os, proof_os, value_os).

## Outputs
- DQ score document.
- Account scoring sheet.
- Draft outreach pack (3 sequences).
- Governance review file.
- Proof pack (single PDF + folder).
- Retainer offer at the end of day 7.

## Rules
- No day may end without a logged artifact.
- No customer-facing output is sent without founder approval.
- No private customer data leaves the private repo.
- Source passport must be completed before scoring begins.

---

## Day-by-Day

### Day 0 — Kickoff (same day as payment)
- Open `clients/<client_name_private>/` in the private repo.
- Run the kickoff form. Capture: ICP, current motion, top 3 questions.
- Drop the source data into `delivery/research/` (private).

### Day 1 — Source Passport
- AI sub-agent `data_os` generates the source passport.
- Founder reviews. File stored in `clients/<client>/source_passport.md`.

### Day 2 — Data Quality Score
- DQ score computed. Documented thresholds, missing fields, risk areas.
- Output: `clients/<client>/dq_score.md`.

### Day 3 — Account Scoring
- 50–250 accounts scored against the customer ICP.
- Output: `clients/<client>/account_scoring.csv`.

### Day 4 — Draft Outreach Pack
- AI prepares 3 outreach sequences per top segment.
- Founder reviews and approves wording.
- Output: `clients/<client>/outreach_pack.md`.

### Day 5 — Governance Review
- `governance_os` agent runs trust checks: PII handling, claims supportable, autonomy honored.
- Output: `clients/<client>/governance_review.md`.

### Day 6 — Proof Pack Assembly
- `proof_os` agent compiles all artifacts into the final proof pack.
- Output: `clients/<client>/proof_pack.pdf` and `proof_pack/` folder.

### Day 7 — Handoff and Retainer Offer
- Founder delivers proof pack to customer.
- Founder offers Rung 3 (Managed Pilot) or Rung 4 (Revenue Desk) in writing.
- Output: `clients/<client>/handoff_notes.md` and `next_offer.md`.

---

## Failure Modes (Update On Discovery)

- Customer data arrives late → day 0 is paused; sprint timer restarts.
- DQ score reveals unusable data → switch offer to data hygiene scope; refund partial if no value possible.
- No reply by day 7 on retainer offer → schedule a 15-minute review call in the next 7 days.

## Metrics
- Days from payment to proof pack (target: 7).
- Number of approved artifacts per sprint (target: 6).
- Conversion to Rung 3 or Rung 4 within 14 days of delivery.

## Evidence
- Folder per delivered sprint in `dealix-ops-private/clients/`.
- Signed proof pack stored alongside.
- Retainer offer logged in `dealix-ops-private/revenue/`.

## Last Reviewed
2026-05-23
