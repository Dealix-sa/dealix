# المراجعة الشهرية للخنادق — Monthly Moat Review

> How to measure moat strength monthly. One score per moat. One action per laggard.

## Purpose
Convert the abstract "moats" concept into a monthly disciplined check. Surface declines before they harden.

## Owner
Founder/CEO.

## Inputs
- Evidence library counts (proof moat).
- Trust dashboard composite (governance moat).
- Sector report contribution counts (sector data moat).
- Published founder pieces (founder voice moat).
- Sprint factory founder-free %.

## Outputs
- `dealix-ops-private/moat/YYYY-MM.md` — month's review.
- Updates to the Board Pack (Section 7).
- Action assigned to the lowest-scoring moat.

## Rules
1. Run during the Monthly Strategy Review.
2. Score each moat using the scale in `MOAT_SYSTEM.md`. No "feel" scoring.
3. Direction is computed against the prior month. Two consecutive declines trigger a bet.
4. The lowest-scoring moat gets one named action with owner and deadline next month.
5. Marketing claims about a moat are blocked if its score < 60.

## Metrics
- Months reviewed: 12 / year.
- Average score across 5 moats: target ≥ 65.
- Months with all 5 moats trending flat or up: tracked.

## Cadence
Monthly.

## Evidence
`dealix-ops-private/moat/`.

## Verifier
`make moat-review-verify` — checks this month's file exists and has all 5 scores.

## Runtime Command
`make moat-review month=YYYY-MM`

---

## Template

```
# Monthly Moat Review — YYYY-MM

## Scores

| Moat | Prior month | This month | Direction | Action owner | Action deadline |
|---|---|---|---|---|---|
| Proof | NN | NN | ↑↓→ | | |
| Governance | NN | NN | ↑↓→ | | |
| Sector data | NN | NN | ↑↓→ | | |
| Founder voice | NN | NN | ↑↓→ | | |
| Sprint factory | NN | NN | ↑↓→ | | |

Average: NN
Moats ≥ 60: N of 5

## Evidence per moat
- Proof: <count of shareable artifacts> — list new this month
- Governance: dashboard score, flags closed
- Sector data: sectors with ≥ 5 PSDE
- Founder voice: pieces published this month with citations
- Sprint factory: % founder-free sprints in last 90 days

## Lowest moat: <name>, score NN
Why: <one paragraph>
Action: <one sentence>
Owner: <name>
Deadline: <YYYY-MM-DD>

## Declines (any moat scoring lower than prior month)
- <moat>: <reason> — bet candidate? yes/no

## Marketing-claim eligibility
- Proof claim allowed? (score ≥ 60) yes/no
- Sector-data claim allowed? yes/no
- Sprint-factory claim allowed? yes/no

## Notes
<short paragraph on cross-moat patterns>
```

## What good looks like
- All 5 moats ≥ 60 with at least 2 trending up.
- No moat has declined two months in a row.
- Each moat had at least one evidence artifact added this month.

## What bad looks like
- A moat scoring < 40 for two months with no action started.
- Marketing using a moat claim whose score is < 60.
- Founder is the named owner of all 5 moats with no delegation in sight after 12 months.

## How this feeds Strategy
- Repeated decline in a moat → candidate bet next month.
- All moats green for 2 quarters → consider raising thresholds (the bar moves).

## القواعد العربية
1. تُجرى ضمن المراجعة الاستراتيجية الشهرية.
2. الدرجات بالمقاييس المحددة في MOAT_SYSTEM، لا بالحس.
3. أدنى خندق يحصل على إجراء واحد بمالك ومهلة.

## Cross-links
- `MOAT_SYSTEM.md`
- `MONTHLY_STRATEGY_REVIEW.md`
- `STRATEGIC_BETS.md`
- `docs/14_trust_os/TRUST_DASHBOARD.md`
