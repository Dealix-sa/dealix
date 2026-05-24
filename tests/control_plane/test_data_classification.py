"""Data Classification (section 54)."""

from __future__ import annotations

import pytest

from dealix.control_plane.data_classification import (
    DataClass,
    DataClassificationPolicy,
)
from dealix.control_plane.sovereignty import SovereigntyTier


def test_public_data_can_be_sent_externally() -> None:
    assert DataClassificationPolicy.can_send_external(DataClass.PUBLIC) is True


def test_sovereign_data_blocks_external_and_export() -> None:
    assert DataClassificationPolicy.can_send_external(DataClass.SOVEREIGN) is False
    with pytest.raises(PermissionError):
        DataClassificationPolicy.assert_can_export(
            DataClass.SOVEREIGN, SovereigntyTier.INTERNAL
        )


def test_only_sami_feeds_sovereign_data_into_agent() -> None:
    assert (
        DataClassificationPolicy.can_feed_agent(DataClass.SOVEREIGN, SovereigntyTier.SAMI)
        is True
    )
    assert (
        DataClassificationPolicy.can_feed_agent(DataClass.SOVEREIGN, SovereigntyTier.AGENT)
        is False
    )


def test_restricted_requires_internal_or_higher_to_feed() -> None:
    assert (
        DataClassificationPolicy.can_feed_agent(
            DataClass.RESTRICTED, SovereigntyTier.INTERNAL
        )
        is True
    )
    assert (
        DataClassificationPolicy.can_feed_agent(
            DataClass.RESTRICTED, SovereigntyTier.AGENT
        )
        is False
    )
