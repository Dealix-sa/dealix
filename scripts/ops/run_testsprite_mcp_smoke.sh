#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$ROOT/reports/runtime"
LOG_FILE="$LOG_DIR/testsprite_mcp_smoke.log"
TIMEOUT_SECONDS="${TESTSPRITE_MCP_TIMEOUT_SECONDS:-15}"

mkdir -p "$LOG_DIR"

if [[ -z "${TESTSPRITE_API_KEY:-}" ]]; then
  echo "TESTSPRITE_MCP_SMOKE=MISSING_SECRET"
  echo "Set TESTSPRITE_API_KEY or configure the GitHub Actions secret before running."
  exit 1
fi

# Never echo the key. TestSprite MCP expects API_KEY in the child environment.
export API_KEY="$TESTSPRITE_API_KEY"

echo "TESTSPRITE_MCP_SMOKE=STARTING"
echo "Package: @testsprite/testsprite-mcp@latest"
echo "Timeout seconds: $TIMEOUT_SECONDS"

set +e
timeout "$TIMEOUT_SECONDS" npx -y @testsprite/testsprite-mcp@latest >"$LOG_FILE" 2>&1
status=$?
set -e

if [[ "$status" == "0" ]]; then
  echo "TESTSPRITE_MCP_SMOKE=EXITED_CLEANLY"
  echo "Log: $LOG_FILE"
  exit 0
fi

if [[ "$status" == "124" ]]; then
  echo "TESTSPRITE_MCP_SMOKE=SERVER_STAYED_ALIVE"
  echo "The MCP server did not crash during the timeout window. This is acceptable for stdio MCP servers."
  echo "Log: $LOG_FILE"
  exit 0
fi

echo "TESTSPRITE_MCP_SMOKE=FAILED"
echo "Exit status: $status"
echo "Last log lines:"
tail -80 "$LOG_FILE" || true
exit "$status"
