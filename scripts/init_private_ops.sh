#!/usr/bin/env bash
# Bootstrap /opt/dealix-ops-private/ runtime data tree.
#
# Purpose: seed the private-ops directory tree and CSV headers consumed by
# scripts/generate_sales_cockpit.py and scripts/generate_approval_center.py.
# Idempotent: safe to re-run.
#
# Run once per server. Not tracked by git. Source-of-truth schema:
#   docs/data/GROWTH_DATABASE_MODEL_V2.md
#   schemas/growth_database.schema.json
#
# Usage:
#   bash scripts/init_private_ops.sh                       # defaults to /opt/dealix-ops-private
#   bash scripts/init_private_ops.sh /custom/path          # custom root
set -euo pipefail

ROOT="${1:-/opt/dealix-ops-private}"

mkdir -p \
  "$ROOT/growth" \
  "$ROOT/intelligence" \
  "$ROOT/outreach" \
  "$ROOT/distribution" \
  "$ROOT/sales" \
  "$ROOT/finance" \
  "$ROOT/delivery" \
  "$ROOT/client_success" \
  "$ROOT/trust" \
  "$ROOT/content" \
  "$ROOT/founder"

seed() {
  local path="$1"; shift
  local header="$1"; shift
  if [ ! -f "$path" ]; then
    printf '%s\n' "$header" > "$path"
    echo "seeded: $path"
  else
    echo "exists: $path"
  fi
}

seed "$ROOT/growth/market_accounts.csv" \
  "account_id,company,website,country,city,sector,business_type,offer,source,discovered_at,status,next_action"

seed "$ROOT/intelligence/lead_intelligence_base.csv" \
  "account_id,company,sector,website,country,city,business_type,offer,buyer_titles,public_contact_path,source,fit_score,priority,why_fit,status,last_researched,last_contacted,reply_status,next_action"

seed "$ROOT/outreach/outreach_queue.csv" \
  "outreach_id,account_id,company,channel,recipient_or_contact_path,message,approval_status,send_status,sent_at,next_action"

seed "$ROOT/outreach/suppression_list.csv" \
  "company,contact,reason,source,date,status"

seed "$ROOT/outreach/conversation_log.csv" \
  "date,account_id,company,channel,reply_type,summary,routed_to,next_action"

seed "$ROOT/distribution/channel_scorecard.csv" \
  "channel,leads,approved_outreach,sent,replies,positive_replies,samples,proposals,cash,trust_issues,decision,next_action"

seed "$ROOT/distribution/sector_scorecard.csv" \
  "sector,total_leads,a_leads,b_leads,approved,sent,replies,positive_replies,samples,proposals,cash,decision,next_action"

seed "$ROOT/distribution/experiment_log.csv" \
  "date,hypothesis,segment,channel,message_angle,sample_size,metric,threshold,result,decision,next_action"

seed "$ROOT/sales/proposal_queue.csv" \
  "date,account_id,company,trigger,proposal_type,amount_sar,status,due_date,next_action"

seed "$ROOT/finance/payment_capture_queue.csv" \
  "company,proposal_value,proposal_date,followup_stage,status,next_followup_date,next_action"

seed "$ROOT/client_success/retention_queue.csv" \
  "company,delivery_date,feedback_status,health_score,retainer_status,proof_status,referral_status,next_action"

echo
echo "PASS: private ops initialized at $ROOT"
echo "Next: 'make sales-cockpit' and 'make approval-center' (set PRIVATE_OPS=$ROOT if non-default)."
