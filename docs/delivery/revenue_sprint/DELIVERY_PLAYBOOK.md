# Revenue Sprint Delivery Playbook

The seven-day playbook that produces a paid Revenue Sprint deliverable, end to end. Run by AI under founder supervision, with QA at every checkpoint.

## Purpose
Make the 499 SAR Revenue Sprint a productised, repeatable, profitable offering — not an artisanal consult. The playbook is the operating manual the AI follows when a customer pays for a Sprint. Founder reviews at three checkpoints; everything else runs on the playbook.

## Owner
Sami (Founder) — accountable. AI delivery agent — operator.

## Review Cadence
Monthly, against the last 5 Sprints delivered.

## Inputs
- Paid Sprint purchase signal from `revenue/cash_collected.csv` (private ops).
- Customer intake form (company, sector, target outcome, data sources).
- Sector data pack and benchmark library.
- Approved proposal language for this customer.

## Outputs
- Day 1: Source Passport (data sources catalogued, access verified).
- Day 2: DQ Score (data quality assessment, gaps flagged).
- Day 3: Account Scoring (target accounts ranked).
- Day 4: Draft Pack (first draft of Revenue Sprint deliverable).
- Day 5: Governance Review (claims checked, evidence linked, doctrine compliance).
- Day 6: Proof Pack Assembly (final deliverable, attribution, evidence).
- Day 7: Handover + Retainer eligibility check.

## Rules
- No claim ships without a source.
- No deliverable ships without QA checklist signed off.
- No customer-facing artifact leaves Dealix without founder approval at the Day 5 checkpoint.
- Sprint must hit Day 7 handover within 9 calendar days from payment, or the customer is offered a partial refund and a root-cause analysis.
- Every Sprint produces one Capital Asset (reusable data, prompt, or playbook) added to the asset registry.

## Metrics
- Sprints delivered per month.
- On-time delivery rate (target: 95%).
- Customer satisfaction signal (good / mixed / bad).
- Sprint → Data Pack conversion rate.
- Sprint → Managed Ops conversion rate.

## Evidence
- Proof Pack file in `clients/<client>_private/proof_pack.md` (private ops).
- Capital Asset entry in `assets/registry.csv` (private ops).
- Customer reply confirming receipt.
- Approval log entry for Day 5 governance review.

## The Seven Days

### Day 1 — Source Passport
- Confirm intake.
- Catalogue every data source available.
- Verify access (read-only credentials, exports, etc.).
- Write the Source Passport doc.
- Output: `sources_passport.md`.

### Day 2 — DQ Score
- Score every source on completeness, recency, accuracy, fitness for purpose.
- Flag gaps and propose substitutes.
- Output: `dq_score.md`.

### Day 3 — Account Scoring
- Apply the Dealix scoring model to the customer's account list.
- Rank accounts by fit, intent, and reachability.
- Output: `account_scoring.csv`.

### Day 4 — Draft Pack
- Compose the first draft deliverable per the offer template.
- Run AI generation under doctrine constraints.
- Output: `draft_pack.md`.

### Day 5 — Governance Review (founder checkpoint)
- Every claim linked to a source.
- Every recommendation linked to evidence.
- No language outside doctrine.
- Output: founder approval logged in `trust/approval_log.csv`.

### Day 6 — Proof Pack Assembly
- Final deliverable assembled with cover, summary, evidence, attribution.
- Capital Asset registered.
- Output: `proof_pack.md` in client folder + asset entry.

### Day 7 — Handover + Retainer Eligibility
- Handover meeting scheduled.
- Deliverable sent.
- Retainer eligibility evaluated against the offer ladder rules.
- Output: handover log + retainer decision.

## Last Reviewed
2026-05-23
