# Dealix Company OS Scorecard

The scorecard is the single page that tells the founder whether the
Company OS is running. Each system gets a score (0–100), a status, an
evidence pointer, the verifier that proves it, and the next action.

## Purpose
Give the founder a single-page view of every operating system in the
Company OS, with a score, a status, evidence, and a next action — so
the answer to "is this thing working?" never takes more than 60
seconds to find.

## Owner
Sami (Founder).

## Review Cadence
Weekly. Updated inside every Weekly CEO Review.

## Inputs
- Verifier outputs from `scripts/verify_company_os_deep.py` and
  `scripts/verify_document_quality.py`.
- External evidence from the week: payments, deliveries, customer
  quotes, approvals logged.
- The previous week's scorecard for delta comparison.
- The Weekly Intelligence Review.

## Outputs
- Updated system scores and statuses.
- Updated evidence pointers (always the freshest artifact).
- Updated next actions for the upcoming week.
- Promotion / demotion records when a system crosses a threshold.

## Rules
- A system can only be PASS when an external artifact exists this
  month.
- A system can only be COMPOUNDING when external artifacts exist
  every week for four consecutive weeks.
- A system moving down requires a written reason in the Weekly
  Intelligence Review.
- Scores are evidence-bound: no score increase without a linked
  artifact.
- The scorecard is the only place system-level status is recorded;
  other documents reference it, they don't restate it.

## Metrics
- Number of systems at PASS or COMPOUNDING (target: grows
  monotonically).
- Number of systems unchanged for >4 weeks (target: low; movement
  means learning).
- Time from external artifact → scorecard update (target: same
  week).

## Evidence
- Git history of this file (every weekly update is a commit).
- Archived Weekly Intelligence Reviews in
  `weekly_reviews/YYYY-MM-DD.md` (private).
- Linked evidence per row in the table below.

## Last Reviewed
2026-05-23

---

## Statuses

- **PASS** — system is operating and producing revenue, delivery,
  trust, or learning evidence this week.
- **READY INTERNAL** — system is built and verifier-green, but has not
  yet produced external evidence (e.g. paid customer).
- **FIX** — system is broken, blocked, or missing required content.
- **NOT STARTED** — not yet built.

The scorecard is updated after every weekly review.

---

## Current Snapshot

| System       | Score | Status         | Evidence                                                      | Verification                  | Next Action                              |
|---           |---:   |---             |---                                                            |---                            |---                                       |
| Founder OS   | 70    | READY INTERNAL | docs/founder/DAILY_COMMAND_BRIEF.md + WEEKLY_CEO_REVIEW.md    | verify_company_os_deep.py     | Run daily brief for 5 working days       |
| Strategy OS  | 65    | READY INTERNAL | docs/strategy/* (legacy) + doctrine                           | verify_document_quality.py    | Map legacy strategy docs to standard     |
| Revenue OS   | 60    | FIX            | docs/revenue/OFFER_LADDER.md + PIPELINE_STAGES.md             | verify_company_os_deep.py     | Add 25 leads to private pipeline tracker |
| Delivery OS  | 70    | READY INTERNAL | docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md + QA list   | verify_company_os_deep.py     | Prepare 3 signal samples                 |
| Trust OS     | 80    | READY INTERNAL | docs/trust/APPROVAL_MATRIX.md + AUTONOMY_POLICY.md            | verify_company_os_deep.py     | Log first 10 approvals into trust log    |
| Learning OS  | 55    | FIX            | docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md (template only)   | verify_company_os_deep.py     | Write first weekly intelligence review   |

---

## Score Definitions

- **0–39 NOT STARTED**: documents do not exist or do not meet the
  standard.
- **40–59 FIX**: documents exist, verifiers fail, no external evidence.
- **60–79 READY INTERNAL**: documents exist, verifiers pass, no
  external evidence yet.
- **80–89 PASS**: external evidence (payment, delivery, signed
  approval, weekly review) exists this month.
- **90–100 COMPOUNDING**: external evidence exists every week and the
  loop produces leverage (retainer, referral, repeatable playbook).

---

## Promotion Rules

A system moves from `READY INTERNAL` → `PASS` only when **all** of the
following are true:

1. The verifier for that system is green on `main`.
2. An external artifact exists this month (payment, delivered work,
   approved external message, written weekly review).
3. The evidence is linked in the table above.

A system moves to `COMPOUNDING` only when it produced external
evidence every week for the last four weeks.

---

## Weekly Update Protocol

Every weekly CEO review (see `docs/founder/WEEKLY_CEO_REVIEW.md`)
ends with updating this scorecard:

1. Re-score each system.
2. Update the status.
3. Update the evidence link to the freshest artifact.
4. Update the next action for the upcoming week.
5. Bump `## Last Updated`.

If any system moves backwards (e.g. PASS → FIX), the weekly
intelligence review must explain why.
