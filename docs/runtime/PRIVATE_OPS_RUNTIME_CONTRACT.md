# Private Ops Runtime Contract

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The private ops runtime is the directory tree at
`/opt/dealix-ops-private` (or `$PRIVATE_OPS`) that holds Dealix's
operational state outside the repository. This document is the
authoritative contract for the folder tree, the CSV schemas, and the
write rules. The schema list mirrors
`scripts/bootstrap_private_ops_runtime.py` exactly.

## Why "outside the repo"

The private ops runtime is intentionally outside the repo. Three
reasons:

1. **Trust boundary.** A compromise of the application or the
   repository does not put audit, suppression, or queue state at
   risk.
2. **PDPL alignment.** Personal data flowing through queues does not
   end up in version control.
3. **Operability.** Operators can inspect, back up, and restore the
   tree without involving the application.

The path is configurable via `PRIVATE_OPS` or
`DEALIX_PRIVATE_OPS_DIR` environment variables. The default is
`/opt/dealix-ops-private`.

## Bootstrap

The directory and seed files are created by
`scripts/bootstrap_private_ops_runtime.py`. Usage:

```
python scripts/bootstrap_private_ops_runtime.py
python scripts/bootstrap_private_ops_runtime.py --target /opt/dealix-ops-private
PRIVATE_OPS=/opt/dealix-ops-private python scripts/bootstrap_private_ops_runtime.py
```

The bootstrap script creates the canonical file list with header
rows. Existing files are not overwritten unless `--force` is
provided.

## Folder tree

```
/opt/dealix-ops-private/
├── README.md
├── intelligence/
├── outreach/
├── approvals/
├── trust/
├── sales/
├── finance/
├── runtime/
├── distribution/
├── evals/
├── product/
├── security/
├── brand/
├── marketing/
├── growth/
├── customer_success/
├── proof/
└── founder/
```

Each subdirectory holds CSVs owned by one or more agents.

## CSV file list (canonical)

The list mirrors `FILES` in
`scripts/bootstrap_private_ops_runtime.py`. The first column is
the relative path; the rest are the header columns.

### `intelligence/`

| File                                  | Columns                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `intelligence/lead_intelligence_base.csv` | `id`, `sector`, `company`, `url`, `country`, `size`, `trigger_event`, `score`, `added_at`              |

### `outreach/`

| File                                  | Columns                                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `outreach/outreach_queue.csv`          | `id`, `channel`, `draft`, `approval_state`, `owner`, `due`, `created_at`                                |
| `outreach/conversation_log.csv`        | `id`, `lead_id`, `channel`, `stage`, `summary`, `ts`                                                    |
| `outreach/suppression_list.csv`        | `id`, `match_type`, `match_value`, `reason`, `added_by`, `added_at`                                     |
| `outreach/linkedin_queue.csv`          | `id`, `target`, `message_draft`, `approval_state`, `owner`, `created_at`                                |
| `outreach/contact_form_queue.csv`      | `id`, `target_url`, `message_draft`, `approval_state`, `owner`, `created_at`                            |
| `outreach/followup_queue.csv`          | `id`, `lead_id`, `draft`, `due_at`, `approval_state`                                                    |
| `outreach/reply_routing_queue.csv`     | `id`, `lead_id`, `intent`, `suggested_route`, `approval_state`                                          |
| `outreach/nurture_queue.csv`           | `id`, `lead_id`, `stage`, `next_touch_due`, `approval_state`                                            |

### `approvals/`

| File                              | Columns                                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| `approvals/approval_queue.csv`     | `id`, `type`, `risk`, `summary`, `payload_ref`, `status`, `created_at`                   |

### `trust/`

| File                               | Columns                                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| `trust/approval_decisions.csv`      | `id`, `ts`, `actor`, `action`, `target`, `risk`, `payload_json`                                |
| `trust/trust_flags.csv`             | `id`, `severity`, `description`, `source`, `created_at`                                        |
| `trust/incidents.csv`               | `id`, `status`, `severity`, `summary`, `owner`, `opened_at`, `closed_at`                       |

