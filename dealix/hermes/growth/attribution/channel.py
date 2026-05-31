from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChannelAttribution:
    channel: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.channel:
            raise ValueError("channel required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
