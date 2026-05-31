"""
Run state — حالة كل agent run / workflow run قابلة للملاحظة من الـ UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    HELD_FOR_APPROVAL = "held_for_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    KILLED = "killed"


@dataclass
class RunState:
    run_id: str
    kind: str  # "agent" | "workflow"
    target_id: str  # agent_id or workflow_id
    request_id: str
    status: RunStatus = RunStatus.PENDING
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def transition(self, status: RunStatus, *, error: str | None = None) -> None:
        self.status = status
        if status in {RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.KILLED}:
            self.ended_at = datetime.now(timezone.utc)
        if error:
            self.error = error


__all__ = ["RunState", "RunStatus"]
