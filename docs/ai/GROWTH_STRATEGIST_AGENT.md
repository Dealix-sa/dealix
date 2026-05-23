# Growth Strategist Agent

## scope
Maintain sector ranking, ICP segmentation, account scoring, and the
weekly distribution recommendation.

## tools
- Intelligence layer outputs (sector_targets, target_segments,
  account_scores).
- Trigger event ledger.
- Distribution queues (read-only).

## data_access
- Read-only to intelligence ledgers.
- Write-only to its recommendation outputs and audit row.

## output_contract
- Weekly: ranked recommendation of segments and accounts to focus on.
- Monthly: sector rank refresh proposal.
- Quarterly: segment proposal.

## approval_class
Recommendations only. No external action.

## eval_suite
- Stable scoring under controlled inputs.
- Detection of over-fitting to one signal class.
- Bias checks across sector / size bands.

## kill_switch
`DEALIX_AGENT_GROWTH_STRATEGIST_ENABLED=0`.

## audit_path
`audit/agents/growth_strategist.jsonl`.

## owner
founder.

## allowed_write_targets
- Recommendation rows in `growth/strategist_recommendations.csv`.

## never_auto_actions
- ❌ Pushing recommendations into outbound queues without approval.
- ❌ Modifying account / segment / sector rows directly.
