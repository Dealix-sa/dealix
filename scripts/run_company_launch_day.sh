#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${REPO_ROOT}/.venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
  PYTHON="python3"
fi

export DEALIX_DATE="${DEALIX_DATE:-$(date +%Y-%m-%d)}"

echo "Running Dealix Company Launch Day — ${DEALIX_DATE}"
echo "============================================================"

exec "$PYTHON" scripts/run_company_launch_day.py "$@"
