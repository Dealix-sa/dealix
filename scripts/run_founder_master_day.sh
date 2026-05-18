#!/usr/bin/env bash
# Master founder day — commercial morning + executive stack + production probe option.
# Usage:
#   bash scripts/run_founder_master_day.sh
#   DEALIX_VERIFY_PROD=1 bash scripts/run_founder_master_day.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Founder Master Day =="
bash "$ROOT/scripts/run_founder_commercial_day.sh"
echo ""
bash "$ROOT/scripts/founder_executive_stack_verify.sh" || true
echo ""
echo "FOUNDER_MASTER_DAY=PASS"
