from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrustSignalAttribution:
    signal_id: str
    confidence: float
    category: str = ""

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
