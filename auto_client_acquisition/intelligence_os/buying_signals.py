"""Buying signal detector — score prospect intent 0-100 based on events.

Doctrine:
  - Read-only (no actions)
  - Scores are estimates (Doctrine #6 — is_estimate=True)
  - Source events traced for transparency
  - No invented engagement metrics

Signal weights (default — tunable via founder_profile.yaml):
  - LinkedIn engagement on Dealix content       : 25 pts
  - Email opened                                 : 10 pts
  - Email replied                                : 30 pts
  - Demo booked                                  : 25 pts
  - Diagnostic submitted                         : 20 pts
  - WhatsApp read (with consent)                 : 5 pts
  - Re-engagement after silence                  : 15 pts

Threshold: 70+ = "hot" alert in cockpit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

SIGNAL_WEIGHTS = {
    "linkedin_engagement": 25,
    "email_opened": 10,
    "email_replied": 30,
    "demo_booked": 25,
    "diagnostic_submitted": 20,
    "whatsapp_read": 5,
    "re_engagement_after_silence": 15,
}

HOT_THRESHOLD = 70


@dataclass
class BuyingSignal:
    event_type: str
    weight: int
    timestamp: str
    source: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "weight": self.weight,
            "timestamp": self.timestamp,
            "source": self.source,
            "detail": self.detail,
        }


@dataclass
class BuyingIntentScore:
    prospect_brief_id: str
    score: int  # 0-100
    alert_level: str  # "none" | "watch" | "hot"
    signals: list[BuyingSignal] = field(default_factory=list)
    is_estimate: bool = True
    computed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "prospect_brief_id": self.prospect_brief_id,
            "score": self.score,
            "alert_level": self.alert_level,
            "signals": [s.to_dict() for s in self.signals],
            "is_estimate": self.is_estimate,
            "computed_at": self.computed_at,
        }


def compute_buying_intent(
    prospect_brief_id: str,
    events: list[dict[str, Any]],
) -> BuyingIntentScore:
    """Compose buying intent score from events.

    events: list of dicts each with at least:
      - event_type: str (must match a SIGNAL_WEIGHTS key)
      - timestamp: ISO 8601 str
      - source: str
      - detail: str (optional)
    """
    signals: list[BuyingSignal] = []
    total = 0

    for ev in events:
        etype = ev.get("event_type", "")
        if etype not in SIGNAL_WEIGHTS:
            continue
        weight = SIGNAL_WEIGHTS[etype]
        signals.append(
            BuyingSignal(
                event_type=etype,
                weight=weight,
                timestamp=ev.get("timestamp", datetime.now(UTC).isoformat()),
                source=ev.get("source", "unknown"),
                detail=ev.get("detail", ""),
            )
        )
        total += weight

    # Cap at 100
    score = min(100, total)

    if score >= HOT_THRESHOLD:
        alert_level = "hot"
    elif score >= 40:
        alert_level = "watch"
    else:
        alert_level = "none"

    return BuyingIntentScore(
        prospect_brief_id=prospect_brief_id,
        score=score,
        alert_level=alert_level,
        signals=signals,
    )


__all__ = [
    "HOT_THRESHOLD",
    "SIGNAL_WEIGHTS",
    "BuyingIntentScore",
    "BuyingSignal",
    "compute_buying_intent",
]
