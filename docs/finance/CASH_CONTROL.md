# التحكم بالنقد — Cash Control

> Daily cash check. Weekly runway calc. Alert thresholds.

## Purpose
Cash is the only metric that, when zero, ends Dealix. This file is the daily safeguard.

## Owner
Founder/CEO.

## Inputs
- Bank balances (Dealix accounts).
- Card processor pending settlements.
- Open invoices (`INVOICE_WORKFLOW.md`).
- Open payables.
- Burn rate (rolling 30 days net cash out, excluding capital injections).

## Outputs
- Daily cash entry in `dealix-ops-private/finance/cash/YYYY-MM-DD.md`.
- Weekly runway calc.
- Alert state (Green / Yellow / Orange / Red).

## Rules
1. Cash is checked daily before 9:00 AM Riyadh.
2. The runway figure is computed weekly with primary data, not interpolated.
3. Alert states are computed against current runway. State transitions trigger named actions.
4. Foreign currency holdings are converted to SAR at the day's mid-market rate.
5. Customer deposits classified as deferred revenue do not count as Dealix cash position for runway math beyond their committed delivery cost.

## Metrics
- Cash today (SAR).
- Runway (days).
- Burn 30d (SAR/month).
- Days to first action threshold (predicted at current burn).

## Cadence
Daily check. Weekly runway. Monthly trend.

## Evidence
`dealix-ops-private/finance/cash/`.

## Verifier
`make cash-control-verify` — checks today's entry exists with cash, burn, runway, and alert state.

## Runtime Command
`make cash-check`

---

## Alert thresholds

| State | Runway | Trigger actions |
|---|---|---|
| Green | ≥ 180 days | Normal operations |
| Yellow | 90–179 days | Founder time shifts: Revenue bucket ≥ 35% |
| Orange | 60–89 days | Emergency Protocol Step 1 |
| Red | < 60 days | Emergency Protocol Step 2; brief advisor |

## Emergency Protocol Step 1 (Orange)
1. Daily cash check moves to twice-daily.
2. Founder time: Revenue bucket ≥ 50%.
3. Pause Tier 5–7 capital allocation (per `CAPITAL_ALLOCATION_SYSTEM.md`).
4. Tighten DSO: reminders move to day 3 / day 7 / day 14.
5. Discount discipline: no discounts > 10% without founder approval.
6. Pipeline pull-forward: review all open proposals for closeability this week.

## Emergency Protocol Step 2 (Red)
All Step 1 actions, plus:
1. Brief one advisor (informally) with the cash picture.
2. Activate `BAD_REVENUE_FILTER.md` strict mode: reject any deal below margin floor.
3. Consider invoice pull-forward (issue final tranches early if deliverable accepted earlier).
4. Personal liquidity review by the founder.
5. Communicate runway transparently within the team if any team exists.

## Daily cash entry template

```
# Cash — YYYY-MM-DD

Bank balance SAR: X
Processor pending SAR: X
Total available SAR: X

Today's expected cash in: SAR X (from <invoice ids>)
Today's expected cash out: SAR X (from <payee list>)

Burn 30d (SAR/month): X
Runway days: NNN
Alert state: Green / Yellow / Orange / Red

Notes:
- <any anomaly>
- <forecasted shortfall>
```

## Weekly runway calc

Runway = current cash / mean_burn_30d × 30, in days.

Where `mean_burn_30d` is the trailing 30-day net cash out (excluding capital injections and deferred revenue inflows).

Cross-check: compare against the bear scenario in `FINANCIAL_MODEL_V1.md`. A gap > 20% triggers a model refresh.

## What is NOT cash for runway purposes
- Open invoices (booked, not cleared).
- Customer deposits classified as deferred revenue beyond their delivery cost.
- Verbal commitments.
- Anticipated proposal closes.

## Disclosure
Cash figures are internal. They appear in the Board Pack with rounding. They never appear in customer-facing docs.

## القواعد العربية
1. النقد يُفحص يوميًا قبل التاسعة صباحًا.
2. حساب المدرج النقدي أسبوعيًا ببيانات أولية، لا بتقدير.
3. حالات التنبيه تُفعِّل إجراءات مسماة.

## Cross-links
- `FINANCE_COMMAND_CENTER.md`
- `FINANCIAL_MODEL_V1.md`
- `CAPITAL_ALLOCATION_SYSTEM.md`
- `docs/revenue/BAD_REVENUE_FILTER.md`
- `INVOICE_WORKFLOW.md`
- `docs/founder/CEO_COMMAND_CENTER.md`