### `sales/`

| File                       | Columns                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| `sales/proposal_queue.csv`  | `id`, `client`, `offer`, `sprint`, `value_sar`, `status`, `created_at`                             |
| `sales/sample_queue.csv`    | `id`, `prospect`, `sample_type`, `status`, `approval_state`, `created_at`                          |

### `finance/`

| File                                  | Columns                                                                                |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| `finance/payment_capture_queue.csv`    | `id`, `client`, `invoice_no`, `amount_sar`, `status`, `due_date`                       |
| `finance/cash_collected.csv`           | `id`, `client`, `amount_sar`, `collected_at`, `method`                                 |
| `finance/ai_unit_economics.csv`        | `ts`, `ai_cost_usd`, `deals_supported`, `cost_per_deal_usd`                            |

### `runtime/`

| File                          | Columns                                                                |
| ----------------------------- | ---------------------------------------------------------------------- |
| `runtime/worker_state.csv`     | `id`, `name`, `status`, `last_run`, `failure_count`, `owner`           |

### `distribution/`

| File                                  | Columns                                                                                              |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `distribution/channel_scorecard.csv`   | `channel`, `draft_volume_7d`, `reply_rate`, `qualified_rate`, `owner`                                |
| `distribution/sector_scorecard.csv`    | `sector`, `accounts`, `engaged`, `qualified`, `won`, `owner`                                         |
| `distribution/experiment_log.csv`       | `id`, `hypothesis`, `channel`, `started_at`, `ended_at`, `result`, `status`, `owner`                 |

### `evals/`

| File                       | Columns                                                       |
| -------------------------- | ------------------------------------------------------------- |
| `evals/eval_status.csv`     | `ts`, `suite`, `pass`, `fail`, `blocking`, `notes`            |

### `product/`

| File                                   | Columns                                                                                           |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `product/productization_candidates.csv` | `id`, `offer`, `rung`, `readiness`, `owner`, `next_step`                                          |
| `product/offer_ladder.csv`              | `rung`, `name`, `positioning`, `price_band_sar`, `trust_gate`                                     |
| `product/product_distribution.csv`       | `rung`, `offer`, `channel`, `status`, `owner`                                                    |

### `security/`

| File                              | Columns                                                                          |
| --------------------------------- | -------------------------------------------------------------------------------- |
| `security/security_status.csv`     | `ts`, `secrets_scan`, `dependency_scan`, `pdpl_review`, `incident_open`          |

### `brand/`

| File                                  | Columns                                                                |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `brand/brand_assets_registry.csv`      | `id`, `asset_type`, `path`, `approved_by`, `ts`                        |

### `marketing/`

| File                              | Columns                                                                |
| --------------------------------- | ---------------------------------------------------------------------- |
| `marketing/content_calendar.csv`   | `day`, `topic`, `channel`, `owner`, `approval_state`                   |
| `marketing/campaigns.csv`          | `id`, `name`, `sector`, `owner`, `status`, `created_at`                |
| `marketing/content_ideas.csv`      | `id`, `topic`, `source`, `sector`, `owner`, `created_at`               |

### `growth/`

| File                              | Columns                                                                                |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| `growth/target_segments.csv`       | `segment`, `icp_fit`, `saudi_relevance`, `ticket_band_sar`, `priority`                 |
| `growth/sector_targets.csv`        | `sector`, `priority`, `accounts`, `score`, `owner`                                     |
| `growth/account_scores.csv`        | `account`, `sector`, `score`, `rank`, `next_action`                                    |
| `growth/distribution_machines.csv`  | `machine`, `owner`, `status`, `kpi`, `trust_gate`                                     |

### `customer_success/`

