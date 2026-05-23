# Sales Operating Rhythm

The Sales Operating Rhythm is the daily, weekly, monthly, and quarterly
cadence that runs the Revenue Factory. It is the meeting structure, the
review structure, and the artefact discipline.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why cadence is the OS

Without cadence, the Revenue Factory becomes whatever the loudest
opportunity demands today. Cadence is the rule that says: every
opportunity gets reviewed, every stage gets attention, every SLA gets
honoured, and every reply gets routed.

## 2. Daily rhythm

### 2.1 Founder daily anchor (start of day)

- Read the day's brief from `founder/operating_scorecard.md`.
- Triage approval queues in priority order:
  1. Reply Router escalations (sensitive class).
  2. Proposal Factory drafts at "queued".
  3. Sample Factory drafts at "queued".
  4. Outbound draft queues (LI, EM, CF).
  5. Partner Referral queue.
- Send approved artefacts as a named operator. No bulk send.
- Note any SLA breach or new pattern in `founder/operating_notes.md`.

### 2.2 Distribution Operator (during day)

- New outbound drafts produced.
- Reply Router runs continuously; classified replies surface to the
  routing queue.
- Trust gate enforcement is real-time.
- Daily volume caps respected.

### 2.3 Delivery Copilot (during day)

- Pipeline view updated.
- Sample and proposal queues kept fresh.
- Stage transitions logged.

### 2.4 End of day

- A short "end-of-day" line written to `founder/operating_notes.md`
  capturing the day's wins, blockers, and one decision the founder
  made.

## 3. Weekly rhythm

### 3.1 Monday sales operating meeting (60 minutes)

- Pipeline review: every opportunity at qualified+ stage.
- SLA review: any breaches and the recovery plan.
- Reply quality review: a sample of 20 replies and their routing.
- Brand voice review: any drift over the previous week.
- Decisions: what changes this week.

Output: `sales/weekly_review_{date}.md` with decisions, owners, and
due dates.

### 3.2 Wednesday content + community review (30 minutes)

- Content calendar status.
- Community engagement signals.
- Decisions on what to publish next.

Output: `marketing/weekly_review_{date}.md`.

### 3.3 Friday close (30 minutes)

- What we closed (or didn't), with reasons.
- Next week's top 5 opportunities.
- Operator capacity check.

Output: `sales/weekly_close_{date}.md` with the top 5 named
opportunities and the next step for each.

## 4. Monthly rhythm

- Win/loss analysis: every won and lost deal reviewed, the reason
  recorded in `sales/win_loss_log.md`, and patterns aggregated.
- Channel portfolio review: cap adjustments approved as needed.
- Objection library audit.
- Pipeline stage SLA review.
- Sector ranking re-score where triggered.

Output: `sales/monthly_review_{month}.md`.

## 5. Quarterly rhythm

- Account scoring re-calibration.
- Channel portfolio reset.
- Offer ladder audit.
- Sector ranking quarterly review.
- Operating rhythm self-audit (is the rhythm still right).

Output: `sales/quarterly_review_{quarter}.md`.

## 6. Source of truth

- `sales/pipeline.csv` for opportunities.
- `sales/weekly_review_*` for weekly notes.
- `sales/monthly_review_*` for monthly notes.
- `sales/quarterly_review_*` for quarterly notes.
- `founder/operating_scorecard.md` for daily brief.

## 7. Approval class

A1 for observation and meeting prep. A2 for any drafts produced from
the meeting (decisions that involve external action). A3 not used.

## 8. Trust gate

- Every meeting note that contains buyer-attributable language is
  treated like a draft — guarantee scan, brand voice check.
- Decisions that touch pricing, terms, or contract commitments require
  founder approval and a ledger entry.
- Sensitive escalations override the rhythm; the founder addresses
  them immediately.

## 9. Owners

- Founder: meeting chair; approval authority.
- Delivery Copilot: pipeline view; SLA tracking.
- Distribution Operator: reply quality; channel performance.
- Performance Analyst: scorecard and calibration.
- Trust Guardian: gate enforcement.

## 10. KPI

- Meeting Adherence (target: 100% of weekly meetings held).
- Decision Yield (decisions made per meeting).
- SLA Breach Count (week-over-week).
- Win/Loss Note Completeness.
- Operating Notes Compactness (one page, max).

## 11. Failure mode

- Meeting becomes status reporting, not decision-making. Chair resets
  the agenda; decisions are required output.
- SLA breaches accumulate. Capacity review; cap reductions until
  recovered.
- Brand voice drift across notes. Brand Guardian rewrites; root cause.

## 12. Recovery path

- For meeting drift: re-set agenda; require named decisions and
  due-dated owners.
- For SLA debt: pause new outbound until backlog is drained.
- For voice drift: paused; rewrite session.

## 13. Cadence summary

```
Daily       -> Brief + queue triage + send
Weekly      -> Mon sales / Wed content / Fri close
Monthly     -> Win/loss + channel + objection + sector
Quarterly   -> Scoring + portfolio + offer + rhythm self-audit
```

## 14. Saudi specifics

- Weekly cadence respects the local working week.
- Monthly cycles align with invoice and reporting cycles.
- Quarterly cycles align with sector reporting cycles.

## 15. Non-negotiables

- No cadence drift without an explicit decision.
- No meeting without a decision yield.
- No approval bypassed for the sake of meeting pace.
- A3 not used.

The rhythm is the operating system. Without it, the rest of the
Revenue Factory is just nice documents.
