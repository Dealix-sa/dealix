# PRIVATE_OPS Runtime Contract

The `PRIVATE_OPS` root is the founder's working directory: a set of CSV files and artifact folders that mirror Postgres state for the systems that have not yet been migrated to the database, and a set of agent write targets that the runtime enforces against the agent registry.

**Source of truth:** this contract + filesystem layout under `$PRIVATE_OPS`
**Owner:** Engineering Lead + Founder
**Trust gate:** A2 — contract changes require founder approval.

## Directory layout

```
$PRIVATE_OPS/
├── audit_log.csv
├── revenue_factory_state.csv
├── revenue_factory_log.csv
├── sample_factory_queue.csv
├── proposal_factory_state.csv
├── proposal_corrections.csv
├── pricing_exceptions.csv
├── reply_routing_log.csv
├── objection_library.csv
├── payments_ledger.csv
├── early_start_exceptions.csv
├── finance_ledger.csv
├── ai_unit_economics.csv
├── delivery_state.csv
├── delivery_qa_log.csv
├── retention_state.csv
├── referral_pipeline.csv
├── customer_success_state.csv
├── client_health_score.csv
├── health_score_calibration.csv
├── proof_approval_log.csv
├── consent_records/
├── product_ladder_state.csv
├── distribution_state.csv
├── distribution_budget.csv
├── attribution_log.csv
├── offer_packages.csv
├── pricing_guardrails.csv
├── sales_scripts.csv
├── sales_coaching_log.csv
├── proposal_templates_state.csv
├── proposals_archive/
├── marketing_state.csv
├── marketing_incidents.csv
├── content_calendar.csv
├── founder_thoughts/
├── founder_content_queue.csv
├── landing_page_state.csv
├── copy_lint_rules.csv
├── email_outreach_log.csv
├── linkedin_outreach_log.csv
├── partner_pipeline.csv
├── partner_revenue_share.csv
├── sector_report_state.csv
├── sector_data/
├── newsletter_state.csv
├── brand_guardian_reviews.csv
├── growth_recommendations.csv
├── experiment_proposals.csv
├── distribution_queue.csv
├── drafts/
├── briefs/
├── package_drafts/
├── pricing_drafts.csv
├── performance_reads/
├── copilot_briefs/
├── trust_decisions.csv
├── escalations.csv
├── policy_exceptions.csv
├── eval_results/
├── prompt_eval_matrix.csv
├── kpi_tree_state.csv
├── conversion_diagnostics_log.csv
├── experiment_log.csv
├── learning_log.csv
├── nba_proposals.csv
├── suppression_list.csv
├── founder_decisions.csv
└── finance_archives/YYYY-MM/
```

## CSV row contract

Every CSV row carries:

- A stable primary key.
- `created_at` and `updated_at` (ISO 8601 UTC).
- `created_by` and `updated_by` (named agent or human id).
- `approval_class` where the row represents an action.

Append-only is the default. Updates are new rows. True deletions require A2 and are logged in `audit_log.csv`.

## Agent write targets

The agent registry (`registries/agent_registry.yaml`) `allowed_write_targets` lists, per agent, the exact paths it may write to. The runtime enforces this:

- Writes outside `allowed_write_targets` are denied with an audit row.
- Reads honour the same principle: an agent only reads paths it needs.

This is the runtime enforcement of LLM08 (excessive agency).

## Audit log

`audit_log.csv` is the append-only ledger of every consequential event:

- Agent dispatches.
- Trust Guardian decisions.
- Founder approvals.
- Policy changes.
- Kill switch activations.
- Export events.

The log is not editable. If a row is wrong, a correcting row is appended.

## Failure modes

- **Path drift:** an agent writes outside its allowlist. Detection: runtime + nightly diff. Recovery: deny, audit; agent paused.
- **Stale snapshot:** a CSV is not refreshed; an agent acts on old data. Detection: freshness check. Recovery: refresh or hold.
- **Bidirectional drift:** Postgres and CSV diverge. Detection: nightly reconciliation. Recovery: Postgres is canonical; CSV resynced.

## Recovery path

If `PRIVATE_OPS` is corrupted, the runtime fails closed for any write that touches it. Reads continue in degraded mode with a banner. Recovery is from Postgres snapshots and audit replay.

## Metrics

- Write denials per day.
- Path-drift incidents per quarter (target: 0).
- CSV-Postgres lag (seconds).
- Audit-log completeness (target: 100%).

## Disclaimer

The contract is the rule. The runtime enforces the rule. Estimated value is not Verified value.
