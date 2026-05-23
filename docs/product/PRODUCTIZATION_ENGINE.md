# Productization Engine

> A workflow becomes a product only after it has earned the right.

## The Four Levels

### Level 0 — Ad hoc
- Done by the founder, by hand, once or twice.
- No template. No checklist.

### Level 1 — Documented (after 3 successes)
- Workflow written down with steps, inputs, outputs.
- Founder can hand the doc to a competent assistant.
- Living document; updated after each subsequent run.

### Level 2 — Templated (after 5 successes)
- Template file in `templates/` with placeholder fields.
- Checklist exists.
- An ICP-fit competent contractor could produce a usable first pass
  from the template in a half-day.

### Level 3 — Automated (after 10 successes)
- The repeatable parts are scripted.
- Human judgement is still required at the named oversight points.
- Cost per run measured; cost cap set.
- Evaluation suite covers the automation.

### Level 4 — SaaS candidate (only after Level 3 + customer pull)
- ≥ 3 customers have asked unprompted for a self-serve version.
- Workflow is stable for ≥ 3 months.
- Workflow has a clear unit pricing model that could survive in SaaS.
- Founder writes a SaaS readiness memo.

A Level-4 candidate still requires a separate Go decision via
`GO_NO_GO_DECISION_SYSTEM.md` before SaaS build begins.

## Promotion Discipline

- A workflow is promoted to Level N only when **all** evidence is
  recorded: dates, customers, outcomes, time-to-deliver.
- Promotion is logged in `dealix-ops-private/product/workflow_promotions.md`.

## Demotion

A workflow is **demoted** when:

- Three consecutive runs at the current level produce poor outcomes.
- The market or customer pattern shifts; the workflow no longer applies.

Demotion is also logged.

## What we will **not** automate

- Anything in the autonomy tier A3 zone (per-send approval required).
- Anything where the cost of a wrong output exceeds the cost of a human
  reviewer.
- Anything where the underlying customer task is unstable.

## Anti-Patterns

- "We automated it after 1 success." → Mock-up, not automation.
- "It feels stable; let us SaaS it." → Without 3 unprompted asks, no.
- "Templates take too long; we will skip to automation." → Skipping
  Level 2 forfeits the leverage that templates give.
