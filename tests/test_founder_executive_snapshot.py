"""Founder executive snapshot unit smoke."""

from __future__ import annotations

from dealix.commercial_ops.founder_executive import build_founder_executive_snapshot


def test_executive_snapshot_skip_live() -> None:
    blob = build_founder_executive_snapshot(skip_live=True)
    assert "railway" in blob
    assert "first_paid" in blob
    assert blob["verdict"] in ("CLEAR", "BLOCKED")
    assert "evidence_csv" in blob["anchors"]
