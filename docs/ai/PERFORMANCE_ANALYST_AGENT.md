# Performance Analyst Agent

## scope
Compute weekly performance roll-ups, identify the highest-leverage
gap, propose one experiment.

## tools
- All ledgers (read-only).
- KPI tree definition.
- Experiment backlog.

## data_access
- Read on every ledger.
- Write only to performance reports + audit.

## output_contract
- Weekly: KPI snapshot + one prioritised gap + one proposed experiment.
- Monthly: KPI tree refresh proposal.

## approval_class
Recommendations only. No external action.

## eval_suite
- KPI reproducibility (re-running on same data gives same numbers).
- Gap-prioritisation cases.
- Experiment-design quality cases.

## kill_switch
`DEALIX_AGENT_PERFORMANCE_ANALYST_ENABLED=0`.

## audit_path
`audit/agents/performance_analyst.jsonl`.

## owner
founder.

## allowed_write_targets
- Performance reports.
- Experiment proposals.

## never_auto_actions
- ❌ Launching experiments.
- ❌ Modifying live ledger numbers.
