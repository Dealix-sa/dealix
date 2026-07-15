"""
Section 75 — Marketplace Readiness.

A second binary readiness gate, for the Dealix marketplace. Mirrors
`PublicAPIReadiness` but with marketplace-specific checks.
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
    "asset_quality_review",
    "trust_review",
    "versioning",
    "payments",
    "partner_agreements",
    "refund_dispute_policy",
    "ratings",
    "liability_limits",
    "security_review",
)


_LISTINGS: tuple[str, ...] = (
    "agent_template",
    "workflow",
    "policy_pack",
    "training_kit",
    "sector_kit",
    "mcp_connector",
    "partner_service",
)


@dataclass
class MarketplaceReadiness:
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
            "listings": list(_LISTINGS),
        }

    def is_ready(self) -> bool:
        return all(self.checks.values()) and self.s4_approval_id is not None

    def assert_ready(self) -> None:
        missing = [k for k, v in self.checks.items() if not v]
        if missing:
            raise PermissionError(
                f"marketplace not ready — missing checks: {sorted(missing)}"
            )
        if self.s4_approval_id is None:
            raise PermissionError("marketplace not ready — S4 approval missing")

    def launch(self, *, approval_center: ApprovalCenter) -> None:
        self.assert_ready()
        card = approval_center.get(self.s4_approval_id or "")
        if card.sovereignty_level is not SovereigntyLevel.S4_LAUNCH_GATE:
            raise PermissionError("approval card is not S4_LAUNCH_GATE")
        if card.decision is not ApprovalDecision.APPROVED:
            raise PermissionError("S4 approval card not APPROVED")
        self.launched = True
