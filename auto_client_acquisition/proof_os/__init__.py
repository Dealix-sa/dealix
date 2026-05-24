"""Proof OS — canonical proof artifacts for the Dealix AI Stack.

The proof layer (L7) assembles three institutional artifacts on every run:

1. **Proof Pack v2** — the 14-section bilingual artifact (AR + EN) the
   customer receives. See :mod:`.proof_pack`.
2. **Decision Passport** — an immutable, hash-bound record for every
   critical AI decision in the run. See :mod:`.decision_passport`.
3. **Evidence Chain** — an append-only, hash-linked ledger of every
   artifact produced during the run. See :mod:`.evidence_chain`.

A composite proof score (0..100) blends section completeness, evidence
depth, and governance posture. See :mod:`.proof_score`.
"""

from auto_client_acquisition.proof_os.decision_passport import (
    ApprovalLevel,
    Confidence,
    DecisionPassport,
    Reversibility,
    Sensitivity,
    issue_passport,
    passport_matches_content,
    passport_to_audit_row,
)
from auto_client_acquisition.proof_os.evidence_chain import (
    GENESIS_HASH,
    EvidenceChain,
    EvidenceLink,
    new_chain,
)
from auto_client_acquisition.proof_os.proof_pack import (
    PROOF_PACK_V2_SECTIONS,
    SECTION_LABELS_AR,
    SECTION_LABELS_EN,
    VALID_OFFER_TIERS,
    ProofPackV2,
    build_empty_proof_pack_v2,
    merge_proof_pack_v2,
    new_proof_pack,
    proof_pack_v2_sections_complete,
    render_json,
    render_markdown,
)
from auto_client_acquisition.proof_os.proof_score import (
    bilingual_completeness_score,
    composite_proof_score,
    evidence_depth_score,
    proof_pack_completeness_score,
    proof_pack_score_with_governance_penalty,
    proof_strength_band,
)

__all__ = [
    "GENESIS_HASH",
    "PROOF_PACK_V2_SECTIONS",
    "SECTION_LABELS_AR",
    "SECTION_LABELS_EN",
    "VALID_OFFER_TIERS",
    "ApprovalLevel",
    "Confidence",
    "DecisionPassport",
    "EvidenceChain",
    "EvidenceLink",
    "ProofPackV2",
    "Reversibility",
    "Sensitivity",
    "bilingual_completeness_score",
    "build_empty_proof_pack_v2",
    "composite_proof_score",
    "evidence_depth_score",
    "issue_passport",
    "merge_proof_pack_v2",
    "new_chain",
    "new_proof_pack",
    "passport_matches_content",
    "passport_to_audit_row",
    "proof_pack_completeness_score",
    "proof_pack_score_with_governance_penalty",
    "proof_pack_v2_sections_complete",
    "proof_strength_band",
    "render_json",
    "render_markdown",
]
