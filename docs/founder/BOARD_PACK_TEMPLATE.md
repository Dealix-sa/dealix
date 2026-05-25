# حزمة المجلس الشهرية — Board Pack Template

> Even pre-investor. Discipline first. Investors second.

## Purpose
Produce a monthly board pack regardless of whether a board exists. The discipline of writing it is the value. If/when investors arrive, the cadence is already in place.

## Owner
Founder/CEO.

## Inputs
- `MONTHLY_STRATEGY_REVIEW.md` output for the month.
- KPI Tree snapshot (`CEO_KPI_TREE.md`).
- Cash & runway (`docs/finance/CASH_CONTROL.md`).
- MRR (`docs/finance/MRR_DEFINITION.md`).
- Bets state (`STRATEGIC_BETS.md`).
- Trust dashboard (`docs/14_trust_os/TRUST_DASHBOARD.md`).

## Outputs
- `dealix-ops-private/board/YYYY-MM.md` (markdown).
- Optional PDF export for sharing.

## Rules
1. One pack per month. Same template every time.
2. Numbers cite their source artifact. No "approximately" — round or omit.
3. No marketing language. No "exciting", no "transform".
4. Risks are named, not euphemized. "Cash is tight" → "Runway: 78 days. Trigger at 60."
5. Decisions and asks are explicit. If no ask, write "Ask: none this month."
6. Pack is dated and immutable once distributed.

## Metrics
- Packs produced: 12 / year.
- Median length: 6–10 pages.
- Time to compile: ≤ 4 hours from `MONTHLY_STRATEGY_REVIEW.md` close.

## Cadence
Monthly, within 3 days of month close.

## Evidence
`dealix-ops-private/board/`.

## Verifier
`make board-pack-verify` — checks file exists, every section filled, cross-links resolve.

## Runtime Command
`make board-pack month=YYYY-MM`

---

## Template

```
# Board Pack — YYYY-MM
Prepared by: Founder/CEO
Date: YYYY-MM-DD
Status: Draft / Final

## 1. Headline
- MRR: SAR X
- Cash: SAR X | Runway: NN days
- Sprints delivered with evidence (north star): N this month
- Audit score (rolling 4-week avg): NN / 100

## 2. The Month in One Page
<3–5 sentences. No fluff. What happened, what mattered, what is next.>

## 3. KPI Tree Snapshot
| KPI | Target Q | This month | Prior month | Direction |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 4. Pipeline & Revenue
- New qualified leads: N
- Proposals sent / accepted: N / N
- Proposal-to-payment rate (rolling 30d): NN%
- Retainer attach rate: NN%
- Revenue recognized this month: SAR X
- Top 3 deals in flight (anonymized):

## 5. Delivery
- Sprints completed: N
- On-time: N / N
- Evidence shipped: N artifacts (case-safe)
- Defects / refunds: N

## 6. Trust & Governance
- Trust artifacts updated: N
- Open flags: N
- Disclosure coverage: NN%
- Notable incident: <text or "none">

## 7. Bets
| Bet | Status | Deadline | Notes |
|---|---|---|---|

## 8. Kills this month
- <slug>: reason
- <slug>: reason

## 9. Capital Allocation (next month)
| Tier | % allocated |
|---|---|
| Revenue gen | NN |
| Delivery quality | NN |
| Trust | NN |
| Repeatability | NN |
| Automation | NN |
| Brand proof | NN |
| Optionality | NN |

## 10. Risks
- Cash:
- Customer concentration:
- Key person:
- Regulatory:
- Market:

## 11. Decisions made this month
1.
2.

## 12. Ask
<one paragraph or "none this month">

## 13. Appendix
- Link to MONTHLY_STRATEGY_REVIEW.md for this month.
- Link to KILL_LIST.md updates.
- Link to dealix-ops-private/weekly/ files.
```

## What stays out
- Real customer names (anonymized labels only).
- Revenue forecasts presented as fact (forecasts go in `FINANCIAL_MODEL_V1.md` with scenarios).
- Guarantees of any kind.
- Marketing claims about competitors.

## القواعد العربية
1. حزمة واحدة شهريًا، بالقالب نفسه.
2. الأرقام تستشهد بمصدرها. لا "تقريبًا".
3. المخاطر تُسمَّى، لا تُلطَّف.

## Cross-links
- `MONTHLY_STRATEGY_REVIEW.md`
- `CEO_KPI_TREE.md`
- `docs/finance/FINANCE_COMMAND_CENTER.md`
- `docs/14_trust_os/TRUST_DASHBOARD.md`
