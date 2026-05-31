"""Enablement assets are bound to tiers and discoverable per tier."""

from __future__ import annotations

from dealix.hermes.partners.program.partner_enablement import publish, required_for, reset


def test_required_for_returns_tier_assets() -> None:
    reset()
    publish("enab_referral_kit", "playbook", "Referral Kit", ["referral"])
    publish("enab_wl_cert", "certification", "White-label Cert", ["white_label"])
    assert {a.asset_id for a in required_for("referral")} == {"enab_referral_kit"}
