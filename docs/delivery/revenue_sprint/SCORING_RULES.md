# Scoring Rules — قواعد تقييم الفرص

## Purpose
Define how raw research rows are converted into scored, ranked leads. Scoring must be reproducible by a second operator within ±1 point per dimension.

## Owner
Head of Delivery. Sector lead (per-sector calibration).

## Inputs
- Raw research rows from Day 2.
- Intake ICP, deal-size band, geo, exclusions.
- Sector reference notes under `docs/sector-reports/`.

## Outputs
- Three integer scores per row (fit, signal, reach), 0–5 each.
- A total score 0–15.
- A ranked, deduplicated, exclusion-filtered list.

## Rules (numbered)
1. Three dimensions only: fit, signal, reach. No hidden multipliers.
2. Each dimension uses a published rubric (below). Scores must cite the rubric line that justified them when challenged in QA.
3. Two operators must agree within ±1 per dimension on a 10-row sample before scoring proceeds.
4. Exclusions override scores. An excluded row is moved to `excluded.csv` with reason.
5. No personal-trait scoring. No inferences about individuals.
6. Scores are not predictions of revenue. They are pack-ranking inputs.

## Metrics
- Inter-rater agreement on the 10-row sample: target ≥ 80%.
- Top-quartile coverage in the shipped pack.
- Rubric-citation completeness at QA: 100% on requested rows.

## Cadence
Per sprint. Rubrics reviewed quarterly in `docs/learning/SECTOR_PERFORMANCE.md`.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/scoring_calibration.md`
- `docs/audit/sprints/SPRINT_<ID>/lead_table.csv`

## Verifier
Sector lead. Head of Delivery on first sprint of any new sector.

## Runtime Command
`make sprint.scoring.calibrate SPRINT=<ID>` — runs the 10-row dual-scoring check.

## Rubrics

**Fit (0–5).** How well the buyer company matches the intake ICP.
- 0: Out of scope (geo, sector, or size).
- 1: Adjacent sector, weak size match.
- 2: Same sector, size band off by one tier.
- 3: Same sector, correct size band, weak sub-sector match.
- 4: Same sector, correct size band, correct sub-sector.
- 5: Bullseye match with named buying-center role available publicly.

**Signal (0–5).** Strength of the publicly observable buying signal.
- 0: No signal observed.
- 1: Generic web presence only.
- 2: Recent (<180 days) news mention, weak buying relevance.
- 3: Recent hiring, expansion, or filing with possible buying relevance.
- 4: Public tender, RFP, or named procurement initiative aligned to the client's offer.
- 5: Public tender or contract award explicitly in scope, with date <60 days.

**Reach (0–5).** Reachability via in-scope channels from the intake.
- 0: No in-scope channel available.
- 1: Channel exists but heavily gated.
- 2: Public form or association membership, low response baseline.
- 3: Public corporate channel (email or form) with normal response baseline.
- 4: Multiple in-scope channels.
- 5: Active tender portal or association relationship Dealix can reference.

## Operating substance
Scoring is a ranking aid, not a forecast. We rank to choose which rows ship in the top of the pack and which sit lower or get cut. The client receives the scores with the rubric so they can re-score if their internal definition differs.

Dual scoring on a 10-row sample at the start of each sprint is the calibration step. If two operators disagree by more than 1 point on more than 20% of rows, the sector lead reviews the rubric application and the operators recalibrate before continuing. This step takes 20 minutes and prevents an entire pack from being mis-ranked.

We do not score individuals. We do not infer personality, intent, or character. We score the company-level fit, the public signal, and the channel availability. The buyer remains a company in the lead table; the named role appears only as a published title.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
