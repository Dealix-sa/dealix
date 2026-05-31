"""Doctrine #8 / Article 4 — outreach rows are always draft-only + unapproved.

The sync is write-only: it never reads `Approved?` back to trigger a send.
The `_outreach_row` builder must encode that invariant regardless of input.
"""

from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("external_id", "title", "body", "channel"),
    [
        ("outreach-1", "Intro", "Hello there", "email"),
        ("outreach-2", "Follow up", "Checking in", "whatsapp"),
        ("outreach-3", "", "", "email"),
    ],
)
def test_outreach_row_always_draft_only_and_unapproved(
    external_id: str, title: str, body: str, channel: str
) -> None:
    from scripts.sync_founder_command_center_to_notion import (
        OUTREACH_GOVERNANCE_STATUS,
        _outreach_row,
    )

    ext, props = _outreach_row(
        external_id=external_id, title=title, body=body, channel=channel
    )

    assert ext == external_id
    assert props["Governance status"]["select"]["name"] == OUTREACH_GOVERNANCE_STATUS
    assert props["Governance status"]["select"]["name"] == "draft_only — awaiting approval"
    assert props["Approved?"]["checkbox"] is False


def test_outreach_status_constant_is_draft_only() -> None:
    from scripts.sync_founder_command_center_to_notion import OUTREACH_GOVERNANCE_STATUS

    assert OUTREACH_GOVERNANCE_STATUS == "draft_only — awaiting approval"
