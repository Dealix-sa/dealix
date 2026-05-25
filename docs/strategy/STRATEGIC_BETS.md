# الرهانات الاستراتيجية — Strategic Bets

> Active bets with budgets, owners, deadlines, kill criteria. Maximum 5 active.

## Purpose
Treat strategy as a portfolio of dated, budgeted bets. Force a kill before a start.

## Owner
Founder/CEO.

## Inputs
- Strategic thesis (`STRATEGIC_THESIS.md`).
- KPI Tree (`docs/founder/CEO_KPI_TREE.md`).
- Capital allocation (`docs/finance/CAPITAL_ALLOCATION_SYSTEM.md`).
- Decisions log (`docs/founder/decisions/`).

## Outputs
- The table in this file (kept current).
- Per-bet decision file in `docs/founder/decisions/`.
- Per-kill file when a bet ends (`docs/founder/KILL_LIST.md`).

## Rules
1. Maximum 5 active bets at any time. To add a sixth, kill or graduate one.
2. Each bet references: thesis pillar #, KPI tree node, budget (SAR + hours), owner, deadline, success criteria, kill criteria.
3. Each bet has a 90-day review date. Reviews are written, not skipped.
4. A "stall token" is added if a bet shows no measurable movement in a week. 3 tokens = mandatory kill review at next Monthly Strategy Review.
5. Bets are added or killed in Monthly Strategy Review only (emergencies use an A2 Go/No-Go gate).
6. Bets that contradict the thesis are rejected regardless of expected return.

## Metrics
- Active bets count: ≤ 5.
- Bets killed per quarter: ≥ 1.
- Bets graduating to "won" per year: ≥ 2.
- Bets exceeding deadline by > 30 days: target 0.

## Cadence
Reviewed Weekly (stall tokens). Decided Monthly. Rebalanced Quarterly.

## Evidence
This file + per-bet decision files + kill log.

## Verifier
`make bets-verify` — confirms each active bet has all required fields and the count is ≤ 5.

## Runtime Command
`make bet-add slug=<slug>` and `make bet-kill slug=<slug>`.

---

## Active Bets (template — fill as bets are added)

| # | Slug | Thesis pillar | KPI node | Budget SAR | Budget hours | Owner | Started | Deadline | Stall tokens | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <slug> | 1 | REV-PROP-PAY | 0 | 0 | Founder | YYYY-MM-DD | YYYY-MM-DD | 0 | active |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |

## Bet definition

A bet is:
- A focused, time-bound effort that, if it works, materially moves a KPI.
- Resourced from the current month's capital allocation.
- Linked to one thesis pillar; cross-pillar bets are not allowed.

A bet is NOT:
- A vague initiative ("improve content").
- An open-ended project without a deadline.
- A customer engagement (those are sprints, not bets).

## Per-bet record (lives in `docs/founder/decisions/<bet-slug>.md`)

```
# Bet: <slug>
Started: YYYY-MM-DD
Owner: <name>
Deadline: YYYY-MM-DD (90 days max for first review)
Class: A1 / A2 / A3

## Thesis link
Pillar #: <1–5>

## KPI link
Node: <e.g., REV-PROP-PAY>
Expected move: <from NN to NN by deadline>

## Budget
SAR: <amount>
Hours: <founder hours>

## Hypothesis
"If we <action>, then <KPI> will move by <amount> within <time>, because <evidence>."

## Success criteria (measurable, dated)
1.
2.

## Kill criteria (measurable, dated)
1.

## Weekly check-in (appended each Sunday in Weekly Review)
- YYYY-WW: movement | stall token? (Y/N) | note

## 90-day review
[ ] Won — KPI moved as hypothesized
[ ] Continue with change — adjust budget/scope
[ ] Killed — reason logged in KILL_LIST.md
```

## Graduation
A "won" bet exits the list and either:
- Becomes operating cadence (folded into a doc + verifier), or
- Productizes per `OFFER_EVOLUTION_SYSTEM.md`.

Either way, the bet slot opens for a new bet.

## القواعد العربية
1. خمسة رهانات نشطة كحد أقصى.
2. لكل رهان: ركيزة، عقدة مؤشر، ميزانية، مالك، مهلة، معايير نجاح، معايير إلغاء.
3. التوقف بلا حركة قابلة للقياس يجمع "رمز ركود". ثلاثة تستوجب مراجعة إلغاء.

## Cross-links
- `STRATEGIC_THESIS.md`
- `docs/founder/CEO_KPI_TREE.md`
- `docs/founder/KILL_LIST.md`
- `docs/finance/CAPITAL_ALLOCATION_SYSTEM.md`
- `docs/founder/DECISION_QUALITY_SYSTEM.md`
