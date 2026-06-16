# Dealix Operating Loops

The five loops the company actually runs on. Anchored to the doctrine, read every week.

## Purpose
Describe the five operating loops so any operator (human or agent) can pick up where the previous one left off.

## Owner
Sami (Founder).

## Review Cadence
Weekly during the CEO review.

## Inputs
- The doctrine (`DEALIX_OPERATING_DOCTRINE.md`).
- The scorecard (`DEALIX_COMPANY_OS_SCORECARD.md`).
- Daily briefs, weekly review, approval log.

## Outputs
- Updated loop status (running, paused, broken).
- Adjustments to cadence or owners.
- Triggers to escalate to the doctrine if a loop is structurally broken.

## Rules
- Every loop must have an owner.
- Every loop must produce evidence per cycle.
- A broken loop blocks the scorecard from going green.

---

## The Five Loops

### Revenue Loop
- Cadence: Daily.
- Owner: Sales OS.
- Cycle: Surface accounts → score → draft outreach → founder approves → send → log → reply → propose → paid.
- Evidence: pipeline tracker movements per day.

### Delivery Loop
- Cadence: Per customer + weekly review.
- Owner: Delivery OS.
- Cycle: Paid → kickoff → 7-day sprint → proof pack → retainer offer.
- Evidence: client folder per customer in private ops.

### Trust Loop
- Cadence: Daily.
- Owner: Trust OS.
- Cycle: AI proposes action → autonomy level checked → approval matrix applied → log written → audit on weekly basis.
- Evidence: `dealix-ops-private/trust/approval_log.csv`.

### Learning Loop
- Cadence: Weekly.
- Owner: Learning OS.
- Cycle: What happened → what worked → what failed → what bottleneck → what will change.
- Evidence: `weekly_reviews/` and `learning/` in private ops.

### CEO Loop
- Cadence: Daily + weekly.
- Owner: Founder OS.
- Cycle: Daily command brief → make three decisions → weekly CEO review → update scorecard.
- Evidence: signed daily briefs and weekly reviews.

---

## Status Table (Updated Weekly)

| Loop | Status | Last Run | Next Action |
|---|---|---|---|
| Revenue Loop | Starting | 2026-05-23 | Load 25 leads |
| Delivery Loop | Starting | 2026-05-23 | Prepare 3 sample packs |
| Trust Loop | Running | 2026-05-23 | Log every approval |
| Learning Loop | Starting | 2026-05-23 | Write first review |
| CEO Loop | Running | 2026-05-23 | Sign brief daily |

## Metrics
- Number of loops with status `Running` this week.
- Number of consecutive days each loop produced evidence.
- Number of loop breakages this quarter.

## Evidence
- This file's status table, updated weekly.
- Private ops repo containing each loop's outputs.
- Scorecard reflecting per-loop scores.

## Last Reviewed
2026-05-23
