# المراجعة الاستراتيجية الشهرية — Monthly Strategy Review

> End of month. Bets, kills, productization candidates. Strategy adjusts, not vibes.

## Purpose
Run a deliberate strategic reset every month. Decide what continues, what dies, what graduates from project to product.

## Owner
Founder/CEO.

## Inputs
- Four (or five) Weekly CEO Reviews from this month.
- `STRATEGIC_BETS.md` current state.
- `OFFER_EVOLUTION_SYSTEM.md` thresholds and counters.
- `MOAT_SYSTEM.md` and the monthly moat score.
- `CAPITAL_ALLOCATION_SYSTEM.md` last allocation.
- `KILL_LIST.md` this month's adds.

## Outputs
- `dealix-ops-private/monthly/YYYY-MM.md` — review.
- `BOARD_PACK_TEMPLATE.md` produced for this month.
- Decisions logged: bet starts, bet kills, productization graduations, allocation shifts.

## Rules
1. Run on the last working day of the month, before 17:00 Riyadh.
2. Every active bet is graded: continue / continue with change / kill.
3. Every offer is checked against the 3/5/10 evolution rule.
4. Capital allocation is re-set with explicit percentages.
5. No new bet is started in this review without a kill or a graduation pairing it.
6. Each kill has a written reason and a learning extracted.

## Metrics
- Months reviewed: 12 / year.
- Bets killed per quarter: ≥ 1 (forced discipline).
- Productization events per year: ≥ 2.
- Capital allocation drift > 15% triggers re-review.

## Cadence
Monthly, last working day.

## Evidence
`dealix-ops-private/monthly/`, board pack PDF in `dealix-ops-private/board/`.

## Verifier
`make month-close-verify` — checks file exists, bets graded, board pack generated.

## Runtime Command
`make ceo-month-close`

---

## Template

```
# Monthly Strategy Review — YYYY-MM

## Snapshot
- MRR start / end: SAR X → SAR Y
- Cash start / end: SAR X → SAR Y
- Runway start / end: D → D days
- Sprints delivered with evidence: N
- Audit score average (4 weeks): NN

## Bets review
| Bet | Started | Status | Decision | Reason |
|---|---|---|---|---|
| ... | YYYY-MM | active | continue | <evidence> |

Killed this month:
- <bet>: reason: <text>; learning: <one line>

## Offer evolution check
For each offer in OFFER_LADDER.md:
- Successful runs: N
- 3 successes → doc updated? (yes/no)
- 5 successes → template created? (yes/no)
- 10 successes → automation candidate? (yes/no)

## Moat review
Pulled from MOAT_SYSTEM.md monthly score:
| Moat | Last month | This month | Direction |
|---|---|---|---|
| Proof | NN | NN | ↑↓→ |
| Governance | NN | NN | |
| Sector data | NN | NN | |
| Founder voice | NN | NN | |
| Sprint factory | NN | NN | |

## Capital allocation
Reset for next month per CAPITAL_ALLOCATION_SYSTEM.md tiers.

## Productization candidates
- <offer/process>: criteria met / not met
- Decision: graduate / hold / kill

## Strategic risks
- Cash, customer concentration, key person, regulatory, market

## Three decisions for next month
1.
2.
3.

## What is the single hypothesis we are testing next month?
<text>
```

## Anti-patterns this review prevents
- Quietly continuing bets that have stalled.
- Adding new initiatives without killing anything.
- Sliding capital allocation by feel.
- Refusing to productize working offers (founder ego trap).

## القواعد العربية
1. تُجرى في آخر يوم عمل من الشهر.
2. كل رهان نشط يُصنّف: استمرار / تعديل / إلغاء.
3. لا رهان جديد دون إلغاء أو ترقية رهان قديم.

## Cross-links
- `STRATEGIC_BETS.md`
- `MOAT_SYSTEM.md`
- `BOARD_PACK_TEMPLATE.md`
- `OFFER_EVOLUTION_SYSTEM.md`
- `CAPITAL_ALLOCATION_SYSTEM.md`
