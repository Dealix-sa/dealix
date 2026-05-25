"""Partner tier registration validates tier and lists by tier."""

from __future__ import annotations

import pytest

from dealix.hermes.partners.program.partner_tiers import list_all, register, reset


def test_register_partner_valid_and_invalid() -> None:
    reset()
    register("p_alpha", "Alpha Co", "referral", region="SA")
    assert list_all("referral")[0].partner_id == "p_alpha"
    with pytest.raises(ValueError):
        register("p_x", "Bad", "platinum")
