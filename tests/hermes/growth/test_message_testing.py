"""Variant outcomes require an evidence_pack_id and aggregate per variant."""

from __future__ import annotations

import pytest

from dealix.hermes.growth.message_testing import (
    attribution_for,
    record_outcome,
    register_variant,
    reset,
)


def test_outcome_requires_evidence_pack_id() -> None:
    reset()
    v = register_variant("cam_1", "A", "Hello {name}")
    record_outcome(v.variant_id, 12_000, evidence_pack_id="ep_1")
    assert attribution_for(v.variant_id) == 12_000
    with pytest.raises(ValueError):
        record_outcome(v.variant_id, 5_000, evidence_pack_id="")
