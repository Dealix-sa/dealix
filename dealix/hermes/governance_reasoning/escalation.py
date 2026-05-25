"""Escalation routing — append-only ledger producing approval_id tokens."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

_LEDGER_PATH_ENV = "DEALIX_HERMES_ESCALATION_PATH"
_DEFAULT_PATH = Path("data/hermes/escalation_ledger.jsonl")


@dataclass(frozen=True)
class EscalationTicket:
    approval_id: str
    action: str
    actor: str
    reason: str
    created_at: float
    context: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"


def _ledger_path() -> Path:
    raw = os.environ.get(_LEDGER_PATH_ENV)
    path = Path(raw) if raw else _DEFAULT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def escalate(action: str, actor: str, reason: str, context: dict[str, Any] | None = None) -> EscalationTicket:
    """Create a pending escalation ticket, append to ledger, return approval_id."""
    ticket = EscalationTicket(
        approval_id=f"esc_{uuid.uuid4().hex[:12]}",
        action=action,
        actor=actor,
        reason=reason,
        created_at=time.time(),
        context=dict(context or {}),
    )
    with _ledger_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(ticket), sort_keys=True) + "\n")
    return ticket


def list_pending() -> list[EscalationTicket]:
    """Return all escalation tickets currently in the ledger."""
    path = _ledger_path()
    if not path.exists():
        return []
    out: list[EscalationTicket] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            out.append(EscalationTicket(**data))
    return out
