"""Proof strength score — deterministic readiness from canonical Proof Pack v2 sections.

The score is the weighted blend of:

* **Section completeness** (60%) — share of non-empty sections, AR + EN.
* **Evidence depth** (20%) — log-scaled count of evidence chain links.
* **Governance pass** (20%) — penalty when governance blocked the run.

The score lands in 0..100 and feeds the proof strength band used by the
commercial team (sales support / case candidate / weak proof).
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import PROOF_PACK_V2_SECTIONS


def proof_pack_completeness_score(content_by_section: Mapping[str, str]) -> int:
    """0–100 from share of non-empty v2 sections (no LLM)."""
    if not PROOF_PACK_V2_SECTIONS:
        return 0
    filled = sum(1 for k in PROOF_PACK_V2_SECTIONS if (content_by_section.get(k) or "").strip())
    return round(100.0 * filled / len(PROOF_PACK_V2_SECTIONS))


def bilingual_completeness_score(
    *,
    sections_ar: Mapping[str, str],
    sections_en: Mapping[str, str],
) -> int:
    """Average of AR and EN completeness scores."""
    ar = proof_pack_completeness_score(sections_ar)
    en = proof_pack_completeness_score(sections_en)
    return round((ar + en) / 2)


def evidence_depth_score(evidence_count: int) -> int:
    """0..100 — log-scaled with diminishing returns.

    1 link → ~10, 5 → ~50, 10 → ~70, 20 → ~85, 50+ → ~100.
    """
    if evidence_count <= 0:
        return 0
    raw = math.log(evidence_count + 1, math.e) * 30.0
    return round(min(100.0, raw))


def proof_strength_band(score: int) -> str:
    """Aligns with commercial proof ladder (internal sales / case gating)."""
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    if score >= 55:
        return "internal_learning"
    return "weak_proof"


def proof_pack_score_with_governance_penalty(
    content_by_section: Mapping[str, str],
    *,
    governance_blocked: bool,
) -> int:
    """If a governance BLOCK applies, cap score so weak proof cannot masquerade as case-ready."""
    base = proof_pack_completeness_score(content_by_section)
    if governance_blocked:
        return min(base, 69)
    return base


def composite_proof_score(
    *,
    sections_ar: Mapping[str, str],
    sections_en: Mapping[str, str],
    evidence_count: int,
    governance_blocked: bool,
) -> int:
    """Weighted composite proof score (0..100).

    Components:
        * 60% — bilingual section completeness
        * 20% — evidence depth (log-scaled)
        * 20% — governance pass (100 if clean, 0 if blocked)

    A governance block also caps the score at 69 so we never label a blocked
    run as ``case_candidate`` or even ``sales_support``.
    """
    completeness = bilingual_completeness_score(
        sections_ar=sections_ar,
        sections_en=sections_en,
    )
    depth = evidence_depth_score(evidence_count)
    governance = 0 if governance_blocked else 100
    blended = round(0.60 * completeness + 0.20 * depth + 0.20 * governance)
    if governance_blocked:
        return min(blended, 69)
    return max(0, min(100, blended))


__all__ = [
    "bilingual_completeness_score",
    "composite_proof_score",
    "evidence_depth_score",
    "proof_pack_completeness_score",
    "proof_pack_score_with_governance_penalty",
    "proof_strength_band",
]
