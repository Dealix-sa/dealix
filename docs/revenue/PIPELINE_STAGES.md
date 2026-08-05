# Revenue OS — Pipeline Stages

Every opportunity in Dealix lives in exactly one of seven stages.
Stages are mutually exclusive, sequential (no skipping), and each
has a clear entry condition, exit condition, and SLA.

## Purpose
Standardize how opportunities move through the pipeline so the
private pipeline tracker has unambiguous values, so the Daily Command
Brief can count accurately, and so the founder can spot stuck
opportunities at a glance.

## Owner
Sami (Founder).

## Review Cadence
Weekly, inside the Weekly CEO Review.

## Inputs
- Lead source (warm intro, referral, inbound, signal-triggered).
- Outreach activity log.
- Reply log.
- Proposal log.
- Payment log.
- Delivery log.
- Retainer log.

## Outputs
- Stage transitions (logged in private `pipeline/pipeline_tracker.csv`).
- Stuck-opportunity flags (>SLA in any stage).
- Conversion ratios per stage (reported weekly).

## Rules
- An opportunity has exactly one current stage.
- Transitions are one-way along the ladder; if an opportunity
  regresses, it is **closed-lost** and a new opportunity is opened.
- Each stage has an SLA; an opportunity past SLA is flagged in the
  Daily Command Brief.
- No "stage = TBD". If unclear, the opportunity is `New`.
- A stage transition without evidence (a message sent, a reply, a
  proposal file, a payment) is invalid.

## Metrics
- Count per stage (snapshot).
- Conversion ratio between adjacent stages (target: improving).
- Average days in stage (target: under SLA).
- Stuck count (over SLA, target: 0).

## Evidence
- `pipeline/pipeline_tracker.csv` (private) — single source of truth.
- `clients/<client>/proposal.md` (private) — proof for `Proposal Sent`.
- `revenue/cash_collected.csv` (private) — proof for `Paid`.
- `delivery/<client>/handoff.md` (private) — proof for `Delivered`.

## Last Reviewed
2026-05-23

---

## The Seven Stages

### 1. New
- **Entry:** Lead added to tracker with company, sector, contact.
- **Exit:** First outbound message sent.
- **SLA:** 2 working days.
- **Evidence required to exit:** Message draft approved and sent.

### 2. Contacted
- **Entry:** First outbound message sent.
- **Exit:** Reply received (positive, negative, or neutral).
- **SLA:** 7 days. After 7 days with no reply → one polite follow-up,
  then close-lost.
- **Evidence required to exit:** Logged reply (screenshot or thread
  link).

### 3. Replied
- **Entry:** Lead replied; conversation is live.
- **Exit:** Proposal sent OR conversation ends (close-lost).
- **SLA:** 5 working days to send proposal once intent is confirmed.
- **Evidence required to exit:** A scoped proposal file referencing
  the offer ladder rung.

### 4. Proposal Sent
- **Entry:** Proposal delivered to the lead.
- **Exit:** Payment received OR rejection logged.
- **SLA:** 10 working days.
- **Evidence required to exit:** Payment receipt OR explicit "no"
  recorded.

### 5. Paid
- **Entry:** Payment received; kickoff scheduled.
- **Exit:** Engagement delivered and signed off.
- **SLA:** Matches the rung's delivery time
  (see `docs/revenue/OFFER_LADDER.md`).
- **Evidence required to exit:** Customer sign-off on delivery (email
  or signed acceptance).

### 6. Delivered
- **Entry:** Customer signed off the engagement.
- **Exit:** Customer agrees to retainer / next rung OR formally
  closes the engagement.
- **SLA:** 14 days post-delivery to convert or close.
- **Evidence required to exit:** Retainer agreement, next-rung
  proposal accepted, or close-out note.

### 7. Retainer
- **Entry:** Recurring agreement in place (monthly invoice or
  multi-month SOW).
- **Exit:** Retainer ends (renewed, paused, or churned).
- **SLA:** Continuous; monthly health check inside the Weekly CEO
  Review.
- **Evidence required to exit:** Renewal signed, pause requested in
  writing, or churn reason recorded.

---

## Stage Transitions Diagram

```
New ──► Contacted ──► Replied ──► Proposal Sent ──► Paid ──► Delivered ──► Retainer
                                                                              │
                                                                              ▼
                                                                        Renewed / Paused / Churned
```

Any opportunity that regresses (e.g. Replied → silent for 14 days) is
**closed-lost**, not moved backwards. Closed-lost is final.

---

## Failure Modes To Watch
- Many opportunities stuck in `Replied` → proposal scoping is broken.
- Many `Proposal Sent` aging past SLA → price or proposal artifact
  is wrong.
- Few opportunities reaching `Retainer` → delivery does not produce
  enough trust to upsell.
- Stage counts not matching tracker → tracker discipline broken;
  treat as P0.
