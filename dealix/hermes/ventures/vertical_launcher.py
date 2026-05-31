"""Vertical launcher — one Vertical Card per launch."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class VerticalCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vertical_id: str
    vertical: str
    buyer: str
    pain: str
    offer_id: str
    first_50_targets: list[str] = Field(default_factory=list)
    pilot_metric: str = ""
    scale_rule: str = ""
    kill_rule: str = ""
    approval_id: str | None = None


def launch_vertical(card: VerticalCard) -> VerticalCard:
    if not card.scale_rule or not card.kill_rule:
        raise ValueError("vertical launch requires both scale_rule and kill_rule")
    if not card.first_50_targets:
        raise ValueError("vertical launch requires a first-50 target list")
    return card
