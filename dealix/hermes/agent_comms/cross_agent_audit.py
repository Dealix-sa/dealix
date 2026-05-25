"""Append-only ledger of agent-to-agent messages."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

_LEDGER_PATH_ENV = "DEALIX_HERMES_AGENT_AUDIT_PATH"
_DEFAULT_PATH = Path("data/hermes/agent_audit_ledger.jsonl")


@dataclass(frozen=True)
class AgentMessageRecord:
    message_id: str
    sender_agent: str
    receiver_agent: str
    intent: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0


def _path() -> Path:
    raw = os.environ.get(_LEDGER_PATH_ENV)
    p = Path(raw) if raw else _DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def record(sender_agent: str, receiver_agent: str, intent: str, payload: dict[str, Any] | None = None) -> AgentMessageRecord:
    """Append an agent-to-agent message envelope to the audit ledger."""
    rec = AgentMessageRecord(
        message_id=f"msg_{uuid.uuid4().hex[:12]}",
        sender_agent=sender_agent,
        receiver_agent=receiver_agent,
        intent=intent,
        payload=dict(payload or {}),
        timestamp=time.time(),
    )
    with _path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(rec), sort_keys=True) + "\n")
    return rec


def list_messages() -> list[AgentMessageRecord]:
    """Return every record currently in the agent audit ledger."""
    p = _path()
    if not p.exists():
        return []
    out: list[AgentMessageRecord] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(AgentMessageRecord(**json.loads(line)))
    return out
