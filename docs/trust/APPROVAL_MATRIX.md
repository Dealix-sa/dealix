# Trust OS — Approval Matrix

The Approval Matrix tells you exactly who must approve what,
in what form, before any action with external consequences happens.
It pairs with the Autonomy Policy: the Autonomy Policy says **what
AI may attempt**; this matrix says **how it gets approved**.

## Purpose
Make approvals fast, unambiguous, and logged. The founder should
never wonder "do I need to approve this?" — the matrix answers
that in one lookup.

## Owner
Sami (Founder).

## Review Cadence
Monthly. Updated immediately whenever an approval-related incident
occurs.

## Inputs
- Action proposed by AI or operator.
- Risk classification of the action (from the Autonomy Policy).
- Customer / external dimension of the action.
- Money dimension of the action.
- Reversibility of the action.

## Outputs
- Approval level required (A0 / A1 / A2 / A3 / Never).
- Logged approval in `trust/approval_log.csv` (private).
- A pointer to the artifact under approval.
- A decision: approved, deferred, rejected.

## Rules
- No external action may execute without an approval at the matching
  level recorded **before** the action.
- A0 actions still get logged (they are not exempt; they are just
  fast).
- A Never action is **Never** — no exception, no escalation overrides
  it.
- Approvals are personal: a logged approval names the approver, time,
  and evidence link.
- A deferred decision stays deferred until the queue is worked; it
  does not silently expire.

## Metrics
- Median time from approval requested → granted (target: under 2h
  for A1, under 24h for A2).
- Number of unlogged external actions (target: 0).
- Number of Never actions attempted (target: 0; any single one is a
  P0 incident).
- Approval backlog depth (target: under 5 items).

## Evidence
- `trust/approval_log.csv` (private) — every approval logged.
- `founder/approvals_waiting.md` (private) — current queue.
- `founder/decision_log.md` (private) — context for non-trivial
  approvals.

## Last Reviewed
2026-05-23

---

## The Approval Levels

### A0 — Auto-logged (no human gate)
- Internal-only, reversible, non-customer-facing actions.
- Examples: a verifier run, a private notes update, a draft saved
  internally, a private dashboard refresh.
- Logged in the approval log but does not block execution.

### A1 — Founder light approval
- External-facing but low blast radius, easily reversible.
- Examples: a single warm DM draft to a known contact, a public
  blog post draft (still queued), a single proposal draft to a
  Rung 1 / Rung 2 customer.
- Founder approval logged before send (text reply, emoji ack
  acceptable if the matrix entry permits).

### A2 — Founder explicit approval
- External-facing, mid-to-high blast radius, or money-touching.
- Examples: pricing change inside a proposal, customer-facing
  deliverable ship, Rung 3+ proposal send, public commitment.
- Founder approval logged with the artifact link and a one-line
  rationale.

### A3 — Founder + Evidence approval
- Highest blast radius: anything that changes the offer ladder,
  the approval matrix itself, the autonomy policy, customer
  contracts, or commits Dealix to public claims.
- Examples: changing a price on the offer ladder, adding a new
  rung, signing a contract, posting a benchmark publicly.
- Founder approval logged with full evidence pack: the proposed
  change, the supporting data, the rollback plan, and the
  acceptance timestamp.

### Never
- Actions that are outright prohibited and have no approval path:
  cold scraping, automated mass outreach without consent, sending
  customer data to unapproved third parties, making guarantees we
  cannot defend, fabricating evidence, bypassing the QA checklist.
- Any attempt is a P0 incident and is reviewed in the next Weekly
  CEO Review regardless of outcome.

---

## Action → Approval Lookup

| Action type                              | Level | Notes                                      |
|---                                       |---    |---                                         |
| Internal verifier run                    | A0    | Logged, not gated.                         |
| Internal note / private dashboard update | A0    | Logged, not gated.                         |
| Warm DM to known contact (draft → send)  | A1    | Text ack OK.                               |
| Public post draft (queued)               | A1    | Send still gated.                          |
| Public post send                         | A2    | Artifact + rationale logged.               |
| Rung 1–2 proposal send                   | A1    | Customer + offer logged.                   |
| Rung 3+ proposal send                    | A2    | Customer + offer + scope logged.           |
| Customer-facing deliverable ship         | A2    | QA checklist + artifact link logged.       |
| Pricing change on a single proposal      | A2    | Rationale logged.                          |
| Offer ladder change                      | A3    | Full evidence pack.                        |
| Approval Matrix change                   | A3    | Full evidence pack + rollback plan.        |
| Autonomy Policy change                   | A3    | Full evidence pack + rollback plan.        |
| Contract signing                         | A3    | Counter-signature logged.                  |
| Cold scrape / mass outreach              | Never | Refuse and report.                         |
| Send customer data outside Dealix scope  | Never | Refuse and report.                         |
| State a guarantee without evidence       | Never | Refuse and report.                         |
| Bypass QA checklist                      | Never | Refuse and report.                         |

---

## Failure Modes To Watch
- A1 approvals being granted by emoji with no record → reset
  discipline; log everything.
- A2 actions slipping through as A1 → audit a random week's
  approval log monthly.
- Never actions attempted (even refused) → P0; full review of
  upstream rules.
