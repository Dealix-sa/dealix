"""خادم الشركاء — PartnerScout.

Pure-function scout that filters incoming signals against criteria
(sector, region, minimum trust score) and produces ranked
PartnerCandidate records. No IO.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.signals import Signal, SignalCategory, SignalClassifier


class PartnerCriteria(BaseModel):
    """Filter applied to scout output."""

    model_config = ConfigDict(extra="forbid")

    segment: str = Field(..., min_length=1, max_length=64)
    min_trust_score: float = Field(default=2.0, ge=0.0, le=5.0)
    keywords: tuple[str, ...] = Field(default_factory=tuple)


class PartnerCandidate(BaseModel):
    """A candidate partner promoted from a Signal."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=200)
    segment: str = Field(..., min_length=1, max_length=64)
    why_relevant: str = Field(..., min_length=1, max_length=600)
    fit_signals: list[str] = Field(default_factory=list, max_length=10)
    trust_score: float = Field(default=2.5, ge=0.0, le=5.0)
    source_signal_id: str = Field(..., min_length=1)


class PartnerScout:
    """Surface partner candidates from a stream of Signals."""

    def __init__(self, classifier: SignalClassifier | None = None) -> None:
        self._classifier = classifier or SignalClassifier()

    def find(
        self,
        signals: list[Signal],
        criteria: PartnerCriteria,
        partner_metadata: dict[str, dict[str, Any]] | None = None,
    ) -> list[PartnerCandidate]:
        meta = partner_metadata or {}
        candidates: list[PartnerCandidate] = []
        for signal in signals:
            classification = self._classifier.classify(signal)
            if classification.category != SignalCategory.PARTNER:
                continue
            name = self._extract_name(signal, meta)
            metadata = meta.get(name, {})
            trust_score = float(metadata.get("trust_score", 2.5))
            if trust_score < criteria.min_trust_score:
                continue
            fit_signals = [
                f"rule:{rule}" for rule in classification.matched_rules
                if rule.startswith("partner")
            ]
            for kw in criteria.keywords:
                if kw.lower() in signal.raw_text.lower():
                    fit_signals.append(f"keyword:{kw}")
            why = (
                f"signal from {signal.source.value} matched partner category; "
                f"trust={trust_score}, segment={criteria.segment}"
            )
            candidates.append(
                PartnerCandidate(
                    name=name,
                    segment=criteria.segment,
                    why_relevant=why,
                    fit_signals=fit_signals,
                    trust_score=trust_score,
                    source_signal_id=signal.signal_id,
                )
            )
        candidates.sort(key=lambda c: (-c.trust_score, c.name))
        return candidates

    @staticmethod
    def _extract_name(signal: Signal, meta: dict[str, Any]) -> str:
        # Prefer explicit metadata.name from the Signal; otherwise fall
        # back to "Unknown Partner <signal id tail>".
        explicit = signal.metadata.get("partner_name") if signal.metadata else None
        if explicit:
            return explicit
        return f"Unknown Partner {signal.signal_id[-6:]}"


__all__ = ["PartnerCandidate", "PartnerCriteria", "PartnerScout"]
