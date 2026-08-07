#!/usr/bin/env bash
# Dealix V10 master runner — runs the full V10 baseline.
# Exit on first hard failure; soft failures are allowed for optional steps.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bold() { printf "\n\033[1m== %s ==\033[0m\n" "$1"; }

bold "1. Secrets check"
python3 scripts/check_no_secrets.py

bold "2. Required env (demo)"
python3 scripts/check_required_env.py --mode demo

bold "3. Ultimate OS verification"
python3 scripts/verify_dealix_ultimate_os.py

bold "4. Daily operator (demo)"
python3 scripts/dealix_daily_operator.py --mode demo

bold "5. Demo pack"
python3 scripts/generate_demo_pack.py --lang both

bold "6. Release notes"
python3 scripts/generate_release_notes.py --days 7 || true

bold "7. Health snapshot"
python3 scripts/generate_health_snapshot.py

bold "8. Production readiness"
python3 scripts/production_readiness_check.py

bold "9. Pre-push guard"
python3 scripts/pre_push_guard.py

if [ -d apps/web ]; then
  bold "10. Web build"
  (cd apps/web && npm install --no-audit --no-fund && npm run typecheck && npm run build)
fi

echo ""
echo "Dealix V10 run-all complete."
