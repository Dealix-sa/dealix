"""خادم المال — CashScout (spec §41).

Scans raw signals and surfaces the ones with a fast cash trail. Pure
heuristics — no LLM, no IO. Each surfaced lead points back to the
signal id so the orchestrator can pull the full context.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import Money
from dealix.hermes.core.signals import (
    Signal,
    SignalClassification,
    SignalClassifier,
    SignalSource,
)


class CashLead(BaseModel):
    """A short-form pointer at a high-urgency money signal."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(..., min_length=1)
    urgency: int = Field(..., ge=1, le=5)
    expected_amount: Money
    recommended_offer: str = Field(..., min_length=1, max_length=120)
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str = Field(..., min_length=1, max_length=400)


# ─────────────────────────────────────────────────────────────
# Heuristics
# ─────────────────────────────────────────────────────────────


_URGENT_KEYWORDS: tuple[str, ...] = (
    "today", "asap", "tomorrow", "this week", "deadline",
    "urgent", "now", "rush", "اليوم", "بسرعة", "عاجل",
)
_OFFER_KEYWORDS: dict[str, str] = {
    "pipeline": "Revenue Hunter Pilot",
    "lead": "Revenue Hunter Pilot",
    "meeting": "Revenue Hunter Pilot",
    "demo": "Revenue Hunter Pilot",
    "governance": "AI Trust Kit",
    "audit": "AI Trust Kit",
    "compliance": "AI Trust Kit",
    "agency": "Agency White-label Kit",
    "white-label": "Agency White-label Kit",
    "vertical": "Vertical Launch Sprint",
    "clinic": "Vertical Launch Sprint",
    "broker": "Vertical Launch Sprint",
    "renewal": "Renewal & Upsell Pack",
    "upsell": "Renewal & Upsell Pack",
    "retainer": "Renewal & Upsell Pack",
}
_DEFAULT_OFFER = "Revenue Hunter Pilot"


class CashScout:
    """Turn a stream of raw Signals into a list of triaged CashLeads."""

    def __init__(self, classifier: SignalClassifier | None = None) -> None:
        self._classifier = classifier or SignalClassifier()

    def scan(self, signals: list[Signal]) -> list[CashLead]:
        leads: list[CashLead] = []
        for signal in signals:
            classification = self._classifier.classify(signal)
            if not classification.monetizable:
                continue
            lead = self._lead_from(signal, classification)
            if lead is not None:
                leads.append(lead)
        leads.sort(key=lambda l: (-l.urgency, -l.confidence))
        return leads

    @staticmethod
    def _lead_from(
        signal: Signal,
        classification: SignalClassification,
    ) -> CashLead | None:
        text = signal.raw_text.lower()
        urgency = 3
        if any(kw in text for kw in _URGENT_KEYWORDS):
            urgency = 5
        if signal.source == SignalSource.TENDER:
            urgency = max(urgency, 4)
        if classification.repeatable:
            urgency = min(5, urgency + 1)

        # Confidence proportional to how many rules matched + sensitivity demerit.
        rule_count = len(classification.matched_rules)
        confidence = max(0.1, min(0.95, 0.4 + 0.1 * rule_count))
        if classification.sensitive:
            confidence = min(confidence, 0.6)

        recommended = _DEFAULT_OFFER
        for keyword, offer_name in _OFFER_KEYWORDS.items():
            if keyword in text:
                recommended = offer_name
                break

        # Expected amount baseline: pilot pricing midpoint.
        expected = Money.sar(Decimal("6000"))

        rationale_parts = [
            f"category={classification.category.value}",
            f"matched_rules={rule_count}",
        ]
        if classification.repeatable:
            rationale_parts.append("repeatable")
        if signal.source == SignalSource.TENDER:
            rationale_parts.append("source=tender")

        return CashLead(
            signal_id=signal.signal_id,
            urgency=urgency,
            expected_amount=expected,
            recommended_offer=recommended,
            confidence=round(confidence, 3),
            rationale="; ".join(rationale_parts),
        )


__all__ = ["CashLead", "CashScout"]
