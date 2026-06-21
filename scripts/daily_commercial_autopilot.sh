#!/usr/bin/env bash
# Dealix Daily Commercial Autopilot
# Usage: bash scripts/daily_commercial_autopilot.sh [--gmail-push] [--count N]
# Cron: 0 5 * * * cd /home/user/dealix && bash scripts/daily_commercial_autopilot.sh >> logs/daily_autopilot.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DATE="$(date +%Y-%m-%d)"
COUNT="${COUNT:-120}"
GMAIL_PUSH="${1:-}"

echo "============================================"
echo "Dealix Daily Commercial Autopilot -- $DATE"
echo "============================================"

cd "$REPO_ROOT"

# 1. Generate 100+ drafts (all sectors, AR+EN)
echo "[1/4] Generating daily drafts..."
python3 scripts/generate_daily_mass_drafts.py \
  --sectors all \
  --count "$COUNT" \
  --date "$DATE" \
  ${GMAIL_PUSH:+--gmail-push --limit 50}

# 2. Export outreach-ready leads if API is running
echo "[2/4] Exporting outreach leads..."
if python3 -c "import httpx; r=httpx.get('http://localhost:8000/health', timeout=3); exit(0 if r.status_code==200 else 1)" 2>/dev/null; then
  python3 scripts/export_outreach_ready.py --max 50 \
    --out "data/daily_drafts/$DATE/leads_ready.csv" 2>/dev/null || true
else
  echo "  (API not running -- skipping live export)"
fi

# 3. Show today's summary
echo "[3/4] Summary:"
if [ -f "data/daily_drafts/$DATE/summary.md" ]; then
  head -20 "data/daily_drafts/$DATE/summary.md"
fi

# 4. List output files
echo "[4/4] Output files:"
ls -lh "data/daily_drafts/$DATE/" 2>/dev/null || echo "  No output directory found"

echo ""
echo "=== DONE: data/daily_drafts/$DATE/ ==="
echo "[REMINDER] All drafts require manual approval before sending."
