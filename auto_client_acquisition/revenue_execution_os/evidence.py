"""Evidence levels (L0-L5) re-exported for the Revenue Execution OS.

Thin convenience surface over ``proof_engine.evidence`` so distribution code
has one import site. No new vocabulary is introduced here.
"""

from __future__ import annotations

from auto_client_acquisition.proof_engine.evidence import (
    EVIDENCE_LEVEL_DESCRIPTIONS_AR,
    EVIDENCE_LEVEL_DESCRIPTIONS_EN,
    EvidenceLevel,
    assert_public_proof_allowed,
)

# Below this level a commercial claim may not be used in public marketing.
PUBLIC_MARKETING_MIN_LEVEL = int(EvidenceLevel.L4_PUBLIC_APPROVED)


def evidence_label(level: int, lang: str = "ar") -> str:
    """Bilingual description for an evidence level (empty string if unknown)."""
    table = EVIDENCE_LEVEL_DESCRIPTIONS_AR if lang == "ar" else EVIDENCE_LEVEL_DESCRIPTIONS_EN
    return table.get(int(level), "")


def is_public_marketing_allowed(level: int, *, consent_public: bool) -> bool:
    """True only when ``level`` >= L4 and explicit public consent is given."""
    return int(level) >= PUBLIC_MARKETING_MIN_LEVEL and bool(consent_public)


__all__ = [
    "EVIDENCE_LEVEL_DESCRIPTIONS_AR",
    "EVIDENCE_LEVEL_DESCRIPTIONS_EN",
    "PUBLIC_MARKETING_MIN_LEVEL",
    "EvidenceLevel",
    "assert_public_proof_allowed",
    "evidence_label",
    "is_public_marketing_allowed",
]
