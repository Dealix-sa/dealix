"""
Kill switch — a single trip that disables every MCP call across the
plane until manually cleared.
"""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class KillSwitch:
    tripped: bool = False
    reason: str = ""
    tripped_by: str = ""
    tripped_at: float = 0.0

    def trip(self, reason: str, tripped_by: str) -> None:
        if not reason or not tripped_by:
            raise ValueError("trip requires reason and tripped_by")
        self.tripped = True
        self.reason = reason
        self.tripped_by = tripped_by
        self.tripped_at = time.time()

    def clear(self, cleared_by: str, note: str) -> None:
        if not cleared_by or not note:
            raise ValueError("clear requires cleared_by and note")
        self.tripped = False
        self.reason = f"cleared by {cleared_by}: {note}"
        self.tripped_at = 0.0
