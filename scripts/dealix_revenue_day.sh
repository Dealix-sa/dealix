#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Revenue Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

safe_run() {
  local title="$1"
  shift
  echo ""
  echo "--- $title ---"
  if command -v timeout >/dev/null 2>&1; then
    timeout 120 "$@" || echo "WARN: $title skipped/failed"
  else
    "$@" || echo "WARN: $title skipped/failed"
  fi
}

safe_run "revenue engine v2" python company/revenue_engine/revenue_engine_v2.py

TODAY="$(date +%F)"
RUNTIME="company/runtime/revenue/${TODAY}"

echo ""
echo "FILES:"
if [ -d "$RUNTIME" ]; then
  ls "$RUNTIME"/
else
  echo "WARN: runtime dir not found — check engine output above"
fi

echo ""
echo "=== Revenue Day Complete ==="
echo "Next: open ${RUNTIME}/CEO_REVENUE_REPORT.md"
echo "Then: review WHATSAPP_DRAFTS.md and send manually"
