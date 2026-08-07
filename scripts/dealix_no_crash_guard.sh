#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Dealix No-Crash Guard =="

echo "== 1. Git dirty state =="
git status --short

echo "== 2. Python compile critical paths =="
python -m compileall -q api dealix scripts tests

echo "== 3. Ruff critical paths =="
ruff check api dealix scripts tests

echo "== 4. Commercial digest tests =="
pytest -q tests/test_founder_commercial_digest.py

echo "== 5. Revenue OS / Control Plane =="
bash scripts/run_business_now.sh

echo "== 6. Commercial launch ready =="
python3 scripts/verify_commercial_launch_ready.py

echo "== 7. Founder go-live =="
bash scripts/founder_go_live_verify.sh

echo "== 8. Secret file guard =="
python - <<'PY'
from pathlib import Path
bad = []
for p in [Path(".env"), Path(".env.local"), Path("frontend/.env.local")]:
    if p.exists():
        bad.append(str(p))
if bad:
    print("WARN: local env files exist; ensure they are ignored and never committed:", bad)
else:
    print("ok: no local env files detected at root/frontend")
PY

echo "NO_CRASH_GUARD=PASS"
