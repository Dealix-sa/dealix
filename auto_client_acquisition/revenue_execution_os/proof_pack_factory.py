"""Proof Pack factory — assembles canonical v2 proof packs (reuse, no new schema).

Wraps ``proof_os`` (14-section v2 pack) + ``proof_os.proof_score`` so the
distribution layer can attach a proof pack ref to a prospect/customer. The
non-negotiable "no paid project without a Proof Pack (score >= 70)" is checked
here via ``proof_pack_meets_bar``.
"""

from __future__ import annotations

from collections.abc import Mapping
from uuid import uuid4

from auto_client_acquisition.proof_os import (
    build_empty_proof_pack_v2,
    merge_proof_pack_v2,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_score_with_governance_penalty,
)
from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.evidence import EvidenceLevel
from auto_client_acquisition.revenue_execution_os.models import ProofPackRef, now_iso

# The commercial proof bar (matches proof_strength_band "sales_support").
PROOF_BAR = 70


def build_proof_pack(
    *,
    prospect_id: str = "",
    customer_id: str = "",
    sections: Mapping[str, str] | None = None,
    governance_blocked: bool = False,
) -> ProofPackRef:
    """Assemble a proof pack ref from (partial) v2 sections (pure)."""
    merged = merge_proof_pack_v2(build_empty_proof_pack_v2(), dict(sections or {}))
    complete, _missing = proof_pack_v2_sections_complete(merged)
    score = proof_pack_score_with_governance_penalty(merged, governance_blocked=governance_blocked)
    level = (
        int(EvidenceLevel.L2_CUSTOMER_REVIEWED)
        if complete
        else int(EvidenceLevel.L1_INTERNAL_DRAFT)
    )
    status = "ready" if score >= PROOF_BAR else "draft"
    return ProofPackRef(
        proof_pack_id=f"pp_{uuid4().hex[:18]}",
        prospect_id=prospect_id,
        customer_id=customer_id,
        sections=dict(merged),
        sections_complete=complete,
        score=score,
        evidence_level=level,
        status=status,
        created_at=now_iso(),
    )


def proof_pack_meets_bar(pack: ProofPackRef) -> bool:
    """True when the pack clears the commercial proof bar (score >= 70)."""
    return pack.score >= PROOF_BAR


def generate_proof_pack(
    *,
    prospect_id: str = "",
    customer_id: str = "",
    sections: Mapping[str, str] | None = None,
    governance_blocked: bool = False,
) -> ProofPackRef:
    """Build + persist a proof pack ref."""
    pack = build_proof_pack(
        prospect_id=prospect_id,
        customer_id=customer_id,
        sections=sections,
        governance_blocked=governance_blocked,
    )
    return stores.PROOF_PACKS.add(pack)


__all__ = [
    "PROOF_BAR",
    "build_proof_pack",
    "generate_proof_pack",
    "proof_pack_meets_bar",
]
