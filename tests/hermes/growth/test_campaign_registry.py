"""Campaigns register as drafts linked to an offer and an ICP."""

from __future__ import annotations

from dealix.hermes.growth.campaign_registry import list_all, register, reset


def test_campaign_registers_as_draft() -> None:
    reset()
    cam = register("Q3 outreach", offer_id="of_1", icp_id="icp_x", channels=["email"])
    assert cam.status == "draft"
    assert cam.campaign_id in {c.campaign_id for c in list_all()}
