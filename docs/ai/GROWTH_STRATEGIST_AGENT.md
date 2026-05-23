# Growth Strategist Agent

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Growth Strategist scores sectors and accounts and surfaces
> next-best growth moves. It does not execute. It recommends; the
> founder decides.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `growth_strategist`                                                    |
| `name`                      | Growth Strategist                                                      |
| `purpose`                   | Update sector scoring, surface next-best growth moves.                 |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `account_scoring_model`, `sector_targets_reader`, `growth_recommender` |
| `outputs`                   | `growth/sector_targets.csv`, `growth/account_scores.csv`, `growth/next_best_moves.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `growth/`                                                              |
| `KPI`                       | Account score precision (recommended accounts that produce qualified conversations), sector hit rate, refusal rate |
| `failure_mode`              | Over-recommends within a narrow sector; recommends targets on the suppression list; recommends growth moves without evidence backing |

## Purpose

The Growth Strategist maintains the sector scoring model and the
account scoring model. Each week it produces a refreshed list of
accounts with scores and a list of next-best growth moves for the
founder to review. The agent does not draft outreach (that is the
Distribution Operator's job) and does not commit any external
action.

## Responsibilities

- Maintain sector scoring against criteria such as: Dealix existing
  evidence, sector partner presence, founder-set allow-list,
  PDPL/regulatory posture.
- Score accounts against criteria such as: signal strength,
  relationship status, sector fit, suppression status, refusal
  flags.
- Surface next-best moves — "consider engaging this sector body",
  "consider drafting a sector report excerpt for this sector",
  "consider deferring this sector until evidence improves".
- Maintain a record of refused recommendations and their reasons.

## Tools

- `account_scoring_model` — the scoring model with documented
  weights. Weights are reviewed quarterly.
- `sector_targets_reader` — reads `growth/sector_targets.csv` and
  related sector evidence.
- `growth_recommender` — the next-best-move recommender, driven by
  the scoring model and the audit ledger.

## Outputs

- `growth/sector_targets.csv` — sector list with status (`active`,
  `evaluated`, `declined`, `paused`) and rationale.
- `growth/account_scores.csv` — accounts with current score, signal
  set, suppression status, and recommendation state.
- `growth/next_best_moves.csv` — recommended moves for the founder
  with rationale and evidence links.

Outputs are append-only for history; current-state rows are
overwritten with versioned change notes.

## External Action

Always `false`. The Growth Strategist does not contact accounts.
Its recommendations are read by the Distribution Operator and the
founder.

## Kill Switch

Anyone with operator role can pause. Reasons to pause:

- The scoring model has drifted.
- A sector has been added that requires a manual review before
  scoring resumes.
- The agent has produced recommendations that include suppressed
  identities.

## Eval Requirements

The agent's eval suite covers:

- Scoring stability across runs.
- Suppression cross-check (no scored account is on the suppression
  list).
- Refusal-list compliance (no account in a refusal-list sector is
  scored without explicit founder override).
- Evidence presence on every "next best move" recommendation.

A failed eval pauses new recommendations until resolved.

## Audit Requirements

Every scoring run writes an audit entry covering:

- Model version.
- Weights used.
- Number of accounts scored.
- Number of accounts above the engagement threshold.
- Number of recommendations produced.
- Number of refusal overrides triggered.

## Owner

Founder.

## Allowed Write Targets

`growth/` only.

## KPI

- Account score precision: of accounts recommended for outreach,
  what fraction produce a qualified conversation within a
  defined window.
- Sector hit rate: of sectors recommended for activation, what
  fraction produce an R2+ engagement within two quarters.
- Refusal rate: fraction of accounts recommended that are later
  refused by the founder for scope, relationship, or signal
  reasons. A persistently high refusal rate indicates model drift.

## Failure Modes

- The agent over-recommends within a narrow sector (one strong
  signal dominates). Mitigation: the scoring weights are
  recalibrated quarterly; a sector diversity check is added to the
  eval.
- The agent recommends targets on the suppression list. Mitigation:
  suppression cross-check is a blocking eval; the agent cannot
  publish recommendations until cross-check passes.
- The agent recommends moves without evidence backing. Mitigation:
  evidence presence is a blocking eval; recommendations without
  evidence links are blocked.
- The scoring model drifts toward optimising for ease-of-engagement
  over fit. Mitigation: the founder reviews the model weights
  quarterly with the Performance Analyst.

## Cross-Agent Dependencies

- Reads from the Distribution Operator's response patterns to
  inform scoring.
- Reads from the Performance Analyst's funnel data.
- Writes recommendations consumed by the Distribution Operator and
  the founder.
- Refusals recorded here feed the Trust Guardian's monthly review.

## Operating Cadence

- Weekly: full scoring refresh; recommendations queued for founder
  review.
- Monthly: sector list review.
- Quarterly: scoring weights review with the founder.

## Banned Behaviours

- Scoring accounts on the suppression list as engagement-ready.
- Producing recommendations without evidence backing.
- Producing recommendations that imply guaranteed outcomes.
- Writing outside `growth/`.
- Invoking tools not in its tool list.

## Failure Response

If a scoring run is found to have included suppressed identities:

1. The run is invalidated.
2. The Trust Guardian opens a high-severity flag.
3. The scoring model is paused.
4. The suppression integration is repaired.
5. The model is restored after eval passes.

## Why an Agent, Not a Spreadsheet

A spreadsheet records scores. The Growth Strategist updates them
continuously against new evidence, refusals, sector observations,
and trust events. The agent is the discipline that keeps scoring
honest week over week. A spreadsheet drifts; the agent's audit
trail makes drift visible.

## Cross-References

- Distribution OS: `docs/product/PRODUCT_DISTRIBUTION_OS.md`.
- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Agent registry: `registries/agent_registry.yaml`.
- Trust contract: `policies/dealix_control_policy.yaml`.
