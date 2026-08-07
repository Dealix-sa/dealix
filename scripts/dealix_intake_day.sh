#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Intake Day ==="
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

safe_run "intake engine v2" python company/intake/intake_engine.py

TODAY="$(date +%F)"
RUNTIME="company/runtime/intake/${TODAY}"

echo ""
echo "FILES:"
if [ -d "$RUNTIME" ]; then
  ls "$RUNTIME"/
else
  echo "WARN: runtime dir not found"
fi

echo ""
echo "=== Intake Day Complete ==="
echo ""
echo "NEXT STEPS:"
echo "1. Open ${RUNTIME}/INTAKE_SUMMARY.md"
echo "2. Review Tier A first — contact within 24 hours"
echo "3. Review INTAKE_WHATSAPP_DRAFTS.md — send manually only"
echo "4. Review INTAKE_PROPOSAL_STUBS.md — Tier A only"
echo "5. Update CRM after every contact"
