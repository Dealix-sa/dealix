"""Partner motion + metrics tests."""

from __future__ import annotations

from dealix.growth_os.partners.metrics import PartnerMetrics
from dealix.growth_os.partners.motion import (
    PARTNER_MOTION_STAGES,
    PartnerMotion,
    list_stages,
)


def test_partner_motion_stages_present() -> None:
    stages = {s.key for s in PARTNER_MOTION_STAGES}
    expected = {"target", "qualify", "onboard", "enable", "first_deal", "repeat", "strategic"}
    assert expected.issubset(stages)
    assert list_stages() == list(PARTNER_MOTION_STAGES)


def test_partner_motion_wraps_stages() -> None:
    motion = PartnerMotion()
    assert motion.stages == PARTNER_MOTION_STAGES


def test_partner_metrics_conversion_rate() -> None:
    m = PartnerMetrics(
        partner_id="p_001",
        partner_label="Partner X",
        stage="repeat",
        sourced_leads=10,
        qualified_leads=5,
        deals_closed=2,
        real_revenue_usd=5000.0,
    )
    assert m.conversion_rate() == 0.2

    zero = PartnerMetrics(
        partner_id="p_002",
        partner_label="Partner Y",
        stage="target",
    )
    assert zero.conversion_rate() == 0.0
