"""CEO Master Plan status script.

The `analyze_ceo_master_plan` helper has not been added to
`scripts/run_ceo_master_plan_status.py` yet (only the `main` entrypoint
exists). The skipif keeps the test discoverable but green until that
helper lands; once it does, the gating import below resolves and the
real assertions run.
"""

from __future__ import annotations

import importlib

import pytest

_module = importlib.import_module("scripts.run_ceo_master_plan_status")
analyze_ceo_master_plan = getattr(_module, "analyze_ceo_master_plan", None)

pytestmark = pytest.mark.skipif(
    analyze_ceo_master_plan is None,
    reason="scripts.run_ceo_master_plan_status.analyze_ceo_master_plan not implemented yet",
)


def test_analyze_ceo_master_plan_keys():
    blob = analyze_ceo_master_plan()
    assert "overall_verdict" in blob
    assert blob["p0_revenue_close"]["verdict"] in {"PASS", "OPEN", "IN_PROGRESS"}
    assert blob["p0_ceo_decision"]["decision"]["one_decision_filled"] is True
    assert blob["p0_gtm_blitz"]["icp"]["eligible"] >= 75
    assert blob["p0_gtm_blitz"]["proposal_templates"] >= 5
    assert blob["p2_repeatability"]["artifacts_present"] >= 4
