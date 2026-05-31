from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GEOAttribution:
    surface_id: str
    confidence: float
    engine: str = ""

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError("surface_id required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
