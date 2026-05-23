# Sector Performance — أداء القطاعات

## Purpose
Track per-sector outcomes across sprints: client-reported conversion patterns, satisfaction, renewal, and reference willingness. Inform which sectors Dealix focuses on next quarter.

## Owner
Founder. Sector leads per sector.

## Inputs
- Closed sprints tagged by sector code.
- Client-reported outcome data at 30-day check-in.
- Renewal data from `docs/delivery/RENEWAL_PROCESS.md`.
- Win-loss reviews per sector.

## Outputs
- Per-sector scorecard updated monthly.
- Quarterly recommendation on sector focus.

## Rules (numbered)
1. Sector codes are pulled from the intake list; new codes require A2 approval.
2. Conversion data is client-reported, not Dealix-inferred.
3. Every cell shows sample size; cells under 5 sprints are "low confidence".
4. Sector recommendations are written, not implicit.
5. Sectors with persistently weak scorecards (below threshold for 2 consecutive quarters) trigger a focus review.

## Metrics
- Sprints per sector per quarter.
- Renewal rate per sector.
- Acknowledgement rate at handoff per sector.
- Reference willingness per sector.

## Cadence
Updated monthly. Reviewed quarterly.

## Evidence (paths)
- `docs/learning/registers/sector_performance/<quarter>.md`

## Verifier
Founder.

## Runtime Command
`make learning.sectors.scorecard` refreshes the per-sector scorecards.

## Sector scorecard

Per sector, the scorecard captures:

- Sprints closed this quarter and lifetime.
- Median acknowledgement time at handoff.
- Renewal rate (sprint-to-sprint).
- Reference willingness rate (would the client be referenced).
- Top reasons clients cited for value.
- Top reasons clients cited for hesitation or non-renewal.
- Operator hours per sprint in this sector (cost signal).

## Sector focus decision

Quarterly, the founder reads all sector scorecards and produces a one-paragraph decision on which sectors get priority next quarter. The decision is logged in `COMPANY_MEMORY.md` and feeds the monthly strategy update.

The decision considers:

- Renewal rate (the most reliable signal).
- Operator hours per sprint (cost signal; high-cost sectors need higher value).
- Sample size (we do not abandon a sector after 2 sprints).
- Strategic position (some sectors are kept for portfolio reasons).

## Worked example

Sector: Industrial equipment (KSA Eastern region).

- Sprints closed this quarter: 4. Lifetime: 9.
- Median acknowledgement: 36 hours.
- Renewal rate: 67 percent (6 of 9).
- Reference willingness: 4 of 9 clients.
- Top value cited: source-cited evidence pack quality, sector-specific signals.
- Top hesitation cited: clients want help with sending (currently out of default scope; A3 path documented).
- Operator hours per sprint: at baseline.

Recommendation: continue prioritization; document the sending-assist offering as an explicit optional add-on with A3 approval flow.

## Operating substance
Sector performance is the lens through which Dealix decides where to invest. Sprints in a sector with 67 percent renewal compound; sprints in a sector with 20 percent renewal drain. The scorecard makes the difference visible.

The data is patient. After 2 sprints in a sector, the scorecard is anecdotal. After 10 sprints, it is signal. We do not rush sector decisions based on small samples.

Operator hours per sprint is the cost signal that often gets ignored. A sector where a sprint takes 30 percent more operator hours than baseline must produce 30 percent more value to be worth the same priority. The scorecard surfaces this honestly.

Client-reported only. Sector performance is not measured by Dealix's view of the work; it is measured by client behavior at renewal and reference. Those are the two metrics that survive contact with reality.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
