"""HMAC-based signing of workflow intent: who, what, when."""

from __future__ import annotations

import hashlib
import hmac
import os
import time
from dataclasses import dataclass, field
from typing import Any


def _secret() -> bytes:
    return os.environ.get("DEALIX_HERMES_SECRET", "dealix-hermes-dev-secret").encode("utf-8")


@dataclass(frozen=True)
class IntentProof:
    intent: str
    actor: str
    timestamp: float
    signature: str
    payload: dict[str, Any] = field(default_factory=dict)


def _canonical(intent: str, actor: str, timestamp: float, payload: dict[str, Any]) -> bytes:
    items = sorted(payload.items())
    encoded = "|".join(f"{k}={v}" for k, v in items)
    return f"{intent}|{actor}|{timestamp:.6f}|{encoded}".encode("utf-8")


def sign_intent(intent: str, actor: str, payload: dict[str, Any] | None = None, *, ts: float | None = None) -> IntentProof:
    """Sign a workflow intent with HMAC-SHA256 and return an IntentProof."""
    ts = ts if ts is not None else time.time()
    payload = payload or {}
    msg = _canonical(intent, actor, ts, payload)
    sig = hmac.new(_secret(), msg, hashlib.sha256).hexdigest()
    return IntentProof(intent=intent, actor=actor, timestamp=ts, signature=sig, payload=dict(payload))


def verify_intent(proof: IntentProof) -> bool:
    """Return True when the IntentProof signature is valid."""
    msg = _canonical(proof.intent, proof.actor, proof.timestamp, proof.payload)
    expected = hmac.new(_secret(), msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, proof.signature)
