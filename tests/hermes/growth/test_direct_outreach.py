"""Outreach is always queued as DRAFT and requires approval; no network send."""

from __future__ import annotations

from dealix.hermes.growth.direct_outreach import list_drafts, queue_draft


def test_outreach_is_draft_and_requires_approval() -> None:
    d = queue_draft("cam_1", "acc_1", "email", "subject", "body")
    assert d.status == "draft"
    assert d.requires_approval is True
    assert list_drafts("cam_1") and list_drafts("cam_1")[-1].draft_id == d.draft_id
