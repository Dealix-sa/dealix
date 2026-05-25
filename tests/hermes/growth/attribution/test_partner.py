"""Partner attribution captures partner-sourced verified revenue."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, partner


def test_partner_attribution() -> None:
    _base.reset()
    partner.attribute("partner_alpha", 18_000, evidence_pack_id="ep_1")
    assert partner.total("partner_alpha") == 18_000
