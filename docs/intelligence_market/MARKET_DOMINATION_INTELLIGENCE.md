# Market Domination Intelligence

The intelligence layer that feeds every Dealix machine. Outputs are
**ranked, scored, or recommended** — never raw automation triggers.

## 1. Layer responsibilities

| Layer | Output | Owner |
|---|---|---|
| Market map | Sector tree with size, density, accessibility per sector. | growth_strategist |
| Sector ranking | Ordered list of target sectors with a composite score. | growth_strategist |
| ICP segmentation | Sub-segments with persona, pain, budget, accessibility. | offer_architect |
| Buyer persona | Named persona, jobs, pains, gains, channels. | content_strategist |
| Trigger events | Time-bound signals worth acting on. | distribution_operator |
| Competitor intelligence | Battle cards, gap analysis, positioning deltas. | growth_strategist |
| Account scoring | Per-account composite score 0-100. | account_scoring_machine |

## 2. Inputs (allowed, with provenance)

- Public registries (CR, MCI, Chambers of Commerce, SDAIA).
- Public web (sector trade pubs, RFP boards, regulator notices).
- Customer-uploaded CRMs (with their consent).
- Internal proof artifacts.
- Approved enrichment providers.

Every record carries `source`, `collected_at`, `consent_status`,
`allowed_use`. Records without these never reach the scoring layer.

## 3. Outputs

- `growth/sector_targets.csv` — sector rank with composite score.
- `growth/account_scores.csv` — per-account composite + sub-scores.
- `growth/target_segments.csv` — ICP segments with persona linkage.
- `intelligence/trigger_events.csv` (queue) — bounded list per week.

## 4. Refresh cadence

- Sector ranking: monthly.
- ICP segmentation: quarterly.
- Account scoring: weekly.
- Trigger events: daily.
- Competitor intelligence: monthly.

## 5. Quality gates

- No record reaches scoring without `source` and `consent_status`.
- No score is published with > 30 % fallback-sourced fields.
- Every ranked list shows the timestamp and source mix at the top.
- Drift (a sector moving > 20 percentile in one cycle) raises a flag
  for the growth_strategist to review.

## 6. Failure modes

| Failure | Symptom | Recovery |
|---|---|---|
| Provider outage | Coverage drops > 20 % | Surface `source=fallback`; pause auto-ranking. |
| Stale data | `collected_at` > 60 days for > 30 % | Mark sector "stale"; recommend a refresh. |
| Schema drift | Field validation fails | Block ingestion; surface to control plane. |
| Excessive change | Score moves > ±25 in one cycle | Hold for human review. |
