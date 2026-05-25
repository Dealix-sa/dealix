#!/usr/bin/env bash
# Growth OS master verifier — runs the Python integrity check then the targeted pytest set.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

OK=1

echo "[growth_os] 1/2 Python integrity check…"
if python3 scripts/growth_os_verify.py >/tmp/growth_os_verify.log 2>&1; then
  INTEGRITY=pass
else
  INTEGRITY=fail
  OK=0
fi
tail -n 5 /tmp/growth_os_verify.log 2>/dev/null || true

echo "[growth_os] 2/2 pytest test_growth_os_*…"
if python3 -m pytest -q --no-cov tests/test_growth_os_icp_matrix.py \
    tests/test_growth_os_abm_pipeline.py \
    tests/test_growth_os_geo_checker.py \
    tests/test_growth_os_content_cta_matrix.py \
    tests/test_growth_os_revenue_proof_rules.py \
    tests/test_growth_os_revenue_quality_score.py \
    tests/test_growth_os_attribution.py \
    tests/test_growth_os_experiments.py \
    tests/test_growth_os_dashboard_red_flags.py \
    tests/test_growth_os_streams_decisions.py \
    tests/test_growth_os_funnels_registry.py \
    tests/test_growth_os_partners_motion.py \
    tests/test_growth_os_brand_positioning.py \
    tests/test_growth_os_operating_rules.py \
    tests/test_growth_os_router.py \
    >/tmp/growth_os_pytest.log 2>&1; then
  PYTEST=pass
else
  PYTEST=fail
  OK=0
fi
tail -n 12 /tmp/growth_os_pytest.log 2>/dev/null || true

echo ""
echo "================== DEALIX GROWTH OS VERDICT =================="
if [[ $OK -eq 1 ]]; then
  echo "DEALIX_GROWTH_OS_VERDICT=PASS"
else
  echo "DEALIX_GROWTH_OS_VERDICT=FAIL"
fi
echo "INTEGRITY=${INTEGRITY}"
echo "PYTEST=${PYTEST}"
echo "==============================================================="
exit $((1 - OK))
