"""خادم الذكاء — CompetitorWatch.

Turns raw competitor observations (e.g. landing-page changes, pricing
announcements) into structured CompetitorEvent records.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import utcnow


class CompetitorEvent(BaseModel):
    """A structured competitor observation."""

    model_config = ConfigDict(extra="forbid")

    competitor: str = Field(..., min_length=1, max_length=200)
    kind: str = Field(..., min_length=1, max_length=64)
    summary: str = Field(..., min_length=1, max_length=600)
    detected_at: datetime = Field(default_factory=utcnow)
    urgency: int = Field(default=3, ge=1, le=5)
    suggested_response: str = Field(..., min_length=1, max_length=400)


_KIND_KEYWORDS: dict[str, tuple[str, ...]] = {
    "pricing_change": ("price drop", "new pricing", "discounted", "launched at"),
    "feature_release": ("released", "now supports", "new feature"),
    "funding": ("raised", "secured", "investment", "series"),
    "partnership": ("partnered with", "alliance with", "joint venture"),
    "executive_move": ("hired", "appointed", "joined as ceo", "joined as cto"),
}

_RESPONSE_PLAYBOOK: dict[str, str] = {
    "pricing_change": "Stress-test our price band; consider time-limited pilot pricing.",
    "feature_release": "Refresh proof bundle showing our equivalent capability.",
    "funding": "Update competitive map; alert sales on potential aggressive growth.",
    "partnership": "Audit our partner roster for overlap; brief partner team.",
    "executive_move": "Open a relationship-track playbook for the new exec.",
}


class CompetitorWatch:
    """Heuristic translator from raw observations to CompetitorEvents."""

    def observe(self, observations: list[dict[str, Any]]) -> list[CompetitorEvent]:
        events: list[CompetitorEvent] = []
        for raw in observations:
            event = self._classify(raw)
            if event is not None:
                events.append(event)
        events.sort(key=lambda e: (-e.urgency, e.competitor))
        return events

    @staticmethod
    def _classify(raw: dict[str, Any]) -> CompetitorEvent | None:
        competitor = str(raw.get("competitor") or "").strip()
        summary = str(raw.get("summary") or raw.get("text") or "").strip()
        if not competitor or not summary:
            return None
        text = summary.lower()

        kind = "general"
        for label, keywords in _KIND_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                kind = label
                break

        urgency = 3
        if kind in {"pricing_change", "funding"}:
            urgency = 4
        if kind == "partnership":
            urgency = 4

        response = _RESPONSE_PLAYBOOK.get(
            kind,
            "Log + monitor; revisit if it recurs in next cycle.",
        )
        return CompetitorEvent(
            competitor=competitor,
            kind=kind,
            summary=summary[:600],
            urgency=urgency,
            suggested_response=response,
        )


__all__ = ["CompetitorEvent", "CompetitorWatch"]
