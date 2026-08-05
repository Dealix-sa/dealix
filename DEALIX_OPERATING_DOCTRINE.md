# Dealix Operating Doctrine

The Dealix Company OS runs on five interlocking loops. Each loop has a
clear input, a clear output, an owner, and a verifier. The loops
together describe how Dealix turns signals into revenue, delivery into
trust, and trust into compounding learning.

The doctrine is short on purpose: every operator should be able to
recite the loops from memory.

## Purpose
Define the five operating loops of Dealix and the AI / Founder
contract that runs them. Every other operating document in the
Company OS instantiates or supports one of these loops.

## Owner
Sami (Founder).

## Review Cadence
Quarterly. Re-read in the first Weekly CEO Review of each quarter
and updated only when a loop has structurally changed.

## Inputs
- Operating reality of the last quarter (what loops produced
  evidence and what loops went silent).
- Customer evidence: payments, deliveries, signed approvals, quotes.
- Incidents that reshaped the AI / Founder contract.

## Outputs
- The five-loop map below.
- The AI / Founder contract.
- The list of non-negotiables binding every loop.
- The composition diagram showing how loops chain together.

## Rules
- The doctrine is descriptive of what the Company OS does, not
  aspirational of what it might do — if a loop is broken in
  practice, that fact is captured here.
- Changes to the doctrine require A3 approval
  (`docs/trust/APPROVAL_MATRIX.md`).
- The doctrine names exactly five loops; adding a sixth requires a
  structural decision and a rewrite, not an addendum.

## Metrics
- Number of loops with a green verifier (target: 5/5).
- Number of weeks the full chain produced evidence end to end
  (target: every week).
- Number of doctrine changes per year (target: low; doctrine should
  be stable).

## Evidence
- `scripts/verify_company_os_deep.py` exercises this doctrine on
  every CI run.
- Each loop's section below names its operating documents and the
  verifier pointers that exercise them.

## Last Reviewed
2026-05-23

---

## The Five Loops

### Revenue Loop
Signal → Outreach → Reply → Proposal → Paid.

- AI prepares the signal sample, the outreach draft, and the proposal.
- Founder approves the message and the price.
- Owner: Founder.
- Cadence: Daily.
- Evidence: `pipeline/pipeline_tracker.csv`, `revenue/cash_collected.csv`.

### Delivery Loop
Paid → Kickoff → Discovery → Draft → QA → Delivered → Retainer.

- AI prepares discovery questions, draft artifacts, QA checklists.
- Founder approves every customer-facing output.
- Owner: Founder.
- Cadence: Per-engagement, reviewed weekly.
- Evidence: `docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md`,
  `docs/delivery/revenue_sprint/QA_CHECKLIST.md`.

### Trust Loop
Action → Approval gate → Logged decision → Audit trail.

- AI prepares the action with a risk classification.
- Founder approves at the matching approval level.
- Owner: Founder.
- Cadence: Continuous.
- Evidence: `docs/trust/APPROVAL_MATRIX.md`,
  `docs/trust/AUTONOMY_POLICY.md`, `trust/approval_log.csv`.

### Learning Loop
Weekly review → Worked / Failed / Bottleneck → One decision → Change.

- AI prepares the weekly intelligence pack from the week's logs.
- Founder approves the one change for the next week.
- Owner: Founder.
- Cadence: Weekly.
- Evidence: `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`,
  `learning/experiment_log.md`.

### CEO Loop
Daily brief → Decisions made → Weekly review → Strategic update.

- AI prepares the daily command brief and weekly CEO review.
- Founder makes the strategic calls.
- Owner: Founder.
- Cadence: Daily brief, weekly review.
- Evidence: `docs/founder/DAILY_COMMAND_BRIEF.md`,
  `docs/founder/WEEKLY_CEO_REVIEW.md`.

---

## The AI / Founder Contract

The doctrine works because the boundary is fixed and visible:

- **AI prepares** every artifact: signals, drafts, proposals, QA lists,
  reviews, briefs, dashboards.
- **Founder approves** every external action, every paid offer, every
  customer deliverable, every trust-significant decision.

This contract is enforced by `docs/trust/AUTONOMY_POLICY.md` (what AI
may do alone vs. with approval) and `docs/trust/APPROVAL_MATRIX.md`
(who signs off at which level).

---

## Non-Negotiables

1. No external action ships without founder approval at the matching
   approval level.
2. No customer-facing deliverable ships without QA + founder sign-off.
3. No claim ships without evidence: a payment, a delivery, a customer
   quote, a passing test, or a logged decision.
4. No customer PII or private pipeline data in the public repo.
5. Every loop has a verifier and the verifier must be green before a
   merge to `main`.

---

## How the loops compose

```
  Signal ──► Revenue Loop ──► Paid
                                │
                                ▼
                          Delivery Loop ──► Delivered
                                │
                                ▼
                            Trust Loop ──► Logged
                                │
                                ▼
                          Learning Loop ──► One Change
                                │
                                ▼
                             CEO Loop ──► Next Week
```

Revenue produces customers. Delivery produces trust. Trust produces
referrals and retainers. Learning produces leverage. CEO closes the
week with one decision that compounds the next week.

That is the doctrine. Everything else is implementation.
