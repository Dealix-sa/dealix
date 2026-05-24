"""Market Radar — converts raw market signals into ranked opportunities.

The radar is a pure transformation. It does not fetch the internet. Feeds
are passed in (news headlines, open-data records, tender summaries) and
the radar emits Hermes Signals via `SignalIntake`. The orchestrator then
upgrades selected signals into opportunities.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.signals import SignalIntake
from dealix.hermes.core.schemas import Signal, SignalSource


@dataclass(slots=True)
class MarketFeedItem:
    source: SignalSource
    title: str
    summary: str
    payload: dict | None = None


class MarketRadar:
    def __init__(self, intake: SignalIntake) -> None:
        self._intake = intake

    def ingest(self, items: list[MarketFeedItem], *, captured_by: str) -> list[Signal]:
        out: list[Signal] = []
        for item in items:
            signal = self._intake.capture(
                source=item.source,
                title=item.title.strip()[:200],
                summary=item.summary.strip()[:2000],
                captured_by=captured_by,
                raw_payload=dict(item.payload or {}),
                tags=["market_radar"],
            )
            out.append(signal)
        return out


__all__ = ["MarketRadar", "MarketFeedItem"]
