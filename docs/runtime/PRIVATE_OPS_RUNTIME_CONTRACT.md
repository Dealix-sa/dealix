# Private Ops Runtime Contract

## Purpose
Define temporary runtime CSV source-of-truth before Postgres becomes primary.

## Required Files
```txt
/opt/dealix-ops-private/intelligence/lead_intelligence_base.csv
/opt/dealix-ops-private/outreach/outreach_queue.csv
/opt/dealix-ops-private/outreach/conversation_log.csv
/opt/dealix-ops-private/outreach/suppression_list.csv
/opt/dealix-ops-private/approvals/approval_queue.csv
/opt/dealix-ops-private/trust/approval_decisions.csv
/opt/dealix-ops-private/sales/proposal_queue.csv
/opt/dealix-ops-private/finance/payment_capture_queue.csv
/opt/dealix-ops-private/finance/cash_collected.csv
/opt/dealix-ops-private/founder/ceo_runtime_state.json
```

## Environment Override
The base path is configurable via the `DEALIX_PRIVATE_OPS` environment variable.
Default: `/opt/dealix-ops-private`.

## Bootstrap
A bootstrap helper is provided at `scripts/bootstrap_private_ops.sh` which
creates empty CSVs with the required headers under either the env-provided
path or the default. Use this for local development or first-time setup.

## Schemas

### intelligence/lead_intelligence_base.csv
`account_id,company,sector,website,country,city,business_type,offer,buyer_titles,public_contact_path,source,fit_score,priority,why_fit,status,last_researched,last_contacted,reply_status,next_action`

### outreach/outreach_queue.csv
`outreach_id,account_id,company,channel,recipient_or_contact_path,message,approval_status,send_status,sent_at,next_action`

### outreach/conversation_log.csv
`date,account_id,company,channel,reply_type,summary,routed_to,next_action`

### outreach/suppression_list.csv
`company,contact,reason,source,date,status`

### approvals/approval_queue.csv
`approval_id,type,company,approval_class,risk_level,summary,evidence,recommended_action,status,created_at`

### trust/approval_decisions.csv
`approval_id,type,actor,decision,reason,approval_class,risk_level,policy_result,evidence,source_endpoint,timestamp,external_action_allowed`

### sales/proposal_queue.csv
`date,account_id,company,trigger,proposal_type,amount_sar,status,due_date,next_action`

### finance/payment_capture_queue.csv
`company,proposal_value,proposal_date,followup_stage,status,next_followup_date,next_action`

### finance/cash_collected.csv
`date,client,offer,amount_sar,payment_method,status,notes`

## Rule
CSV is acceptable for bootstrap.
Postgres becomes primary after live runtime proves daily use.
