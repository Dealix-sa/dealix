# Performance Analyst Agent

The Performance Analyst agent produces the weekly performance read: KPI tree movements, conversion diagnostics, and experiment results. It does not act.

**Source of truth:** `registries/agent_registry.yaml` entry `performance_analyst`
**Owner:** Founder + Marketing Lead
**Trust gate:** A0 for internal read-outs; A1 for external sharing (e.g. with a client).

## Spec

| Field | Value |
|-------|-------|
| `id` | `performance_analyst` |
| `name` | Performance Analyst |
| `purpose` | Produce weekly performance read and diagnostics |
| `approval_class_max` | A1 |
| `tools` | `read_factory_state`, `read_unit_economics`, `read_experiment_log`, `read_value_ledger`, `write_analysis` |
| `outputs` | `weekly_performance_read`, `diagnostic_note` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | founder |
| `allowed_write_targets` | `$PRIVATE_OPS/performance_reads/` |

## What it does

1. Reads the Revenue KPI Tree state (`docs/performance/REVENUE_KPI_TREE.md`).
2. Computes week-over-week movement at each node.
3. Identifies the node whose movement explains most of the parent change.
4. Cross-references active experiments (`docs/performance/EXPERIMENT_BACKLOG.md`).
5. Drafts a performance read with: headline movement, leading explanation, supporting evidence, recommended diagnostic.

## OWASP LLM Top 10 posture

- **Excessive agency (LLM08).** The agent reads and writes one artifact type. It does not change KPIs, pause experiments, or move budget.
- **Hallucination control.** Every numeric claim cites the source row id and timestamp. The eval suite penalises uncited claims.
- **Sensitive information disclosure (LLM06).** Reads include client identifiers; outputs to external audiences are reviewed for case-safe framing.

## Eval

- Numeric accuracy: spot-checked against source CSVs.
- Causal-language discipline: "explained by" and "associated with", never "caused by" without an experiment.
- No-guarantee language.
- Citation density: every number sourced.

## Failure modes

- **Numerical drift:** computed KPIs disagree with source. Detection: spot audit. Recovery: re-run, flag discrepancy.
- **Spurious causation:** agent attributes movement to an experiment when timing is coincidental. Detection: human review. Recovery: re-train on counterfactual examples.
- **Stale read:** the read uses data from a paused pipeline. Detection: freshness check. Recovery: refresh or hold.

## Recovery path

If the analyst's numbers diverge from source, the founder kills it; reads are done manually until source-of-truth pipelines are reconciled.

## Metrics

- Reads per week.
- Numerical accuracy (spot-checked).
- Decisions made on the back of the read (estimated).
- Eval pass rate.

## Disclaimer

The performance read is analysis, not advice. Dealix does not guarantee that any read leads to a positive decision. Estimated value is not Verified value.
