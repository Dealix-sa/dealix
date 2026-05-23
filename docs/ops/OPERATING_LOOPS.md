# Operating Loops

The Operating Loops document is the wiring diagram for the Dealix
Company OS. It restates the five loops from `DEALIX_OPERATING_DOCTRINE.md`
in operational terms — owner, cadence, inputs, outputs, verifier,
and failure modes — so any operator can see how a signal becomes
revenue, how revenue becomes trust, and how trust becomes leverage.

## Purpose
Turn doctrine into wiring. Make the five loops legible and
testable so the Daily Command Brief, the Weekly Intelligence
Review, and the Scorecard all reference the same loop names and
the same verifier scripts.

## Owner
Sami (Founder).

## Review Cadence
Quarterly. Re-read inside the first Weekly CEO Review of each
quarter and adjusted only if a loop has structurally changed.

## Inputs
- The current doctrine (`DEALIX_OPERATING_DOCTRINE.md`).
- The current offer ladder (`docs/revenue/OFFER_LADDER.md`).
- The pipeline stages (`docs/revenue/PIPELINE_STAGES.md`).
- The autonomy policy and approval matrix (`docs/trust/`).
- Last quarter's weekly intelligence reviews.

## Outputs
- A single canonical map of the five loops.
- A verifier reference for each loop.
- A failure-mode catalogue per loop.

## Rules
- Each loop has exactly one owner.
- Each loop has exactly one cadence.
- Each loop has a verifier — if it doesn't, the loop is theatrical.
- Loops compose in the documented order (Revenue → Delivery → Trust
  → Learning → CEO).
- Cross-loop side effects are explicit (e.g. Trust incidents feed
  the Learning loop).

## Metrics
- Number of loops with a green verifier (target: 5/5).
- Number of weeks the full chain produced evidence end to end
  (target: every week).
- Lead-time from signal → paid (Revenue + Delivery composed).
- Lead-time from incident → policy change (Trust + Learning composed).

## Evidence
- `scripts/verify_company_os_deep.py` — verifies all five loops
  exist and are populated.
- Each loop's evidence pointer below.

## Last Reviewed
2026-05-23

---

## The Five Loops, Wired

### Revenue Loop
- **Owner:** Sami.
- **Cadence:** Daily.
- **Inputs:** Market signals, warm contacts, inbound replies, last
  week's pipeline state.
- **Outputs:** New pipeline entries, sent outreach, sent proposals,
  collected cash.
- **Verifier:** `verify_company_os_deep.py` checks
  `docs/revenue/OFFER_LADDER.md` and `docs/revenue/PIPELINE_STAGES.md`
  contain the required structure.
- **Failure mode:** Pipeline grows but cash does not → proposal or
  price is wrong. Cash grows but pipeline does not → no top-of-funnel.

### Delivery Loop
- **Owner:** Sami.
- **Cadence:** Per-engagement; reviewed weekly.
- **Inputs:** A paid engagement; discovery notes; customer artifacts.
- **Outputs:** Shipped, signed-off deliverables; Proof Pack entries;
  queued Rung 3 proposals.
- **Verifier:** `verify_company_os_deep.py` checks the Revenue Sprint
  playbook and QA checklist exist and reference the seven-day
  sequence.
- **Failure mode:** On-time-delivery drops → playbook discipline; QA
  pass-rate drops → quality bar slipping; refunds → P0.

### Trust Loop
- **Owner:** Sami.
- **Cadence:** Continuous.
- **Inputs:** Proposed actions from AI / operators; risk
  classification; customer signals.
- **Outputs:** Logged approvals; refusals; incident records;
  promoted / demoted autonomy levels.
- **Verifier:** `verify_company_os_deep.py` checks the Approval
  Matrix lists A0–A3 + Never, and the Autonomy Policy lists L0–L4.
- **Failure mode:** Approvals granted by emoji without a log →
  reset; Never actions attempted → P0; autonomy creep without
  evidence → demote on schedule.

### Learning Loop
- **Owner:** Sami.
- **Cadence:** Weekly.
- **Inputs:** The week's logs from Revenue, Delivery, Trust loops;
  customer feedback; public content engagement.
- **Outputs:** Completed Weekly Intelligence Review; one committed
  change for the next week; scorecard delta.
- **Verifier:** `verify_company_os_deep.py` checks the Weekly
  Intelligence Review template contains all five required questions.
- **Failure mode:** Same bottleneck three weeks running → promote
  to A3 structural decision; "One Change" not landing month over
  month → review is theatrical, not operational.

### CEO Loop
- **Owner:** Sami.
- **Cadence:** Daily brief + weekly review.
- **Inputs:** Daily Command Briefs; Weekly Intelligence Review;
  the four other loops' outputs.
- **Outputs:** Decisions made (logged); committed "One Change";
  scorecard update; structural changes when warranted.
- **Verifier:** `verify_company_os_deep.py` checks
  `docs/founder/DAILY_COMMAND_BRIEF.md` contains Money / Sales /
  Delivery / Trust / Decisions Required sections.
- **Failure mode:** Daily brief unread → upstream loops drift
  unnoticed; weekly review skipped → learning compounds in the
  wrong direction.

---

## Loop Composition

```
[Revenue Loop]         signal → outreach → reply → proposal → paid
       │
       ▼
[Delivery Loop]        paid → kickoff → discovery → draft → QA → delivered → retainer
       │
       ▼
[Trust Loop]           every action → approval gate → logged decision → audit trail
       │
       ▼
[Learning Loop]        weekly review → what worked/failed/bottleneck → One Change
       │
       ▼
[CEO Loop]             daily brief → decisions made → weekly review → strategic update
```

The chain produces evidence at every junction: a payment, a
deliverable, an approval, a review, a scorecard delta. If any
junction goes silent for a full week, the next Weekly CEO Review
must explain why.

---

## Failure Modes Across Loops
- A loop with no evidence for the week is broken, not "quiet".
- A loop where the verifier is green but no external artifact exists
  for a month is internal-only — it needs to ship.
- A loop downstream of a broken upstream loop will look healthy for
  a while, then collapse — always diagnose upstream first.
