"""
Evidence Synthesizer

Connects proof artifacts (testimonials, before/after metrics, deliverables,
audit logs) to commercial decisions and creates governed evidence packs.

This is the Trust Engine's intelligence surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EvidenceType(str, Enum):
    TESTIMONIAL = "testimonial"
    METRIC = "metric"
    DELIVERABLE = "deliverable"
    AUDIT_LOG = "audit_log"
    DECISION = "decision"
    CONTRACT = "contract"


class DecisionType(str, Enum):
    GO = "go"
    NO_GO = "no_go"
    CONDITIONAL = "conditional"
    DEFER = "defer"


@dataclass
class EvidenceItem:
    evidence_id: str
    evidence_type: EvidenceType
    title: str
    description: str
    source: str
    created_at: datetime
    verified: bool = False
    attachments: list[str] = field(default_factory=list)


@dataclass
class EvidencePack:
    pack_id: str
    decision_type: DecisionType
    decision: str
    confidence: float  # 0.0 - 1.0
    evidence_items: list[EvidenceItem]
    gaps: list[str]
    risks: list[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


class EvidenceSynthesizer:
    """Builds evidence-based decision packs for commercial actions."""

    def __init__(self):
        self._items: list[EvidenceItem] = []
        self._packs: list[EvidencePack] = []

    def add(self, item: EvidenceItem) -> None:
        self._items.append(item)

    def synthesize(
        self,
        decision_question: str,
        required_types: list[EvidenceType] | None = None,
    ) -> EvidencePack:
        """Synthesize evidence into a governed decision pack."""
        required_types = required_types or [
            EvidenceType.METRIC, EvidenceType.TESTIMONIAL, EvidenceType.DELIVERABLE
        ]

        matched = [item for item in self._items if item.verified]
        present_types = {item.evidence_type for item in matched}
        gaps = [f"Missing {t.value}" for t in required_types if t not in present_types]

        confidence = 0.0
        if EvidenceType.METRIC in present_types:
            confidence += 0.35
        if EvidenceType.TESTIMONIAL in present_types:
            confidence += 0.25
        if EvidenceType.DELIVERABLE in present_types:
            confidence += 0.25
        if EvidenceType.AUDIT_LOG in present_types:
            confidence += 0.15

        confidence = min(confidence, 1.0)

        risks = []
        if confidence < 0.5:
            risks.append("Insufficient evidence for a strong go decision")
        if EvidenceType.AUDIT_LOG not in present_types:
            risks.append("No audit trail attached")

        decision_type = DecisionType.CONDITIONAL
        if confidence >= 0.8 and not gaps:
            decision_type = DecisionType.GO
        elif confidence < 0.4:
            decision_type = DecisionType.DEFER

        decision_text = self._render_decision(decision_question, decision_type, confidence)

        pack = EvidencePack(
            pack_id=f"evp-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            decision_type=decision_type,
            decision=decision_text,
            confidence=round(confidence, 2),
            evidence_items=matched,
            gaps=gaps,
            risks=risks,
        )
        self._packs.append(pack)
        return pack

    def _render_decision(
        self,
        question: str,
        decision_type: DecisionType,
        confidence: float,
    ) -> str:
        prefixes = {
            DecisionType.GO: "GO",
            DecisionType.NO_GO: "NO GO",
            DecisionType.CONDITIONAL: "CONDITIONAL GO",
            DecisionType.DEFER: "DEFER",
        }
        return (
            f"{prefixes[decision_type]} — {question} "
            f"(confidence {confidence:.0%})"
        )

    def report(self) -> dict[str, Any]:
        return {
            "total_evidence_items": len(self._items),
            "verified_items": sum(1 for i in self._items if i.verified),
            "total_packs": len(self._packs),
            "go_decisions": sum(1 for p in self._packs if p.decision_type == DecisionType.GO),
        }
