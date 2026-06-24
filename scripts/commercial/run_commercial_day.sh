#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

"$PYTHON_BIN" scripts/commercial/commercial_readiness_check.py
"$PYTHON_BIN" scripts/commercial/generate_commercial_go_live_pack.py
"$PYTHON_BIN" scripts/commercial/generate_daily_targeting_plan.py
"$PYTHON_BIN" scripts/commercial/generate_company_brain_pack.py
"$PYTHON_BIN" scripts/commercial/generate_authorized_sales_agent_pack.py
"$PYTHON_BIN" scripts/commercial/generate_company_specific_sales_pack.py --company "Sample Riyadh B2B Company" --sector b2b_services --city Riyadh --source-url "manual_review_required"
"$PYTHON_BIN" scripts/commercial/generate_strategic_command_center.py
"$PYTHON_BIN" scripts/ops/backend_launch_cleanliness_check.py

echo "Commercial day completed. Review reports/commercial, reports/command_center, and reports/go_live."
