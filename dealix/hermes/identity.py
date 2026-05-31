"""Hermes identity primitives.

Non-negotiable #9: "No agent without identity." Every dispatch carries
agent_id=hermes and a monotonic run_id used in the audit ledger.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


AGENT_ID = "hermes"
AGENT_VERSION = "1.0.0"


def new_run_id() -> str:
    """Monotonic run_id: timestamp-millis + short uuid."""
    millis = int(time.time() * 1000)
    return f"hermes_{millis}_{uuid4().hex[:8]}"


@dataclass(frozen=True)
class HermesIdentity:
    agent_id: str = AGENT_ID
    version: str = AGENT_VERSION
    kill_switch: bool = False
    started_at: str = ""

    @classmethod
    def current(cls) -> "HermesIdentity":
        return cls(
            agent_id=AGENT_ID,
            version=AGENT_VERSION,
            kill_switch=os.getenv("HERMES_KILL_SWITCH", "0").strip() in {"1", "true", "yes"},
            started_at=datetime.now(UTC).isoformat(),
        )

    def signature(self, run_id: str) -> dict[str, str]:
        return {
            "agent_id": self.agent_id,
            "agent_version": self.version,
            "run_id": run_id,
            "signed_at": datetime.now(UTC).isoformat(),
        }
