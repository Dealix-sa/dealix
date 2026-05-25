"""
Product Readiness Gate — Section 49.

أي offer لا يخرج للسوق قبل المرور على فحص بنيوي يضمن وجود كل العناصر
الحرجة (buyer / pain / promise / deliverables / price / cta / risks /
metric / upsell / delivery checklist / proof hypothesis).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .offer_registry import Offer


REQUIRED_FIELDS: tuple[tuple[str, str], ...] = (
    ("buyer", "buyer must be defined"),
    ("pain", "pain must be defined"),
    ("promise", "promise must be defined"),
    ("entry_cta", "entry_cta must be defined"),
    ("outcome_metric", "outcome_metric must be defined"),
    ("proof_hypothesis", "proof_hypothesis must be defined"),
)


@dataclass
class ReadinessResult:
    offer_id: str
    ready: bool
    score: int
    missing: list[str] = field(default_factory=list)
    required_before_launch: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "offer_id": self.offer_id,
            "ready": self.ready,
            "score": self.score,
            "missing": self.missing,
            "required_before_launch": self.required_before_launch,
        }


class ProductReadinessGate:
    def assess(self, offer: Offer) -> ReadinessResult:
        missing: list[str] = []
        required: list[str] = []
        max_points = 100
        points = max_points

        for attr, msg in REQUIRED_FIELDS:
            value = getattr(offer, attr, None)
            if not value:
                missing.append(attr)
                required.append(msg)
                points -= 10

        if not offer.deliverables:
            missing.append("deliverables")
            required.append("at least one deliverable is required")
            points -= 10

        if offer.price_min_sar <= 0 or offer.price_max_sar < offer.price_min_sar:
            missing.append("price_band")
            required.append(
                "price_min_sar must be > 0 and <= price_max_sar"
            )
            points -= 10

        if not offer.trust_risks:
            missing.append("trust_risks")
            required.append(
                "explicit trust_risks list is required for any external offer"
            )
            points -= 10

        if not offer.delivery_checklist:
            missing.append("delivery_checklist")
            required.append("delivery_checklist must contain at least 2 items")
            points -= 10
        elif len(offer.delivery_checklist) < 2:
            missing.append("delivery_checklist")
            required.append("delivery_checklist must contain at least 2 items")
            points -= 5

        if offer.upsell is None:
            missing.append("upsell")
            required.append(
                "upsell path is required (no offer without next-step revenue)"
            )
            points -= 5

        score = max(0, points)
        ready = not missing
        return ReadinessResult(
            offer_id=offer.offer_id,
            ready=ready,
            score=score,
            missing=missing,
            required_before_launch=required,
        )


__all__ = ["ProductReadinessGate", "ReadinessResult"]
