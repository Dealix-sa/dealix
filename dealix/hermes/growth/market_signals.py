"""Ingest market signals (deal won/lost, demo request, churn) into Signal dataclasses."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

_SIGNAL_KINDS = {"deal_won", "deal_lost", "demo_request", "churn", "expansion", "referral"}


@dataclass(frozen=True)
class Signal:
    signal_id: str
    kind: str
    account_id: str
    value_sar: float
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0


_STORE: list[Signal] = []


def ingest(kind: str, account_id: str, value_sar: float = 0.0, metadata: dict[str, Any] | None = None) -> Signal:
    """Validate and record a market signal in the in-memory store."""
    if kind not in _SIGNAL_KINDS:
        raise ValueError(f"unknown signal kind: {kind}")
    sig = Signal(
        signal_id=f"sig_{uuid.uuid4().hex[:10]}",
        kind=kind,
        account_id=account_id,
        value_sar=float(value_sar),
        metadata=dict(metadata or {}),
        timestamp=time.time(),
    )
    _STORE.append(sig)
    return sig


def list_signals(kind: str | None = None) -> list[Signal]:
    """Return signals optionally filtered by kind."""
    if kind is None:
        return list(_STORE)
    return [s for s in _STORE if s.kind == kind]


def reset() -> None:
    """Clear the in-memory signal store (test helper)."""
    _STORE.clear()
