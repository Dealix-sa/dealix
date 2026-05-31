"""Verify a context packet hash matches an approved policy_version."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

_APPROVED_CONTEXTS: dict[str, str] = {}


@dataclass(frozen=True)
class ContextAttestation:
    policy_version: str
    context_hash: str
    approved: bool


def _hash_context(packet: dict[str, Any]) -> str:
    raw = json.dumps(packet, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def register_approved_context(policy_version: str, packet: dict[str, Any]) -> str:
    """Register an approved policy_version with its canonical context hash."""
    h = _hash_context(packet)
    _APPROVED_CONTEXTS[policy_version] = h
    return h


def attest_context(policy_version: str, packet: dict[str, Any]) -> ContextAttestation:
    """Return ContextAttestation comparing a context packet to the approved hash."""
    h = _hash_context(packet)
    approved = _APPROVED_CONTEXTS.get(policy_version) == h
    return ContextAttestation(policy_version=policy_version, context_hash=h, approved=approved)


def clear_registry() -> None:
    """Reset the in-memory approved-context registry (test helper)."""
    _APPROVED_CONTEXTS.clear()
