#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

"$PYTHON_BIN" scripts/commercial/commercial_readiness_check.py
"$PYTHON_BIN" scripts/commercial/generate_commercial_go_live_pack.py
"$PYTHON_BIN" scripts/commercial/generate_daily_targeting_plan.py
"$PYTHON_BIN" scripts/commercial/generate_company_brain_pack.py
"$PYTHON_BIN" scripts/ops/backend_launch_cleanliness_check.py

echo "Commercial day completed. Review reports/commercial/latest.md, daily_targeting_plan.md, and company_brain_launch_pack.md."
