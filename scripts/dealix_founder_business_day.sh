#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

SEGMENTS="${SEGMENTS:-clinics,training_centers,agencies,restaurants,real_estate}"
PER_SEGMENT="${PER_SEGMENT:-8}"
DRAFT_LIMIT="${DRAFT_LIMIT:-20}"
PROPOSAL_LIMIT="${PROPOSAL_LIMIT:-5}"

python founder_os/scripts/founder_business_autopilot.py \
  --segments "$SEGMENTS" \
  --per-segment "$PER_SEGMENT" \
  --draft-limit "$DRAFT_LIMIT" \
  --proposal-limit "$PROPOSAL_LIMIT"

TODAY="$(date +%F)"
echo ""
echo "Generated:"
echo "founder_os/output/$TODAY/DAILY_REPORT.md"
echo "founder_os/output/$TODAY/daily_targets.csv"
echo "founder_os/output/$TODAY/drafts/"
echo "founder_os/output/$TODAY/proposal_stubs/"
