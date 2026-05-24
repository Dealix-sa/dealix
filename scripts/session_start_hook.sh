#!/usr/bin/env bash
# Dealix session start hook — non-blocking pre-flight check.
# Always exits 0 so the Claude Code session can start even if checks fail.
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
DATE_STR="$(date '+%Y-%m-%d %H:%M:%S %Z')"

echo "Dealix session — pre-flight check"
echo "  date:   ${DATE_STR}"
echo "  branch: ${BRANCH}"
echo "---"

if [ -f scripts/dealix_status.py ]; then
  timeout 25 python scripts/dealix_status.py \
    || echo "WARN: dealix_status returned non-zero or timed out — proceed with caution"
else
  echo "WARN: scripts/dealix_status.py not found — skipping status check"
fi

echo "---"
echo -n "  tip:    "
git log -1 --oneline 2>/dev/null || echo "(no commits / not a git repo)"

UNCOMMITTED="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
echo "  uncommitted files: ${UNCOMMITTED}"

exit 0