| File                                  | Columns                                                                |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `customer_success/client_health.csv`   | `client`, `health`, `next_action`, `due`, `owner`                      |
| `customer_success/referral_queue.csv`  | `id`, `client`, `referral_target`, `status`, `owner`                   |

### `proof/`

| File                                  | Columns                                                                |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `proof/proof_library.csv`              | `id`, `sector`, `title`, `summary_md_ref`, `approval_state`, `owner`   |
| `proof/proof_approval_queue.csv`       | `id`, `proof_id`, `submitted_by`, `status`, `ts`                       |

### `founder/`

| File                                  | Notes                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `founder/operating_scorecard.md`       | Four-pillar scorecard; refreshed nightly.                              |
| `founder/sovereign_readiness.md`       | Saudi residency / PDPL / NCA readiness; refreshed monthly.             |

## Write rules

Every CSV has a single sanctioned writer. The writer maps to an
`allowed_write_targets` entry in `registries/agent_registry.yaml`.
The rules:

1. **One writer per file.** Multiple readers; one writer. Concurrent
   writes are not supported.
2. **Append-only by default.** The audit ledger, suppression list,
   incidents, and conversation log are append-only.
3. **Workers must not edit existing rows.** State changes are
   recorded as additional rows where applicable.
4. **Schema additions append on the right.** New columns are added at
   the end of the header row to preserve compatibility.
5. **Header row is mutable only via the bootstrap script.** Workers
   never rewrite the header.

## File-by-writer ownership

| Writer                       | Files (allowed_write_targets)                                                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| `ceo_copilot`                | `founder/`                                                                                      |
| `brand_guardian`             | `brand/`                                                                                        |
| `growth_strategist`          | `growth/`                                                                                       |
| `distribution_operator`      | `outreach/`                                                                                     |
| `content_strategist`         | `marketing/`                                                                                    |
| `offer_architect`            | `product/`                                                                                      |
| `performance_analyst`        | `distribution/`                                                                                 |
| `trust_guardian`             | `trust/`                                                                                        |
| `eval_guardian`              | `evals/`                                                                                        |
| `finance_copilot`            | `finance/`                                                                                      |
| `delivery_copilot`           | `sales/`                                                                                        |
| `security_guardian`          | `security/`                                                                                     |
| `productization_agent`       | `product/`                                                                                      |
| `partner_revenue_agent`      | `customer_success/`                                                                             |
| `proof_safety_agent`         | `proof/`                                                                                        |
| `incident_response_agent`    | `trust/`                                                                                        |
| Founder Console router        | `trust/` (audit ledger only)                                                                    |

## Read rules

- Any agent may read any file inside the runtime via
  `api/internal/runtime_reader.py`.
- The reader returns an empty result with
  `source: "no-runtime"` when the runtime is unset, and
  `source: "missing"` when the file is absent.
- Readers must be tolerant to extra columns.

## Backups

The private ops runtime is backed up per
`docs/security/BACKUP_AND_RESTORE_OS.md`. The cadence is daily, the
retention is 30 days for daily snapshots and 12 months for monthly
snapshots. Restore is documented in the same file.

## Failure modes

| Failure                              | Behavior                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------- |
| Directory missing                    | Reader returns `no-runtime`; writer raises.                               |
| File missing                         | Reader returns `missing`; writer recreates with header via bootstrap.     |
| Schema drift                         | DQ system flags; worker should not write until reconciled.                 |
| Concurrent writer                    | Not supported; treat as an incident.                                       |
| Disk full                            | Writer raises; ops paging.                                                |

## Verifier

`scripts/verify_ultimate_operating_layer.py` and
`scripts/verify_sovereign_operating_stack.py` reference this contract
in spirit; the schema is enforced at write time by the bootstrap
script. A direct schema verifier is a planned addition.

## Discipline

1. Every file has one writer.
2. Every file traces back to a row in this document.
3. The bootstrap script is the authoritative schema source.
4. The audit ledger and suppression list never shrink.
5. The runtime is backed up daily and lives outside the repository.
