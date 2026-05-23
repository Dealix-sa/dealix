# CEO Dashboard Spec

> What the CEO dashboard must show. This is a specification, not the
> dashboard itself. Implementation lives in `dashboard/` and `apps/`.

## Tiles (Required)

### Row 1 — Money
- **Cash collected** (today / week / month).
- **MRR** (current vs. previous week).
- **Pipeline value** (open opportunities, weighted by stage).
- **Best next close** (single opportunity, with next action).

### Row 2 — Sales
- **DMs sent** (today, week-to-date).
- **Reply rate** (rolling 30-day).
- **Calls booked** (this week).
- **Proposals out** (count + total value).

### Row 3 — Delivery
- **Active clients** (count + status).
- **Due today** (deliverables).
- **Blocked** (with blocker reason).
- **QA queue** (items awaiting founder QA).

### Row 4 — Trust
- **Approvals waiting** (A2 + A3 count).
- **A3 blocked actions** (since last review).
- **Opt-outs** (this week).
- **Incidents** (open).

### Row 5 — System Health
- **Company Health Score** (single number, 0–100).
- **System scoreboard** (12 systems, PASS/FIX/BLOCKED).
- **CI status** (green / red).
- **Verification freshness** (hours since last run).

## Rules

1. Every tile shows the data source path and last-update timestamp.
2. No tile uses a forecasted or projected number without labeling it "PROJECTED".
3. Numbers tied to revenue cite the underlying ledger row.
4. The dashboard must load in under 2 seconds; otherwise it is not used.

## Out of Scope

- Long charts that need scrolling. The dashboard is a glance, not a report.
- Vanity metrics (followers, stars, page views) unless tied to a revenue loop.
