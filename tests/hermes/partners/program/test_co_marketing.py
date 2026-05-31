"""Co-marketing proposals are always queued as drafts requiring approval."""

from __future__ import annotations

from dealix.hermes.partners.program.co_marketing import draft, list_drafts, reset


def test_co_marketing_proposal_is_draft() -> None:
    reset()
    p = draft("p_alpha", "Joint webinar", ["webinar"], ["claim_roi"], notes="Q2")
    assert p.status == "draft"
    assert p.requires_approval is True
    assert list_drafts("p_alpha")[0].proposal_id == p.proposal_id
