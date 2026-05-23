# Revenue Sprint — Delivery Playbook

This playbook governs delivery of the 499 SAR Revenue Sprint
(Rung 2 of the offer ladder). It is the canonical 7-day sequence,
day by day, with explicit inputs, outputs, and quality gates.

## Purpose
Make Revenue Sprint delivery repeatable, AI-prepared, and founder-
approved end to end — so a paid sprint can be shipped in 7 days
with consistent quality and an artifact strong enough to justify a
promotion to Rung 3.

## Owner
Sami (Founder). AI prepares artifacts; founder approves every
customer-facing output.

## Review Cadence
Weekly during active sprints. Monthly review of the playbook itself
for tuning.

## Inputs
- Signed-off proposal referencing the customer's named bottleneck.
- 499 SAR payment confirmed in `revenue/cash_collected.csv` (private).
- Kickoff call recording / notes.
- Customer-supplied artifacts (data, dashboards, screenshots).
- Sector context from prior signal samples or pilots.

## Outputs
- Day-by-day deliverables (see sequence below).
- Final Sprint Report (PDF / markdown).
- Proof Pack entry suitable for case-study consideration.
- A scoped Rung 3 proposal queued for founder review.

## Rules
- Every customer-facing deliverable passes QA
  (`docs/delivery/revenue_sprint/QA_CHECKLIST.md`) before founder
  sign-off and before customer send.
- No customer artifact ships without founder approval at level A2
  (see `docs/trust/APPROVAL_MATRIX.md`).
- The sprint is 7 calendar days from kickoff, not 7 working days.
- If a day's gate fails, the sprint pauses; it does not silently
  slip.
- No new scope is accepted mid-sprint; in-scope clarifications only.
  Out-of-scope items go into the Rung 3 proposal.

## Metrics
- On-time delivery rate (target: 95%+).
- QA pass rate on first review (target: 80%+).
- Customer sign-off within 48 hours of delivery (target: 90%+).
- Promotion-to-Rung-3 rate (target: 40%+).
- Refund rate (target: 0).

## Evidence
- `clients/<client>/sprint/day_N.md` (private) — daily artifact.
- `clients/<client>/sprint/final_report.md` (private) — final.
- `clients/<client>/qa_checklist_signed.md` (private) — QA evidence.
- `clients/<client>/founder_approval.md` (private) — A2 approval log.

## Last Reviewed
2026-05-23

---

## The 7-Day Sequence

### Day 0 — Pre-kickoff (within 24h of payment)
- AI assembles a Source Passport: every artifact the customer
  provided + every public source we'll use.
- AI drafts kickoff questions tied to the named bottleneck.
- Founder reviews and approves the kickoff agenda.
- **Gate:** kickoff agenda approved.

### Day 1 — Kickoff and Discovery
- 45-minute kickoff call.
- AI captures notes + open questions.
- AI produces a Discovery Brief (1 page) confirming scope and the
  precise question the sprint will answer.
- **Gate:** Discovery Brief signed off by customer (email reply OK).

### Day 2 — Data and Signal Scan
- AI runs the data pull and signal scan against the agreed scope.
- AI produces a Findings Sketch (raw, not customer-facing).
- Founder reviews for surprises and steers analysis priorities.
- **Gate:** Findings Sketch reviewed; analysis priorities set.

### Day 3 — Analysis Pass One
- AI produces the first analysis pass with charts + commentary.
- QA checklist run for clarity, accuracy, evidence links.
- Founder reviews the draft narrative.
- **Gate:** Draft narrative approved or revised.

### Day 4 — Analysis Pass Two and Recommendations
- AI integrates founder feedback.
- AI drafts the recommendations section: what the customer should
  do in the next 30 days, ranked by impact.
- **Gate:** Recommendations approved by founder.

### Day 5 — Sprint Report Assembly
- AI assembles the full Sprint Report: Executive Summary, Findings,
  Evidence, Recommendations, Next Steps.
- Full QA checklist pass.
- Founder approval at level A2.
- **Gate:** Sprint Report approved for customer send.

### Day 6 — Customer Review Session
- 30–45 minute review call with customer.
- AI captures questions, objections, clarifications.
- AI drafts a Rung 3 proposal aligned to the customer's next step.
- **Gate:** Customer questions answered; Rung 3 proposal drafted.

### Day 7 — Final Delivery and Promotion
- Final Sprint Report delivered (PDF + markdown).
- Customer sign-off requested (email confirmation acceptable).
- Rung 3 proposal sent if customer is ready.
- Proof Pack entry queued.
- **Gate:** Sign-off received OR explicit reason logged for delay.

---

## Failure Modes To Watch
- Customer goes silent between Day 1 and Day 3 → escalate same day;
  do not run analysis on a phantom scope.
- QA checklist failing on multiple sprints for the same reason →
  fix the playbook, not the symptom.
- Promotion-to-Rung-3 below 25% → sprint output is not strong enough
  to justify next rung; review the recommendation quality.
- Refunds → P0, full root-cause review at next Weekly CEO Review.
