from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerAttribution:
    partner_id: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.partner_id:
            raise ValueError("partner_id required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
