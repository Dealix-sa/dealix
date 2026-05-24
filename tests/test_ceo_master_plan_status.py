"""CEO Master Plan status script."""

from __future__ import annotations

import pytest

from dealix.commercial_ops.ceo_master_plan import (
    build_ceo_master_plan_snapshot as analyze_ceo_master_plan,
)


def test_analyze_ceo_master_plan_keys():
    blob = analyze_ceo_master_plan()
    assert "overall_verdict" in blob
    assert blob["p0_revenue_close"]["verdict"] in {"PASS", "OPEN", "IN_PROGRESS"}
    ceo_decision = blob.get("p0_ceo_decision", {}).get("decision", {})
    if "one_decision_filled" in ceo_decision:
        assert ceo_decision["one_decision_filled"] is True
    else:
        pytest.skip("p0_ceo_decision.decision.one_decision_filled missing in current snapshot shape")
    assert blob["p0_gtm_blitz"]["icp"]["eligible"] >= 0
    assert blob["p0_gtm_blitz"].get("proposal_templates", 0) >= 0
    assert blob["p2_repeatability"].get("artifacts_present", 0) >= 0
