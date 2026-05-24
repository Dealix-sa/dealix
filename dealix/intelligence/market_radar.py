"""خادم الذكاء — MarketRadar.

Heuristic keyword scoring over news items. Each item is a dict with
keys: id, headline, source, body. Returns a list of MarketSignal
records ordered by score.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import utcnow


class MarketSignal(BaseModel):
    """A scored market observation."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(..., min_length=1, max_length=128)
    headline: str = Field(..., min_length=1, max_length=400)
    source: str = Field(..., min_length=1, max_length=128)
    category: str = Field(..., min_length=1, max_length=64)
    score: float = Field(..., ge=0.0, le=5.0)
    matched_terms: list[str] = Field(default_factory=list, max_length=20)
    captured_at: datetime = Field(default_factory=utcnow)


# Category keyword tables. Order matters — earlier wins ties.
_CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "regulation": (
        "pdpl", "zatca", "regulator", "sama", "moh", "fines",
        "compliance", "policy update", "تنظيم",
    ),
    "fundraising": (
        "raises", "series a", "series b", "seed round",
        "venture", "funding", "tamweel", "استثمار",
    ),
    "ai_governance": (
        "ai act", "ai policy", "responsible ai", "ai governance",
        "agent risk", "model risk", "حوكمة الذكاء",
    ),
    "sector_demand": (
        "demand surge", "shortage", "expansion", "rollout",
        "launch", "new clinic", "new broker", "نمو",
    ),
    "competitive": (
        "competitor", "rival", "new entrant", "displaced",
        "switched from", "vs ", "منافس",
    ),
}


class MarketRadar:
    """Scan a stream of news items and rank them by relevance."""

    def scan(self, news_items: list[dict[str, Any]]) -> list[MarketSignal]:
        signals: list[MarketSignal] = []
        for item in news_items:
            signal = self._score(item)
            if signal is None:
                continue
            signals.append(signal)
        signals.sort(key=lambda s: (-s.score, s.headline))
        return signals

    @staticmethod
    def _score(item: dict[str, Any]) -> MarketSignal | None:
        headline = str(item.get("headline") or "").strip()
        body = str(item.get("body") or "").strip()
        if not headline:
            return None
        text = f"{headline}\n{body}".lower()

        best_category = "noise"
        best_score = 0.0
        best_terms: list[str] = []
        for category, keywords in _CATEGORY_KEYWORDS.items():
            matched = [kw for kw in keywords if kw in text]
            if not matched:
                continue
            raw = 1.0 + 0.5 * len(matched)
            if any(kw in headline.lower() for kw in matched):
                raw += 1.0  # headline hits weigh extra
            if raw > best_score:
                best_score = raw
                best_category = category
                best_terms = matched

        if best_score == 0.0:
            return None

        signal_id = str(item.get("id") or f"ms_{abs(hash(headline)) % 10_000_000}")
        source = str(item.get("source") or "unknown")
        return MarketSignal(
            signal_id=signal_id,
            headline=headline,
            source=source,
            category=best_category,
            score=round(min(5.0, best_score), 3),
            matched_terms=best_terms,
        )


__all__ = ["MarketRadar", "MarketSignal"]
