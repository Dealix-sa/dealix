#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="$(command -v python3 2>/dev/null || echo py -3)"
if [[ "${1:-}" == "--evening" ]]; then
  exec $PY scripts/founder_evening_evidence.py "${@:2}"
fi
echo "== Founder daily cadence =="
$PY scripts/founder_agent_queue_status.py --seed-today
bash scripts/run_ceo_operating_stack.sh --skip-railway "$@"
