"""Message-variant attribution aggregates per variant_id."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, message


def test_message_variant_attribution() -> None:
    _base.reset()
    message.attribute("var_a", 4_000, evidence_pack_id="ep_1")
    assert message.total("var_a") == 4_000
