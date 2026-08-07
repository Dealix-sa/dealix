#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Trust Day (Wave 7) ==="
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

safe_run "trust center manifest" python scripts/dealix_trust_center_manifest.py

echo ""
echo "--- trust file checks ---"

check_file() {
  path="$1"
  if [ -f "$path" ]; then
    echo "PASS: $path"
  else
    echo "FAIL: $path (missing)"
  fi
}

check_file "trust/AI_USAGE_POLICY_AR.md"
check_file "trust/HUMAN_APPROVAL_GATES.md"
check_file "trust/COMMERCIAL_SAFETY_GATES.md"

echo ""
echo "Wave 7 Trust Day complete."
