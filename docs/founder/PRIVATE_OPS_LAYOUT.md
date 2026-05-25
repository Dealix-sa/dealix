# Private Operations Layout

> The shape of `dealix-ops-private/` — a gitignored sibling of `docs/`.

This directory is **never** committed. It exists on the founder's local
machine and any approved secure backup. `make stage` scaffolds it on
first run.

## Layout

```
dealix-ops-private/
├── founder/
│   ├── ceo_command.md
│   ├── daily_brief.md
│   ├── decision_queue.md
│   ├── approvals_waiting.md
│   ├── risk_log.md
│   ├── focus_queue.md
│   ├── founder_time_log.md
│   ├── weekly_ceo_review.md
│   ├── board_pack.md
│   └── master_dashboard.md
├── revenue/
│   ├── revenue_action_log.csv
│   ├── cash_collected.csv
│   ├── pipeline_value.csv
│   ├── mrr_tracker.csv
│   ├── pricing_experiments.md
│   ├── payment_followup_templates.md
│   ├── invoices/
│   ├── receipts/
│   └── payments/
├── sales/
│   ├── pipeline.csv
│   ├── dms_sent.csv
│   ├── proposal_followups.csv
│   ├── call_notes/
│   ├── proposal_notes/
│   ├── refusals.csv
│   └── objections_log.md
├── delivery/
│   ├── sprint_register.csv
│   ├── samples/
│   ├── research/
│   ├── reports/
│   ├── qa/
│   ├── handoffs/
│   └── case_studies_private/
├── clients/
│   └── <client_id>/
│       ├── intake.yaml
│       ├── scope_confirmed.md
│       ├── icp_definition.md
│       └── deliverables/
├── client_success/
│   ├── retainers.csv
│   ├── health_scores.csv
│   ├── tiers.csv
│   ├── retainer_asks.csv
│   └── feedback/
├── trust/
│   ├── approvals_log.md
│   ├── incident_log.md
│   ├── autonomy_audit.md
│   └── audits/
├── finance/
│   ├── cash_plan.md
│   ├── expenses.csv
│   ├── monthly_finance_review.md
│   ├── runway_estimate.md
│   ├── capital_allocation_review.md
│   ├── refund_log.md
│   ├── transfers_log.md
│   └── founder_compensation.md
├── product/
│   ├── workflow_success_log.csv
│   ├── workflow_promotions.md
│   ├── feature_intake.md
│   └── build_defer_kill_log.md
├── engineering/
│   └── dora.csv
├── content/
│   ├── post_log.csv
│   ├── case_study_pre_consents/
│   └── case_study_consents/
├── people/
│   ├── roles.csv
│   ├── scorecards/
│   └── onboarding_logs/
└── partners/
    ├── partner_register.csv
    ├── referrals.csv
    └── scorecards/
```

## Scaffolding

`make stage` runs `scripts/dealix_ops_stage.py` which:

- Creates the directory structure above if missing.
- Creates empty CSVs with header rows.
- Creates placeholder Markdown files with the canonical headings.
- Reports anything it created (and anything that already existed).
- **Never** overwrites existing private files.

## Bootstrapping discipline

- Do **not** check anything from `dealix-ops-private/` into git, ever.
- Do **not** symlink from public to private (CI cannot follow).
- Do **not** paste content from private files into public posts without
  approval (`PUBLIC_PRIVATE_BOUNDARY.md`).

## Backup

- Local-first.
- Encrypted backup recommended; founder owns the key.
- Cloud backup only with explicit T3 decision and an end-to-end
  encryption mechanism.
