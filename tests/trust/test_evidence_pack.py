"""Tests for `dealix/trust/evidence_pack.py`."""

from __future__ import annotations

import pytest

from dealix.trust.evidence_pack import approve, assert_complete, new_pack


def test_new_pack_starts_incomplete() -> None:
    pack = new_pack("EP-1", "We delivered the Sprint in 7 days.")
    assert not pack.is_complete()
    assert "sources (need at least 1)" in pack.missing_fields()


def test_pack_complete_after_filling_and_approval() -> None:
    pack = new_pack("EP-2", "We delivered in 7 days based on n=3 sprints.")
    pack.sources.append("internal:sprint_log/2026-Q2")
    pack.methodology = "Aggregated delivery days from n=3 sprints; range reported."
    approve(pack, "founder")
    assert pack.is_complete()
    assert_complete(pack)


def test_assert_complete_raises_when_missing() -> None:
    pack = new_pack("EP-3", "incomplete claim")
    with pytest.raises(ValueError):
        assert_complete(pack)
