#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Follow-up Day (Wave 5) ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

safe_run() {
  title="$1"
  shift
  echo ""
  echo "--- $title ---"
  if command -v timeout >/dev/null 2>&1; then
    timeout 60 "$@" || echo "WARN: $title skipped/failed"
  else
    "$@" || echo "WARN: $title skipped/failed"
  fi
}

safe_run "crm follow-up engine" python company/crm/followup_engine.py

TODAY="$(date +%F)"
echo ""
echo "FILES:"
echo "company/runtime/${TODAY}_followup_drafts.csv"
echo ""
echo "NOTE: All drafts require founder approval before sending."
echo "NOTE: No messages have been sent automatically."
