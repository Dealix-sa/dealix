from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MessageAttribution:
    variant_id: str
    confidence: float
    angle: str = ""

    def __post_init__(self) -> None:
        if not self.variant_id:
            raise ValueError("variant_id required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
