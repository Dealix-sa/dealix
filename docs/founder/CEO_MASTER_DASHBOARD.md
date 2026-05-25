# CEO Master Dashboard — Spec — لوحة قيادة المؤسس الرئيسية

## Purpose
The single dashboard the founder reads each morning. Ten panels, fixed layout, no hiding. Drives the daily and weekly decisions. Every other command center feeds into this one.

## Owner
Founder. Maintained personally for first 90 days; ops manager assists after.

## Inputs
- All command centers (productization, content, client success, partner, delegation).
- Finance pack (cash, runway, MRR).
- Trust OS incidents.
- A3 active items.

## Outputs
- A single live page (markdown or rendered).
- Daily glance, weekly review.

## The 10 Panels

### Panel 1 — Founder Focus
- What is the founder's #1 priority this week (one sentence).
- Top 3 calendar blocks for the week.
- Hours actually spent on #1 last week (variance vs plan).
- Source: `docs/founder/CEO_OPERATING_MODEL.md`.

### Panel 2 — Revenue Score
- Cash collected this week / month.
- MRR (if any).
- Pipeline value (estimated, labelled).
- Source: `docs/finance/`.

### Panel 3 — Pipeline
- Qualified opportunities (count, value).
- Stages distribution.
- Cycle time median.
- Source: `docs/01_go_to_market/`.

### Panel 4 — Cash / MRR / Runway
- Cash balance.
- Monthly burn.
- Runway months.
- Source: `docs/finance/`.

### Panel 5 — Delivery Readiness
- Active sprints (count, health).
- On-time milestone rate.
- Capacity utilization.
- Source: `docs/03_commercial_mvp/` + `docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md`.

### Panel 6 — Trust Risks
- Open incidents (count, severity).
- PDPL findings.
- Banned-practice incidents (target 0).
- Source: `docs/14_trust_os/`.

### Panel 7 — Stage Readiness (Proof Gates)
- Current proof gate.
- Gate passed (date) / gate active (kill criterion).
- Days into gate.
- Source: `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.

### Panel 8 — Learning / Decision
- This week's A3 items.
- Decisions to be made by founder this week.
- Decisions to take back from delegates.
- Source: `docs/founder/CEO_OPERATING_MODEL.md`.

### Panel 9 — Productization Candidates
- Candidates by stage (Manual / Template / Automation / SaaS Candidate).
- Promotion-ready and kill-ready candidates.
- Source: `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.

### Panel 10 — Kill / Defer List
- Items killed this month.
- Items deferred (with revisit date).
- Estimated focus saved (labelled).
- Source: `docs/product/BUILD_DEFER_KILL.md` + `docs/founder/CEO_NOT_NOW_LIST.md`.

## Rules
1. No panel hidden. If a panel is empty, the founder writes why.
2. Numbers labelled estimated or verified; the disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" appears at the bottom.
3. Dashboard reviewed every Monday morning, 30 minutes.
4. No clients named on this dashboard if it is screen-shared.
5. The dashboard cannot exceed one page when printed.

## Metrics
- Dashboard review on-time rate (target 100%).
- Panels with no data (target 0; gaps are a signal).
- Decision turnaround time on Panel 8 (median ≤ 7 days).

## Cadence
- Daily glance.
- Weekly review (30 min).
- Monthly variance review.

## Evidence
- Weekly snapshot under `evidence/founder/dashboard/<YYYY-Www>.md`.

## Verifier
Founder.

## Runtime Command
`make ceo-dashboard` — composes the 10-panel view from source command centers, refuses publication if any panel is empty without an explanation.

## Arabic Summary — ملخص عربي
عشر لوحات: التركيز، الإيرادات، الأنبوب، النقد، التسليم، الثقة، بوابات الإثبات، التعلم، مرشحو التحويل لمنتج، قائمة الإلغاء. لا إخفاء، لا أكثر من صفحة، لا عملاء مسمَّون عند مشاركة الشاشة. القيم التقديرية ليست مُتحقَّقة.
