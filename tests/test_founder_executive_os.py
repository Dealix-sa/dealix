from __future__ import annotations

from dealix.commercial_ops.founder_executive_os import build_founder_executive_snapshot


def test_executive_snapshot_keys() -> None:
    snap = build_founder_executive_snapshot(api_base=False)
    assert snap["launch_phase"] in ("SOFT", "PAID_ROADMAP", "PAID_READY")
    assert "railway_verdict" in snap
    assert "first_paid" in snap
