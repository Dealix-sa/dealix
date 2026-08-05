"""
Section 74 — Public API Readiness.

A binary readiness gate for the public API. Every checkbox must be
satisfied AND the S4 launch gate approval card must be APPROVED before
`launch()` will return without raising.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.control_plane.approval_center import (
    ApprovalCenter,
    ApprovalDecision,
    SovereigntyLevel,
)


_REQUIRED_CHECKS: tuple[str, ...] = (
    "auth",
    "rate_limits",
    "billing",
    "tenant_isolation",
    "audit",
    "abuse_detection",
    "terms",
    "kill_switch",
    "developer_docs",
)


_PRODUCTS: tuple[str, ...] = (
    "trust_check_api",
    "opportunity_score_api",
    "proposal_api",
    "evidence_pack_api",
    "outcome_api",
    "pricing_api",
    "partner_match_api",
)


@dataclass
class PublicAPIReadiness:
    """Tracks the readiness checklist for Dealix's public API."""

    checks: dict[str, bool] = field(default_factory=lambda: {c: False for c in _REQUIRED_CHECKS})
    s4_approval_id: str | None = None
    launched: bool = False

    def mark(self, check: str, *, value: bool = True) -> None:
        if check not in self.checks:
            raise KeyError(f"unknown check: {check}")
        self.checks[check] = value

    def status(self) -> dict[str, Any]:
        return {
            "checks": dict(self.checks),
            "checks_passed": sum(1 for v in self.checks.values() if v),
            "checks_total": len(self.checks),
            "s4_approval_id": self.s4_approval_id,
            "launched": self.launched,
            "products": list(_PRODUCTS),
        }

    def is_ready(self) -> bool:
        return all(self.checks.values()) and self.s4_approval_id is not None

    def assert_ready(self) -> None:
        missing = [k for k, v in self.checks.items() if not v]
        if missing:
            raise PermissionError(
                f"public API not ready — missing checks: {sorted(missing)}"
            )
        if self.s4_approval_id is None:
            raise PermissionError("public API not ready — S4 approval missing")

    def launch(self, *, approval_center: ApprovalCenter) -> None:
        self.assert_ready()
        card = approval_center.get(self.s4_approval_id or "")
        if card.sovereignty_level is not SovereigntyLevel.S4_LAUNCH_GATE:
            raise PermissionError("approval card is not S4_LAUNCH_GATE")
        if card.decision is not ApprovalDecision.APPROVED:
            raise PermissionError("S4 approval card not APPROVED")
        self.launched = True
