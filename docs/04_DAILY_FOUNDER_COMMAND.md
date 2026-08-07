# 04 — Daily Founder Command

> **Status:** The 15-minute daily routine.
> **Companion:** `02_FIRST_7_DAYS_EXECUTION.md` + `03_30_60_90_DAY_PLAN.md`.
> **Tool:** `scripts/founder_daily_command_dry_run.py` + `templates/launch/founder_daily_command.example.json`.

## The 15-minute morning routine

```
[0:00] Open `scripts/founder_daily_command_dry_run.py` output.
[0:02] Read "top 10 targets" + "top 5 follow-ups" + "drafts waiting".
[0:05] Open `templates/launch/approval_queue.example.json` → review pending drafts.
[0:08] Approve / reject 1–5 drafts.
[0:10] Send 1–5 messages (in your own tool, manually).
[0:12] Check "stuck deals" + "hot opportunities".
[0:14] Note "one thing to stop" + "one thing to double down".
[0:15] Done.
```

## What the daily command produces (12 lines)

```
DEALIX_FOUNDER_DAILY_COMMAND [date]

1. أهم قرار اليوم: [one line]
2. cash action today: [one line]
3. top 10 targets: [account_id, icp_score]
4. top 5 follow-ups: [account_id, last_action, next_action]
5. drafts waiting approval: [count]
6. meetings to book: [count]
7. deals stuck (>3 days no movement): [count]
8. hot opportunities: [count]
9. proposals to prepare: [count]
10. proof gaps: [count]
11. content to publish: [count]
12. one thing to stop: [one line]
13. one thing to double down: [one line]
14. next 24h plan: [3 bullets]
```

## How to fill it (from your data)

The script `scripts/founder_daily_command_dry_run.py` reads:

- `data/launch/targets/*.json` → for the top 10.
- `data/launch/drafts/*.json` → for the approval queue.
- `data/launch/proposals/*.json` → for the deals.
- `data/launch/case_studies/*.json` → for the proof gaps.
- `data/launch/content/*.json` → for the content queue.
- `data/launch/pipeline/*.json` → for the stuck deals.

It then prints the 14 lines. You review, override, and act.

## The 5 daily decisions

1. **What to send today.** (Approval queue review.)
2. **What to follow up on.** (Top 5 from the script.)
3. **What to stop.** (One thing that is not working.)
4. **What to double down.** (One thing that is working.)
5. **What to write today.** (Content, case study, or proof pack.)

## The 5 weekly decisions (Sunday)

1. **What vertical to double down on.** (Re-score.)
2. **What offer to lead with.** (Re-score.)
3. **What content pillar to focus on.** (Re-pick.)
4. **What partner to engage.** (Re-pick.)
5. **What to retire.** (Drop the things that did not work.)

## The 5 monthly decisions (first Monday)

1. **What to add to the offer ladder.** (After 5 deals in a vertical, recalibrate.)
2. **What to drop from the offer ladder.**
3. **What tooling to invest in.** (Bundle vs repo.)
4. **What to delegate to a setter / VA.**
5. **What to escalate to a board / advisor.**

## The 5 things to ignore daily

1. **Open rates.** Wait until you have 30+ sends.
2. **Industry news.** It does not move the needle day-to-day.
3. **Other founders' posts.** They are noise.
4. **Tool announcements.** Stay with what works.
5. **Long-term plans.** Daily = today.

## The 5 things to NOT skip

1. **The morning routine.** 15 min, every day.
2. **The approval queue review.** Even if empty.
3. **The end-of-day log.** What you did, what you learned.
4. **The weekly review.** Sunday, 60 min.
5. **The monthly re-score.** First Monday, 180 min.

## The dry-run script

```bash
python scripts/founder_daily_command_dry_run.py
```

The script reads the templates + the example JSONs and prints the 14 lines. It does not make any network call. It does not write to the repo. It is the daily command, dry-run.

To make it real, fill in your own data in `data/launch/` and re-run.

## The output format (one example)

```
DEALIX_FOUNDER_DAILY_COMMAND 2026-06-13

1. أهم قرار اليوم: Approve the 2 pending drafts and send by 10am.
2. cash action today: 1 discovery call at 14:00 (Agency X).
3. top 10 targets: agency_x_riyadh (86), agency_y_jeddah (84), ...
4. top 5 follow-ups: agency_x (3 days, send follow-up 1).
5. drafts waiting approval: 2.
6. meetings to book: 1.
7. deals stuck (>3 days no movement): 0.
8. hot opportunities: 1 (agency_x_riyadh replied positively).
9. proposals to prepare: 1.
10. proof gaps: 1 (no case study yet).
11. content to publish: 1 LinkedIn post.
12. one thing to stop: rewriting the discovery call script.
13. one thing to double down: the audit offer.
14. next 24h plan:
    - 09:00 send 2 approved drafts.
    - 14:00 discovery call (agency_x).
    - 16:00 publish the LinkedIn post.
```

## When to update the routine

- After 30 days: if the routine takes > 20 min, the data is bloated — clean it up.
- After 60 days: if the routine is < 5 min, you are not doing enough — push harder.
- After 90 days: rewrite the routine based on what the founder actually does day-to-day.
