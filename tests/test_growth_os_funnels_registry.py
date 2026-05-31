"""Funnel registry tests."""

from __future__ import annotations

from dealix.growth_os.funnels.registry import FUNNELS, get_funnel, list_funnels


def test_required_funnels_present() -> None:
    keys = set(FUNNELS.keys())
    assert {"revenue_hunter", "ai_trust_kit", "agency_white_label"}.issubset(keys)
    assert len(list_funnels()) >= 3


def test_each_funnel_has_stages_and_offer_and_icp() -> None:
    for funnel in FUNNELS.values():
        assert funnel.stages, f"funnel {funnel.key} has no stages"
        assert funnel.primary_offer_key
        assert funnel.target_icp_keys
        for stage in funnel.stages:
            assert stage.key
            assert stage.label_ar
            assert stage.label_en
            assert stage.success_signal


def test_get_funnel_unknown_raises() -> None:
    try:
        get_funnel("nope")
    except KeyError:
        return
    raise AssertionError("expected KeyError")
