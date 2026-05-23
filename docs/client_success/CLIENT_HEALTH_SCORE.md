# Client Health Score

> Composite signal of "will this client renew / expand / churn".
> Updated weekly per active client.

## Score (0–100)

| Signal | Weight | Source |
|---|---|---|
| Delivery on-time rate (last 4 weeks) | 20 | `clients/{client}/delivery_*` |
| Client replied to weekly report | 10 | `clients/{client}/reports/` |
| Client used the deliverables (sent drafts, ran samples) | 20 | Client report or attestation |
| Approval queue cleared in < 48 hr | 10 | `trust/approval_log.csv` |
| New opportunities created this month (via our work) | 15 | Client report or pipeline movement |
| Client feedback (latest survey or working session) | 15 | `clients/{client}/feedback.md` |
| Retainer probability self-assessment by founder | 10 | Weekly judgment call |

## Score Thresholds

- **80–100** — Healthy → upsell conversation OK, case study capture OK
- **60–79** — Watch → identify the weak signal, intervene this week
- **40–59** — At risk → founder + (advisor if Custom AI) intervention; structured save plan
- **0–39** — Churning → stop adding scope; have the honest conversation; plan exit

## Score Update Cadence

- Weekly (Sunday during CEO Review)
- Per-client row in `clients/{client}/health.md`
- Aggregate across all active clients in Weekly CEO Review

## Save Plan (when score drops to At Risk)

1. Founder schedules unscheduled 30-min call within 48 hr
2. Single question: "What's not working?"
3. Listen — don't pitch
4. Co-write a 2-week save plan (one specific thing to fix)
5. Re-score in 2 weeks; if no improvement → exit conversation

## Exit Conversation (when client should churn)

When health < 40 for 4 weeks OR clear signal:
1. Don't pretend it's working
2. Propose graceful exit: complete current month + clean handoff
3. Capture learning in `learning/`
4. Refund unearned future months if client requests
5. Maintain relationship — they may come back

## What This Refuses

- Inflating health to feel better about pipeline
- Saving accounts that don't want to be saved
- Hidden health signals (the score is shareable with client on request)
- Replacing the score with vibe ("I feel like they're fine")
