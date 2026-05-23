"""
Learning router.

Routes learning signals (win/loss outcome, message performance,
experiment result, friction-log entry) into the right private-repo
folder for review during the weekly intelligence cycle.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class LearningSignal:
    kind: str   # win | loss | message | experiment | friction | incident
    summary: str
    payload: dict
    captured_at: datetime


_DESTINATIONS = {
    "win": "learning/win_loss_review.md",
    "loss": "learning/win_loss_review.md",
    "message": "learning/message_performance.csv",
    "experiment": "learning/experiment_log.md",
    "friction": "learning/weekly_intelligence_review.md",
    "incident": "trust/data_incidents.md",
}


class LearningRouter:
    def route(self, signal: LearningSignal) -> str:
        return _DESTINATIONS.get(signal.kind, "learning/weekly_intelligence_review.md")

    def capture(self, kind: str, summary: str, **payload: object) -> LearningSignal:
        return LearningSignal(
            kind=kind,
            summary=summary,
            payload=dict(payload),
            captured_at=datetime.now(timezone.utc),
        )
