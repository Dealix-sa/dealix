# المراجعة الأسبوعية للرئيس التنفيذي — Weekly CEO Review

> Sunday close. Pipeline, cash, delivery, trust, learning. One file. One score.

## Purpose
Close every week deliberately. No ambiguity about what happened, what was learned, what changes.

## Owner
Founder/CEO.

## Inputs
- Seven daily briefs from this week.
- This week's Business Audit score (`CEO_BUSINESS_AUDIT.md`).
- Pipeline state.
- Cash position.
- Sprint board state.
- Trust dashboard.

## Outputs
- `dealix-ops-private/weekly/YYYY-WW.md` — full review.
- Updates to: `STRATEGIC_BETS.md`, `KILL_LIST.md`, `CEO_KPI_TREE.md` snapshot.

## Rules
1. Run Sunday between 16:00–20:00 Riyadh. Not Monday.
2. If a week's review is missing, the next week starts in deficit — first action is back-fill.
3. Every section must answer: what changed, why, evidence link, next step.
4. Bets that did not move this week get one "stall token". Three tokens = mandatory kill review.
5. The review never refers to "feel" — only to numeric or artifact evidence.

## Metrics
- Weeks reviewed: 52 / year.
- Mean review length: 600–1200 words.
- Bets resolved (won / killed) per quarter: track and review.

## Cadence
Weekly, Sunday.

## Evidence
`dealix-ops-private/weekly/`.

## Verifier
`make week-close-verify` — checks for the week's file, sections, audit score linkage.

## Runtime Command
`make ceo-week-close`

---

## Template

```
# Weekly Review — YYYY-WW (Week of YYYY-MM-DD → YYYY-MM-DD)

## Audit score
Score: NN / 100
Worst dimension: <name>
Trend (4-week): <direction>

## Cash & Finance
- Cash start: SAR X | Cash end: SAR X | Net: +/- SAR X
- Runway: NN days (vs last week: +/- D)
- Invoices issued: N (SAR X) | paid: N (SAR X)
- Notes:

## Revenue & Pipeline
- New qualified leads: N
- Proposals sent: N | accepted: N | rejected: N
- Stage movements: <from → to, count>
- Retainer attach (post-sprint): N of N
- Average sprint value: SAR X
- Notes:

## Delivery
- Sprints completed: N
- On-time: N / N
- Evidence shipped: N artifacts
- Defects / refunds: N
- One delivery improvement next week:

## Trust & Governance
- Trust artifacts shipped: N
- Open flags closed: N | new: N
- Refunds / complaints: N
- Disclosure coverage: NN%

## Learning
- Docs updated: N
- New patterns observed:
- Kills logged this week:
- Next week's doc target:

## Bets (from STRATEGIC_BETS.md)
| Bet | Status | Stall tokens | Action |
|---|---|---|---|
| ... | active/won/killed | 0/1/2/3 | ... |

## Decisions to make this week
1.
2.
3.

## Next week's one focus
<single sentence>

## Anomalies / surprises
<text>
```

## Discipline rules
- Numbers before narrative.
- Evidence link before claim.
- Decisions written, not implied.
- A kill is a result, not a failure.

## What this is NOT
- Not a marketing update.
- Not a journal.
- Not a place to relitigate decisions already logged.

## القواعد العربية
1. تُجرى الأحد، لا الإثنين.
2. كل بند يُجاب بأرقام ودليل، لا بانطباع.
3. الرهانات التي لا تتحرك ثلاثة أسابيع تدخل مراجعة الإلغاء.

## Cross-links
- `CEO_BUSINESS_AUDIT.md`
- `MONTHLY_STRATEGY_REVIEW.md`
- `KILL_LIST.md`
- `docs/strategy/STRATEGIC_BETS.md`
