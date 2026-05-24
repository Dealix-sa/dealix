"""خادم المغامرات — VerticalLauncher (spec §35).

`VerticalCard` matches the §35 vertical-launch schema:

    vertical, buyer, pain, offer_name, price_band_sar,
    delivery_window_days, success_metric, exit_criteria,
    sami_kill_trigger
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VerticalCard(BaseModel):
    """§35 vertical-launch card."""

    model_config = ConfigDict(extra="forbid")

    vertical: str = Field(..., min_length=1, max_length=64)
    buyer: str = Field(..., min_length=1, max_length=120)
    pain: str = Field(..., min_length=1, max_length=600)
    offer_name: str = Field(..., min_length=1, max_length=160)
    price_band_sar: tuple[int, int]
    delivery_window_days: int = Field(..., ge=1, le=180)
    success_metric: str = Field(..., min_length=1, max_length=300)
    exit_criteria: list[str] = Field(..., min_length=1, max_length=10)
    sami_kill_trigger: str = Field(..., min_length=1, max_length=300)

    @model_validator(mode="after")
    def _price_band_ordered(self) -> VerticalCard:
        low, high = self.price_band_sar
        if low < 0:
            raise ValueError("price_band_sar low must be >= 0")
        if low > high:
            raise ValueError("price_band_sar low must be <= high")
        return self


SEED_VERTICAL_CARDS: tuple[VerticalCard, ...] = (
    VerticalCard(
        vertical="clinics",
        buyer="Clinic owner",
        pain="No-show losses and weak follow-up motion",
        offer_name="Clinic Activation Pilot",
        price_band_sar=(6000, 12000),
        delivery_window_days=21,
        success_metric="20 % reduction in no-show rate within 21 days",
        exit_criteria=[
            "No-show rate unchanged after 30 days",
            "Clinic refuses to integrate booking data",
            "PDPL consent flow cannot be implemented",
        ],
        sami_kill_trigger="3 clinics churn before day 60",
    ),
    VerticalCard(
        vertical="real_estate_brokers",
        buyer="Real-estate broker / agency owner",
        pain="Long sales cycles, soft qualification, weak referrals",
        offer_name="Broker Revenue Sprint",
        price_band_sar=(7500, 15000),
        delivery_window_days=30,
        success_metric="At least 2 closed deals attributable to Dealix within 30 days",
        exit_criteria=[
            "Broker pipeline unchanged after 45 days",
            "ZATCA compliance gap surfaces on first invoice",
        ],
        sami_kill_trigger="2 brokers churn before day 60",
    ),
)


class VerticalLauncher:
    """In-memory vertical-card registry."""

    def __init__(self, seed: bool = True) -> None:
        self._cards: dict[str, VerticalCard] = {}
        if seed:
            for card in SEED_VERTICAL_CARDS:
                self._cards[card.vertical] = card

    def register(self, card: VerticalCard) -> VerticalCard:
        if card.vertical in self._cards:
            raise ValueError(f"vertical already registered: {card.vertical}")
        self._cards[card.vertical] = card
        return card

    def get(self, vertical: str) -> VerticalCard:
        try:
            return self._cards[vertical]
        except KeyError as exc:
            raise KeyError(f"unknown vertical: {vertical}") from exc

    def all(self) -> list[VerticalCard]:
        return list(self._cards.values())

    @staticmethod
    def from_dict(data: dict[str, Any]) -> VerticalCard:
        """Build a VerticalCard from a dict (used by API surfaces)."""
        return VerticalCard.model_validate(data)


__all__ = ["SEED_VERTICAL_CARDS", "VerticalCard", "VerticalLauncher"]
