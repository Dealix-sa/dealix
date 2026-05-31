"""PartnerClaim — approved (or forbidden) marketing claims partners may use."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PartnerClaim:
    claim: str
    approved: bool
    forbidden_variants: tuple[str, ...] = field(default_factory=tuple)


APPROVED_CLAIMS: tuple[PartnerClaim, ...] = (
    PartnerClaim(
        claim="Dealix helps generate B2B opportunity packs and proposal drafts.",
        approved=True,
        forbidden_variants=(
            "Dealix guarantees sales",
            "Dealix replaces your sales team completely",
            "Dealix promises 100% conversion",
        ),
    ),
    PartnerClaim(
        claim="Dealix runs governed AI agents with approval, audit, and outcome measurement.",
        approved=True,
        forbidden_variants=(
            "Dealix runs fully autonomous AI with no human oversight",
            "Dealix replaces your compliance team",
        ),
    ),
    PartnerClaim(
        claim="Dealix's evidence packs document AI policies aligned with PDPL.",
        approved=True,
        forbidden_variants=(
            "Dealix is officially certified by SDAIA",
            "Dealix guarantees full PDPL compliance",
        ),
    ),
)


def is_claim_approved(text: str) -> bool:
    low = text.lower()
    for claim in APPROVED_CLAIMS:
        for fv in claim.forbidden_variants:
            if fv.lower() in low:
                return False
    return True
