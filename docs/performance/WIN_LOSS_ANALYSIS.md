# Win/Loss Analysis

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Focused on Results.

Win/Loss Analysis is the structured review of completed proposals,
won or lost, that turns outcomes into operating learning. It is the
late-funnel companion to Conversion Diagnostics and the upstream
companion to Objection Analytics.

## Source data

The primary table is `sales/proposal_queue.csv` in the private ops
runtime. Win/Loss adds two derived tables:

| Table                                  | Purpose                                       |
| -------------------------------------- | --------------------------------------------- |
| `performance/win_loss.csv`              | One row per closed proposal with the W/L tag. |
| `performance/win_loss_tags.csv`         | Tag dictionary used in W/L coding.            |

Schemas are written by the Performance Analyst on first run; until
then the analysis is performed inline from the proposal queue.

### `performance/win_loss.csv`

| Column            | Notes                                                     |
| ----------------- | --------------------------------------------------------- |
| `proposal_id`     | Foreign key into `sales/proposal_queue.csv`.              |
| `client`          | Client display name.                                      |
| `sector`          | Sector code from `growth/sector_targets.csv`.             |
| `rung`            | Offer rung from `product/offer_ladder.csv`.               |
| `value_sar`       | Proposal value.                                           |
| `outcome`         | `won`, `lost`, or `no_decision`.                          |
| `primary_reason`  | One tag from `performance/win_loss_tags.csv`.             |
| `secondary_reasons` | Pipe-separated list of additional tags.                 |
| `evidence_ref`    | Pointer to the source (email thread, meeting note, etc.). |
| `coded_at`        | ISO ts.                                                   |
| `coded_by`        | `performance_analyst` or `founder`.                        |

### `performance/win_loss_tags.csv`

| Tag                          | Family             | Notes                                          |
| ---------------------------- | ------------------ | ---------------------------------------------- |
| `pricing_too_high`           | pricing            | Customer cited price as the primary blocker.   |
| `scope_too_broad`            | scope              | Customer felt scope exceeded need.             |
| `scope_too_narrow`           | scope              | Customer felt scope insufficient.              |
| `trust_concern`              | trust              | Customer asked about residency or compliance.  |
| `timing_not_ready`           | timing             | Customer not ready to commit.                  |
| `competitor_chosen`          | competitive        | Customer chose an alternative.                 |
| `internal_priority_shift`    | internal           | Customer internal change.                      |
| `champion_lost`              | champion           | Champion left or was reassigned.               |
| `decision_committee_blocked` | committee          | Committee did not align.                       |
| `proof_insufficient`         | proof              | Customer wanted more proof.                    |
| `sample_sprint_landed`       | proof              | Win driven by sample sprint outcome.           |
| `roi_clear`                  | value              | Win driven by clear ROI framing.               |
| `founder_relationship`       | relationship       | Win driven by direct founder relationship.     |
| `procurement_alignment`      | process            | Win driven by procurement-friendly motion.     |

The tag dictionary is closed: adding a new tag requires a Growth
Strategist approval recorded in the audit ledger.

## Coding discipline

A closed proposal is coded within seven days of its close. The
Performance Analyst drafts the coding; the founder reviews. The
discipline:

| Rule                                                              | Why                                                                     |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Exactly one primary reason per outcome                            | Force a ranking; otherwise everything is "complex".                     |
| At most three secondary reasons                                   | Limit dilution.                                                         |
| Evidence reference is mandatory                                    | A win/loss reason without evidence is a hypothesis, not a finding.      |
| `no_decision` outcomes are coded after 60 days                    | Avoid premature closure on slow processes.                              |
| Founder reviews every loss                                        | Loss patterns drive operating change; do not delegate.                  |

## Aggregations

The Performance Analyst surfaces three aggregations weekly:

1. **Outcome breakdown by sector**: counts of `won` / `lost` /
   `no_decision` × sector.
2. **Primary reason heatmap**: tag × sector cells, with cell value as
   count and color as severity (loss-heavy cells red).
3. **Rung outcome distribution**: outcome × offer rung. Used to
   detect rung misfit.

## Outputs

The weekly Win/Loss meeting produces:

- A one-page summary: top three wins, top three losses, lessons.
- Up to two new experiment drafts.
- Up to one update to the Objection Analytics handbook
  (`OBJECTION_ANALYTICS.md`).
- Updates to the lesson register at `medium` or `high` confidence.

## Feedback into the operating system

| Win/Loss finding                          | Operating action                                            |
| ----------------------------------------- | ----------------------------------------------------------- |
| `pricing_too_high` cluster in a sector    | Review the offer ladder for that sector.                    |
| `proof_insufficient` cluster              | Prioritize proof generation in the Proof Safety Agent.      |
| `trust_concern` cluster                   | Strengthen the sovereign readiness narrative.               |
| `sample_sprint_landed` cluster of wins    | Codify the sample sprint pattern in the playbook.           |
| `champion_lost` cluster                   | Build a stakeholder-mapping artifact in onboarding.         |
| `procurement_alignment` cluster of wins   | Codify the procurement playbook.                            |

## Anti-patterns

| Anti-pattern                              | Why to avoid                                                                |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| Anonymous wins                            | A win not coded against an account is a win not learned from.               |
| Reason-bingo (lots of tags)               | Forces clarity into noise; pick a primary and live with it.                 |
| Coding without the customer voice         | Use customer language where possible; do not project.                       |
| Treating `no_decision` as a loss          | They are different patterns. Code them differently.                         |
| Skipping losses                           | Losses are the highest learning yield. Do not skip them.                    |

## Founder Console exposure

The Win/Loss tables are not yet exposed via an endpoint. They surface
in the weekly scorecard refresh and the founder brief. A future
`/api/v1/internal/performance/win-loss` endpoint will read the table
once the schema stabilizes.

## Cadence

| Activity                | Cadence       |
| ----------------------- | ------------- |
| Coding new closures     | Within 7 days |
| Weekly Win/Loss meeting | Weekly        |
| Tag dictionary review   | Quarterly     |
| Aggregation refresh     | Weekly        |

## Discipline

1. Every closed proposal is coded.
2. Every code has evidence.
3. Every cluster yields an action.
4. The customer's words are the primary source.
5. Losses are reviewed by the founder.
