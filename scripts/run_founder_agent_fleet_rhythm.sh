#!/usr/bin/env bash
# Print agent packets + optional queue seed — founder fleet daily rhythm.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="$(command -v python3 2>/dev/null || echo python3)"
WEEKLY=0
for arg in "$@"; do
  case "$arg" in
    --weekly) WEEKLY=1 ;;
  esac
done

echo "== Founder agent fleet rhythm =="
if [[ "$WEEKLY" -eq 1 ]]; then
  "$PYTHON_BIN" scripts/print_agent_work_packets.py --cadence weekly
else
  "$PYTHON_BIN" scripts/print_agent_work_packets.py --cadence daily
fi

if [[ -f scripts/founder_agent_queue_status.py ]]; then
  "$PYTHON_BIN" scripts/founder_agent_queue_status.py --seed-today 2>/dev/null || true
fi

echo "FOUNDER_AGENT_FLEET_RHYTHM=OK"
