# AI Unit Economics System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Focused on Results.

The AI Unit Economics System is the discipline by which Dealix
tracks the cost of AI inference per deal supported. AI is a cost
center; tracking it deliberately is how we keep the operating model
healthy as scale grows.

## Why this matters

Every Dealix agent burns AI cost. Drafting, eval, scoring, scorecard
assembly, brief generation — all consume tokens. Without tracking,
the cost compounds invisibly. With tracking:

- We can answer "what does it cost to land a deal?" honestly.
- We can detect drift (a costlier model, a more verbose worker, a
  feature flag that doubled cost).
- We can set thresholds that trigger investigations before they
  become problems.

## Source file

`finance/ai_unit_economics.csv` in the private ops runtime:

| Column                | Type    | Notes                                                       |
| --------------------- | ------- | ----------------------------------------------------------- |
| `ts`                  | ISO ts  | When the row was written.                                    |
| `ai_cost_usd`         | float   | USD AI spend in the period.                                  |
| `deals_supported`     | int     | Count of deals the AI motion supported.                      |
| `cost_per_deal_usd`   | float   | Derived: `ai_cost_usd / deals_supported`.                    |

Rows are appended at the end of each measurement period (default
weekly). The Finance Copilot is the sole writer.

## "Deals supported" definition

A deal is "supported" in a period if the AI motion produced or
materially advanced at least one artifact for the deal during the
period. Examples of supporting work:

- A draft outreach for the prospect.
- A draft reply to an objection.
- A sample sprint scoping note.
- A proposal draft.
- A reply-routing classification.

The Finance Copilot computes the count from
`outreach/conversation_log.csv`, `sales/proposal_queue.csv`, and
`sales/sample_queue.csv` joined on lead/client id.

## Cost capture

AI cost is captured per provider invoice. The Finance Copilot
reconciles weekly:

| Step                                         | Source                         |
| -------------------------------------------- | ------------------------------ |
| Pull provider usage                          | Provider portal / API.         |
| Map usage to date range                      | Provider portal.               |
| Convert to USD                               | Provider invoice currency.     |
| Append the row to `finance/ai_unit_economics.csv` | Finance Copilot.          |

The Finance Copilot does not auto-pull cost; the action is manual or
semi-automated with founder approval to authorize the pull.

## Thresholds

The system carries a single operating threshold: `cost_per_deal_usd`.
The threshold is set by the founder and reviewed quarterly. The
default starting band is:

| Band                   | Cost per deal USD       | Action                                                |
| ---------------------- | ----------------------- | ----------------------------------------------------- |
| Healthy                 | < $50                   | None.                                                 |
| Watch                   | $50 – $150              | Investigate weekly.                                   |
| High                    | $150 – $400             | Trust flag at `severity: medium`; investigate.        |
| Alert                   | > $400                  | Trust flag at `severity: high`; pause non-critical AI use; review. |

These bands are starting points and will be tightened as the
operating volume grows. The Founder Console exposes the latest band
in the finance-ops summary.

## Alert pipeline

When `cost_per_deal_usd` crosses into Alert:

1. The Finance Copilot writes a row to `trust/trust_flags.csv` with
   `severity: high` and a description naming the period.
2. The founder reviews in the next brief.
3. The founder approves either a pause of specific workers or a
   continuation with justification (recorded in
   `trust/approval_decisions.csv` with `action: risk_accept`,
   `risk: high`).
4. The Growth Strategist and Performance Analyst review which
   workers contributed most to the period's cost.

## Decomposition

For analytical purposes the Finance Copilot can decompose cost by
worker:

| Decomposition         | Source                                                                   |
| --------------------- | ------------------------------------------------------------------------ |
| Per agent              | Provider call logs joined with agent identifier (when available).        |
| Per worker             | Worker run records joined with provider call logs.                       |
| Per deal               | Cost attributed to the lead id from the conversation log.                |
| Per sector             | Aggregated cost per sector targeting.                                    |

The decomposition is ad hoc; the canonical CSV holds only the
aggregate.

## Cost drivers

| Driver                                       | Mitigation                                                          |
| -------------------------------------------- | ------------------------------------------------------------------- |
| Verbose prompts                              | Brand Guardian-led review of agent prompts.                         |
| Excessive tool use                            | Tool registry review; eval gate suite `tool_misuse`.                |
| Heavy fixtures in evals                       | Trim eval fixtures; favor regex over LLM-based eval where possible. |
| Heavy snapshots                               | Cache snapshots; only rerun on change.                              |
| Drafts that need many rewrites                 | Tighten the input data; sharpen the hypothesis.                     |

## Founder Console exposure

| Endpoint                       | Field                                              |
| ------------------------------ | -------------------------------------------------- |
| `GET /finance/summary`          | `ai_cost_30d_usd`                                  |
| `GET /finance-ops/summary`      | `ai_unit_cost_per_deal_usd` (latest row's value)   |

The 30-day AI cost is computed by summing
`ai_cost_usd` over rows in the trailing 30 days.

## What this system will not do

- Auto-pause an agent without founder approval.
- Auto-renegotiate provider terms.
- Surface customer-attributable cost data externally.

## Discipline

1. Track every period; never skip a week.
2. The threshold is a real action trigger, not theatre.
3. Decomposition is on-demand; the aggregate is the ledger.
4. Provider invoices reconcile to the CSV monthly.
5. Cost growth is normal as scale grows; cost-per-deal must not.

## Cross-references

- `ULTIMATE_FINANCE_OS.md` for the broader finance discipline.
- `REVENUE_KPI_TREE.md` for where unit economics sits in the tree.
- `LEARNING_LOOP.md` for how cost lessons become permanent changes.
- `NEXT_BEST_ACTION_ENGINE.md` for how cost factors into ranking.
