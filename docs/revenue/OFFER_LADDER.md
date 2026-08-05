# Revenue OS — Offer Ladder

Dealix sells five things, in this exact order, on this exact ladder.
Every customer enters at the lowest viable rung and is moved up only
when evidence justifies it. This is the only ladder; we do not sell
"custom" outside it.

## Purpose
Define the five offers, their price, scope, time-to-deliver, and
promotion rules so the founder can quote any opportunity in under
60 seconds and so the pipeline tracker has unambiguous stages.

## Owner
Sami (Founder).

## Review Cadence
Monthly. Reviewed in the first Weekly CEO Review of each month.

## Inputs
- Pipeline conversion data from the last 30 days.
- Delivery time-to-ship data from the last 30 days.
- Cash collected per offer.
- Customer feedback per offer.
- Capacity available this month.

## Outputs
- Offer scope changes (rare).
- Price changes (rare; documented in decision log).
- New offer experiments (queued as "Signal Sample +" or similar,
  never promoted to the ladder until 3 paid runs).

## Rules
- No offer outside the ladder. Custom requests get scoped onto the
  nearest rung or refused.
- No offer below `Signal Sample` is paid — it is the entry rung.
- A customer moves up the ladder only after the prior rung is
  **delivered and signed off**, not just paid.
- A customer can pause on a rung; the ladder is not a forced upgrade.
- Pricing in SAR, ex-VAT.

## Metrics
- Offer mix (% revenue per rung).
- Promotion rate (% of customers moving up the ladder).
- Refund rate per rung (target: 0).
- Time-to-deliver per rung vs. target.

## Evidence
- `pipeline/pipeline_tracker.csv` (private) — every row tagged with rung.
- `revenue/cash_collected.csv` (private) — every payment tagged with rung.
- `clients/<client>/proposal.md` (private) — proposal references rung.

## Last Reviewed
2026-05-23

---

## The Ladder

### Rung 1 — Signal Sample
- **Price:** Free (entry only).
- **Scope:** One narrow market signal, packaged as a 1–2 page artifact.
- **Time:** 24–48 hours.
- **Promotion criteria:** Customer responds with a question or asks
  for more depth.
- **Verifier:** A signal sample is "shipped" only when the customer
  acknowledges receipt and engages.

### Rung 2 — Revenue Sprint
- **Price:** 499 SAR.
- **Scope:** A focused, time-boxed diagnostic on one revenue
  bottleneck the customer named.
- **Time:** 7 days.
- **Promotion criteria:** Customer signs off the sprint report and
  asks "what's next".
- **Verifier:** Payment received and report delivered with QA sign-off.

### Rung 3 — Managed Pilot
- **Price:** 1,500 SAR (one-time data pack) or 2,999 SAR (managed,
  one cycle).
- **Scope:** A scoped pilot of one Dealix capability (a sector data
  pack, a managed signal pipeline, or a managed outbound test).
- **Time:** 14–21 days.
- **Promotion criteria:** Customer wants the cycle to repeat monthly.
- **Verifier:** Pilot deliverable accepted in writing; renewal
  discussion scheduled.

### Rung 4 — Revenue Desk
- **Price:** 2,999–4,999 SAR / month.
- **Scope:** Managed ongoing revenue desk — signals + outreach + QA
  loop on retainer. Approval-gated by founder.
- **Time:** Monthly cycle.
- **Promotion criteria:** Customer asks for deeper system integration
  or a custom build.
- **Verifier:** Two consecutive monthly invoices paid; documented
  customer outcome each month.

### Rung 5 — Dealix OS
- **Price:** 5,000–25,000 SAR (custom AI / integration engagement).
- **Scope:** Custom AI build, integration, or sector OS deployment.
  Founder-led design; AI-prepared artifacts; explicit approval matrix
  for every external action.
- **Time:** 30–90 days.
- **Promotion criteria:** N/A — this is the top of the ladder. After
  this, conversation shifts to renewal/expansion.
- **Verifier:** Statement of work signed, milestones logged, final
  acceptance signed.

---

## Failure Modes To Watch
- Selling Rung 5 to a Rung 2 customer → almost always ends in refund.
- Skipping Rung 1 because "they're warm" → loses qualification signal.
- Pricing a custom that should be Rung 4 → margin destroyed.
- Multiple customers stuck on Rung 1 with no promotion → either the
  sample is wrong or the next rung is too expensive.
