"""Compliance review rejects partners using unapproved claims."""

from __future__ import annotations

from dealix.hermes.partners.program.approved_claims import approve, reset
from dealix.hermes.partners.program.compliance import review


def test_compliance_flags_unapproved_claim() -> None:
    reset()
    approve("claim_roi", "Customers see 3x faster onboarding (median).", evidence_pack_id="ep_1")
    rep = review(
        "p_alpha",
        claims_used=[
            ("claim_roi", "Customers see 3x faster onboarding (median)."),
            ("claim_invented", "We guarantee 10x revenue."),
        ],
    )
    assert rep.compliant is False
    assert any("claim_invented" in v for v in rep.violations)
