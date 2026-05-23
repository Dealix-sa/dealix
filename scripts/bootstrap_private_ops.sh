#!/usr/bin/env bash
# Bootstrap empty Private Ops CSVs with required headers.
# Honours DEALIX_PRIVATE_OPS if set; otherwise uses /opt/dealix-ops-private.

set -euo pipefail

BASE="${DEALIX_PRIVATE_OPS:-/opt/dealix-ops-private}"

mkdir -p "$BASE"/{intelligence,outreach,approvals,trust,sales,finance,founder}

write_if_missing() {
  local path="$1"
  local header="$2"
  if [ ! -f "$path" ]; then
    printf '%s\n' "$header" > "$path"
    echo "created $path"
  else
    echo "kept    $path"
  fi
}

write_if_missing "$BASE/intelligence/lead_intelligence_base.csv" \
  "account_id,company,sector,website,country,city,business_type,offer,buyer_titles,public_contact_path,source,fit_score,priority,why_fit,status,last_researched,last_contacted,reply_status,next_action"

write_if_missing "$BASE/outreach/outreach_queue.csv" \
  "outreach_id,account_id,company,channel,recipient_or_contact_path,message,approval_status,send_status,sent_at,next_action"

write_if_missing "$BASE/outreach/conversation_log.csv" \
  "date,account_id,company,channel,reply_type,summary,routed_to,next_action"

write_if_missing "$BASE/outreach/suppression_list.csv" \
  "company,contact,reason,source,date,status"

write_if_missing "$BASE/approvals/approval_queue.csv" \
  "approval_id,type,company,approval_class,risk_level,summary,evidence,recommended_action,status,created_at"

write_if_missing "$BASE/trust/approval_decisions.csv" \
  "approval_id,type,actor,decision,reason,approval_class,risk_level,policy_result,evidence,source_endpoint,timestamp,external_action_allowed"

write_if_missing "$BASE/sales/proposal_queue.csv" \
  "date,account_id,company,trigger,proposal_type,amount_sar,status,due_date,next_action"

write_if_missing "$BASE/finance/payment_capture_queue.csv" \
  "company,proposal_value,proposal_date,followup_stage,status,next_followup_date,next_action"

write_if_missing "$BASE/finance/cash_collected.csv" \
  "date,client,offer,amount_sar,payment_method,status,notes"

if [ ! -f "$BASE/founder/ceo_runtime_state.json" ]; then
  printf '%s\n' '{}' > "$BASE/founder/ceo_runtime_state.json"
  echo "created $BASE/founder/ceo_runtime_state.json"
fi

echo "Private Ops runtime bootstrapped under: $BASE"
