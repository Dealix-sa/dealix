# Revenue Sprint Factory

> What the customer **receives** once they pay for a Revenue Sprint.

A Revenue Sprint is a **fixed-scope, 7-day engagement** that produces a
specific, named artefact and a measurable revenue / pipeline outcome.

## Inputs (from sale)

- Signed `client_intake.md` from `docs/offers/revenue_sprint/`.
- Payment confirmation or PO logged in `revenue/revenue_action_log.csv`.
- Founder access to the client's pipeline data (read-only credentials).

## Day-by-day

| Day | Output | File |
|---|---|---|
| 1 | Intake call notes + scope confirmation | `clients/<client>/day1_intake.md` |
| 2 | Data ingest + baseline | `clients/<client>/day2_baseline.md` |
| 3 | First analysis pass | `clients/<client>/day3_analysis.md` |
| 4 | Draft deliverable | `clients/<client>/day4_draft.md` |
| 5 | Internal QA via `qa_checklist.md` | `clients/<client>/day5_qa.md` |
| 6 | Client review + revision | `clients/<client>/day6_revision.md` |
| 7 | Final delivery via `delivery_report_template.md` + handoff | `clients/<client>/delivery_report.md` |

## QA gate (before any deliverable leaves Dealix)

Every item in `docs/offers/revenue_sprint/qa_checklist.md` must be checked.
The verifier `scripts/verify_tier2_delivery.py` enforces this.

## Hand-off

`docs/offers/revenue_sprint/handoff_template.md` is used at end-of-sprint and
includes:

- What was delivered.
- What the client should do next.
- The retainer ask, using `retainer_ask.md`.
- The feedback request, using `feedback_request.md`.

## Operating constraints

1. **Sprint scope is frozen on day 1.** Change requests go into the next sprint.
2. **No work begins before payment / PO / written approval is logged.**
3. **One sprint at a time per founder** — capacity is the limit, not pipeline.
4. **Every artefact is reviewable by another human** — no opaque outputs.

## Related

- `docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md` — public-facing kit description.
- `docs/revenue/REVENUE_COMMAND_CENTER.md` — how a sale becomes a sprint.
- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md` — green-lighting a sprint.
