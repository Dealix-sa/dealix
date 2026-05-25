"""
Public-API readiness gate. Until every requirement is checked off
*and* S4 approval is granted, no endpoint may be exposed publicly.
"""

from __future__ import annotations

from dataclasses import dataclass


PUBLIC_API_REQUIREMENTS: tuple[str, ...] = (
    "auth",
    "rate_limits",
    "billing",
    "tenant_isolation",
    "audit",
    "abuse_detection",
    "developer_docs",
    "terms",
    "kill_switch",
    "monitoring",
    "s4_approval",
)


@dataclass
class PublicApiReadiness:
    ready: bool
    missing: tuple[str, ...]
    notes: str


def evaluate_readiness(checks: dict[str, bool]) -> PublicApiReadiness:
    missing = tuple(req for req in PUBLIC_API_REQUIREMENTS if not checks.get(req))
    notes = "All requirements satisfied." if not missing else f"Missing: {', '.join(missing)}"
    return PublicApiReadiness(ready=not missing, missing=missing, notes=notes)
