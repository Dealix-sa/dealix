"""
Public methodology — a structured "how we work" page is a high-impact
trust signal that improves AI search citation rate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PublicMethodology:
    sections: list[str]
    has_evidence_pack: bool
    has_security_posture: bool
    has_governance_model: bool
    last_updated_iso: str


@dataclass
class PublicMethodologyScore:
    score: float
    missing: list[str]
    notes: list[str]


_REQUIRED_SECTIONS = (
    "scope_intake",
    "data_handling",
    "approval_flow",
    "delivery_quality_gates",
    "outcome_measurement",
    "incident_response",
)


def score_public_methodology(m: PublicMethodology) -> PublicMethodologyScore:
    present = {s.lower().strip() for s in m.sections}
    missing = [s for s in _REQUIRED_SECTIONS if s not in present]
    base = max(0.0, 100.0 - (len(missing) * 15))
    if not m.has_evidence_pack:
        base -= 10
    if not m.has_security_posture:
        base -= 10
    if not m.has_governance_model:
        base -= 10
    score = max(0.0, round(base, 2))
    notes: list[str] = []
    if missing:
        notes.append(f"missing sections: {missing}")
    if not m.last_updated_iso:
        notes.append("missing last_updated_iso — AI search distrusts stale pages")
    return PublicMethodologyScore(score=score, missing=missing, notes=notes)
