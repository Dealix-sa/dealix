from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.partners.program.approved_claims import check_partner_claim


@dataclass
class CoMarketingProposal:
    partner_id: str
    asset_title: str
    asset_body: str
    proposed_channels: list[str]


@dataclass
class CoMarketingReview:
    approved: bool
    findings: list[str]
    must_remove_phrases: list[str]


def review_co_marketing(proposal: CoMarketingProposal) -> CoMarketingReview:
    claim = check_partner_claim(proposal.asset_body)
    findings = list(claim.findings)
    if not proposal.proposed_channels:
        findings.append("no_channels_declared")
    # Bar live LinkedIn / WhatsApp blasts by default — those require an
    # explicit founder-approved campaign object.
    for ch in proposal.proposed_channels:
        if ch.lower() in {"whatsapp_broadcast", "linkedin_dm_blast"}:
            findings.append(f"unsupported_channel:{ch}")
    return CoMarketingReview(
        approved=not findings,
        findings=findings,
        must_remove_phrases=list({f.split(":", 1)[1] for f in findings if ":" in f}),
    )
