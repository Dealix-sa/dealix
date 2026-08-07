# 02 — First 7 Days Execution

> **Status:** The day-by-day playbook for week 1.
> **Companion:** `BEST_FIRST_WEDGE_DECISION_AR.md` + `04_DAILY_FOUNDER_COMMAND.md`.
> **Read first:** `README_START_HERE_AR.md`.

## The 7 days in one screen

| Day | Objective | Tasks | Output | Stop condition |
| --- | --- | --- | --- | --- |
| 1 | Decide vertical + offer + first 10 targets | read 3 docs; pick sector; pick offer; list 10 companies from your network | `vertical_choice.md` + `target_account.example.json` × 10 | if you cannot list 10, pivot vertical |
| 2 | Research 10 accounts | 15 min each: LinkedIn, website, Google Maps; fill `target_account.example.json` | 10 filled JSONs + ICP score each | if ICP < 50, drop the account |
| 3 | Write 10 outreach drafts | one email per account; Sequence A for owner, B for sales, C for GM, D for skeptic; run trust preflight on each | 10 drafts in `data/launch/drafts/` | if preflight fails 3+ drafts, rewrite the template |
| 4 | Founder review + send manually | read each draft, approve in `approval_queue.example.json`, send through your normal tool | 10 sends logged in approval queue | if < 5 approved, adjust the drafts |
| 5 | Follow up + book discovery | reply to responses; send follow-up 1 (day 3) to non-responders; book 2–3 discovery calls | 2–3 calls booked in calendar | if 0 calls booked, the message is broken — rewrite |
| 6 | Discovery prep + proposal skeletons | prepare 1-page research per call; build proposal skeleton (no price) | 2–3 proposal skeletons in `data/launch/proposals/` | if you cannot fill the skeleton, the discovery is broken |
| 7 | Founder weekly review + decide | run `make launch-*` (or scripts); review the week; decide: double down or pivot | `WEEKLY_GTM_BOARD_REVIEW_TEMPLATE.md` filled | if no decision, schedule it |

## The 5 daily rituals (run these in addition to the day task)

1. **Morning (15 min):** run the daily founder command (`scripts/founder_daily_command_dry_run.py`).
2. **Mid-day (5 min):** review the approval queue.
3. **End of day (10 min):** log what you did + what you learned.
4. **End of week (60 min):** weekly review.
5. **End of month (180 min):** monthly re-score of vertical + offer + ICP.

## The 5 hard rules for week 1

1. **Do not send more than 10 outreach messages** in week 1. Quality over volume.
2. **Do not pitch in the first message.** The first message is a request, not a pitch.
3. **Do not promise specific outcomes.** Proof metric only.
4. **Do not send WhatsApp to anyone who did not consent.**
5. **Do not skip the preflight.** Even on a "small" draft.

## The 5 day-by-day deliverables

### Day 1 — Decide

- [ ] Read `BEST_FIRST_WEDGE_DECISION_AR.md`.
- [ ] Read `SAUDI_VERTICAL_SELECTION_MATRIX_AR.md`.
- [ ] Pick the vertical (default: agencies). Override with reason.
- [ ] Pick the offer (default: Revenue Leak Audit).
- [ ] List 10 target companies from your network.
- [ ] Save to `data/launch/targets/<id>.json`.

### Day 2 — Research

- [ ] 15 min per account × 10 accounts.
- [ ] Fill `target_account.example.json` for each.
- [ ] Score each with `scripts/icp_score_dry_run.py`.
- [ ] Drop the bottom 5. Keep the top 5.

### Day 3 — Write

- [ ] Pick the sequence per persona (A/B/C/D).
- [ ] Write one draft per account.
- [ ] Run `scripts/trust_preflight_dry_run.py` on each.
- [ ] Reject any FAIL. Rewrite. Re-run.
- [ ] Save drafts to `data/launch/drafts/<id>.json`.

### Day 4 — Send

- [ ] Review each draft.
- [ ] Add to `approval_queue.example.json` with `founder_review_status: approved`.
- [ ] Send manually (in your own email tool, not in the bundle).
- [ ] Log the send in the approval queue.

### Day 5 — Follow up

- [ ] Reply to responses (within 24h).
- [ ] Send follow-up 1 to non-responders (day 3 from initial).
- [ ] Book 2–3 discovery calls in your calendar.
- [ ] Log replies in the approval queue.

### Day 6 — Prep

- [ ] For each booked call, prepare a 1-page research note.
- [ ] Build a proposal skeleton (no price) using `docs/proposal/PROPOSAL_TEMPLATE_AR.md`.
- [ ] Save to `data/launch/proposals/<id>.json`.

### Day 7 — Review

- [ ] Run `scripts/founder_daily_command_dry_run.py`.
- [ ] Open `reports/launch/WEEKLY_GTM_BOARD_REVIEW_TEMPLATE.md`.
- [ ] Fill the review with: what worked, what didn't, what to change.
- [ ] Decide: double down, pivot, or pause.

## The 5 metrics to track

| Metric | Target | If missed |
| --- | --- | --- |
| Outreach sent | 10 | rewrite the message |
| Reply rate | ≥ 20% | rewrite the message |
| Discovery calls booked | 2–3 | the offer is broken |
| Pilot / audit delivered | 1 | the offer is broken |
| Trust preflight rejections | 0 | the templates are broken |

## The 5 ways to fail (and how to detect them early)

| Failure | Day detected | Action |
| --- | --- | --- |
| Wrong vertical | Day 1–2 | pivot before sending |
| Wrong offer | Day 1–2 | pivot before sending |
| Wrong message | Day 4–5 | rewrite based on reply rate |
| Wrong follow-up | Day 5 | rewrite the follow-up |
| Wrong close | Day 6+ | review the discovery |

## The 5 things to ignore in week 1

1. **Volume.** Quality > volume.
2. **Conversion rate optimization.** Wait until you have 30+ sent.
3. **Pricing.** Founder quotes.
4. **Tech stack.** Use what you have.
5. **The full ladder.** Just the first offer.

## The week 1 deliverable

By end of Day 7:

- 10 outreach messages sent.
- 2–3 discovery calls booked.
- 1 audit (or audit-equivalent conversation) in motion.
- 1 weekly review filed.
- 1 decision: double down or pivot.

## When to skip days

Skip a day only if:

- The preflight is blocking legitimate drafts (means: rewrite the templates, not skip the day).
- The founder is on the road (means: catch up the next day, do not skip permanently).
- The vertical is clearly wrong (means: pivot, do not skip).

Never skip a day to "wait for the right moment". The right moment is now.
