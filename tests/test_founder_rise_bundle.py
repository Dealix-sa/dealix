"""Founder executive day bundle tests."""

from __future__ import annotations

from dealix.commercial_ops.founder_rise_bundle import (
    build_executive_day_bundle,
    render_executive_day_md,
)


def test_build_executive_day_bundle_skip_live() -> None:
    blob = build_executive_day_bundle(skip_live=True)
    assert blob["verdict"] in ("CLEAR", "BLOCKED")
    assert "executive_snapshot" in blob
    assert "top_actions_ar" in blob
    assert len(blob["top_actions_ar"]) >= 1


def test_render_md_has_disclaimer() -> None:
    blob = build_executive_day_bundle(skip_live=True)
    md = render_executive_day_md(blob)
    assert "القيمة التقديرية" in md
