"""Offer Builder — constructs Offer Cards with the canonical 6 fields."""

from __future__ import annotations

from dataclasses import dataclass, field


class OfferBuildError(ValueError):
    """Raised when an offer is missing a canonical field."""


@dataclass
class OfferCard:
    offer: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str]
    price_range_sar: str
    delivery_time: str = ""
    upsell: str = ""
    outcome_metric: str = ""
    extras: dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "offer": self.offer,
            "buyer": self.buyer,
            "pain": self.pain,
            "promise": self.promise,
            "deliverables": self.deliverables,
            "price_range_sar": self.price_range_sar,
            "delivery_time": self.delivery_time,
            "upsell": self.upsell,
            "outcome_metric": self.outcome_metric,
            **self.extras,
        }


class OfferBuilder:
    def build(
        self,
        *,
        offer: str,
        buyer: str,
        pain: str,
        promise: str,
        deliverables: list[str],
        price_range_sar: str,
        outcome_metric: str,
        delivery_time: str = "",
        upsell: str = "",
        extras: dict[str, str] | None = None,
    ) -> OfferCard:
        missing = [
            name
            for name, value in (
                ("offer", offer),
                ("buyer", buyer),
                ("pain", pain),
                ("promise", promise),
                ("deliverables", deliverables),
                ("price_range_sar", price_range_sar),
                ("outcome_metric", outcome_metric),
            )
            if not value
        ]
        if missing:
            raise OfferBuildError(f"offer_missing_required_fields:{','.join(missing)}")
        return OfferCard(
            offer=offer,
            buyer=buyer,
            pain=pain,
            promise=promise,
            deliverables=list(deliverables),
            price_range_sar=price_range_sar,
            delivery_time=delivery_time,
            upsell=upsell,
            outcome_metric=outcome_metric,
            extras=extras or {},
        )
