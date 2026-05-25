# مركز قيادة الرئيس التنفيذي — CEO Command Center

> The single page the founder opens every morning. One screen, six questions, one focus.

## Purpose
Force a fixed daily entry point. The founder does not check email, Slack, or LinkedIn before answering the six questions on this page. Everything else is downstream.

## Owner
Founder/CEO.

## Inputs
- `DAILY_COMMAND_BRIEF.md` (auto-filled by the morning brief generator)
- Yesterday's `WEEKLY_CEO_REVIEW.md` state
- Layer status from `dealix-ops-private/state/layers.json`
- Cash position from `docs/finance/CASH_CONTROL.md`

## Outputs
- The day's "one focus" written to `dealix-ops-private/daily/YYYY-MM-DD.md`
- Today's kill/defer decisions appended to `KILL_LIST.md`
- One decision logged to `docs/founder/decisions/`

## Rules
1. Open this page before any inbox. No exceptions.
2. Answer all six questions in writing — not in your head.
3. Pick exactly one focus for the day. Not two. Not three.
4. If cash runway < 90 days, the focus must be revenue-generating.
5. If any layer is Red, the focus must be that layer until it is Amber.
6. End the day by marking the focus Done / Moved / Killed. No silent drops.

## Metrics
- Days the six questions are answered: target 6 of 7 per week.
- Focus completion rate: ≥ 70% per month.
- Median time from "open" to "focus written": ≤ 15 minutes.

## Cadence
Daily, before 9:00 AM Riyadh.

## Evidence
`dealix-ops-private/daily/YYYY-MM-DD.md` — one file per day, append-only.

## Verifier
`make ceo-daily-verify` — fails if today's file is missing or has empty focus field.

## Runtime Command
`make ceo-daily`

---

## The Six Daily Questions

1. **Cash** — What is cash today? What is runway in days? (cite `CASH_CONTROL.md`)
2. **Revenue** — What moved in the pipeline yesterday? What needs a reply today? (cite `REVENUE_COMMAND_CENTER.md`)
3. **Delivery** — Is any active sprint behind? What is the one blocker? (cite sprint board)
4. **Trust** — Any open complaint, refund, or governance flag?
5. **Learning** — What did we learn yesterday that changes a doc? (1 line max)
6. **Focus** — What is the single thing that, if done today, makes the week count?

## The Focus Rule
One focus. Written. Tied to a layer. Tied to a KPI. Closed by end of day with status.

Example (acceptable):
> Focus: Send the revised proposal to Customer-A2. Layer: Revenue. KPI: proposal-to-payment rate. Close by 5pm.

Example (rejected):
> Focus: Work on growth. — Too vague. Reject.

## What does NOT belong here
- Email triage.
- Slack catch-up.
- Reading reports.
- "Thinking time" without a written output.

## Escalation thresholds
| Signal | Action |
|---|---|
| Runway < 90 days | Focus must be revenue. Brief board contact. |
| Runway < 60 days | Trigger `CASH_CONTROL.md` emergency protocol. |
| 2 consecutive missed daily briefs | Founder Leverage Index dropped — review. |
| Any A3 decision pending | Block all other focus until Go/No-Go gate run. |

## القواعد العربية
1. افتح هذه الصفحة قبل أي بريد أو رسالة.
2. اكتب الأجوبة الستة — لا تكتفِ بالتفكير.
3. اختر تركيزًا واحدًا. واحد فقط.
4. إذا كان المدرج النقدي أقل من 90 يومًا، يجب أن يكون التركيز على الإيراد.
5. أغلق اليوم بحالة واضحة: تم / مؤجل / مُلغى.

## Cross-links
- `CEO_OPERATING_MODEL.md`
- `DAILY_COMMAND_BRIEF.md`
- `KILL_LIST.md`
- `docs/finance/CASH_CONTROL.md`
- `docs/revenue/REVENUE_COMMAND_CENTER.md`
