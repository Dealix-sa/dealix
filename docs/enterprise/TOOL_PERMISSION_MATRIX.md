# Tool Permission Matrix

The permission matrix is generated from the live agent registry and the
capability scopes declared in `dealix.hermes.identity`. Sample below.

## Domains

| Domain | Tools (examples) |
| --- | --- |
| `read` | `read_approved_opportunity`, `read_public_data`, `read_internal_doc` |
| `draft` | `draft_proposal`, `draft_message`, `summarize_call`, `flag_risk` |
| `internal_write` | `update_crm_internal`, `create_workflow_internal` |
| `external_send` | `send_external` |
| `approval` | `approve_price` |
| `executor` | `sign_contract`, `export_data`, `issue_refund`, `modify_production_config` |

## Sample matrix

| Agent | read | draft | internal_write | external_send | approval | executor |
| --- | --- | --- | --- | --- | --- | --- |
| `proposal_factory` | ✓ | ✓ |  |  |  |  |
| `market_radar` | ✓ | ✓ |  |  |  |  |
| `value_report_builder` | ✓ | ✓ |  |  |  |  |
| `crm_writer` | ✓ |  | ✓ |  |  |  |
| `external_drafter` | ✓ | ✓ |  | (drafts only — never sends) |  |  |
| `s4_executor` | ✓ |  |  |  |  | (kill-switch + dual approval) |

## Hard rules

1. `external_send`, `approve_price`, `sign_contract`, `export_data`,
   `issue_refund`, and `modify_production_config` are in
   `dealix.classifications.NEVER_AUTO_EXECUTE` — they always require
   human approval.
2. A `send_external` capability never includes a transport. The agent
   produces a draft; the human picks the transport.
3. Capability deltas (adds/removes) require an audit entry with
   `approved_by`.
