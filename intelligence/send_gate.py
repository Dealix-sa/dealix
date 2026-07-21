"""Global outbound send guard.

OUTBOUND_SEND_DISABLED is hard-coded to True. No environment variable can
override this — it is a code-level constraint. Every module that could trigger
external communication MUST call SendGate.assert_blocked() in draft paths.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any


class SendGateViolation(RuntimeError):
    """Raised if any code path attempts to send externally."""


class SendGate:
    OUTBOUND_SEND_DISABLED: bool = True  # Hard-coded; no env toggle

    @classmethod
    def assert_blocked(cls, action: str = "send") -> None:
        if cls.OUTBOUND_SEND_DISABLED:
            raise SendGateViolation(
                f"Action '{action}' is blocked. "
                "All outbound communication requires human approval and manual dispatch."
            )

    @classmethod
    def audit_log(
        cls,
        action: str,
        actor: str,
        draft_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log approval/rejection events to structured log (never sends)."""
        logging.getLogger(__name__).info(
            "send_gate_audit",
            action=action,
            actor=actor,
            draft_id=draft_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
