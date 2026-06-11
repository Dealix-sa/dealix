#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Dealix No-Crash Guard =="

echo "== Imports =="
python - <<'PY'
import pydantic, fastapi, pytest, pytest_asyncio
print("imports ok")
PY

echo "== Compile =="
python -m compileall -q api dealix scripts tests

echo "== Ruff targeted =="
ruff check \
  scripts/verify_company_ready.py \
  scripts/verify_full_mvp_ready.py \
  tests/test_company_os_verify.py \
  tests/test_founder_commercial_digest.py

echo "== Founder commercial digest =="
pytest -q tests/test_founder_commercial_digest.py

echo "== Business NOW =="
timeout 180 bash scripts/run_business_now.sh

echo "== Commercial launch =="
timeout 240 python3 scripts/verify_commercial_launch_ready.py

echo "== Founder go-live =="
timeout 420 bash scripts/founder_go_live_verify.sh

echo "NO_CRASH_GUARD=PASS"
